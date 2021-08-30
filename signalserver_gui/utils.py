"""This module is a collection of utility functions for signalserver_gui."""
# TODO(Justin): Clean up unused imports.
import base64
import configparser
import glob
import os
import subprocess
from zipfile import ZipFile

import pandas as pd
from plotly.graph_objects import Figure, Scatter
import pyproj
import simplekml
from sqlalchemy import Boolean, DateTime, Float, Integer, String, Text, literal
from sqlalchemy.orm import with_expression
from sqlalchemy.sql.expression import desc

from .analysis_report.analysis_report import AnalysisReport
from .model import Antenna, Plot, Station, global_args, plot_args


def which(program):
    """Mimic linux 'which' program to determine if a progam is available."""

    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file
    return None


def run(cmd: str, args: list = []) -> str:
    """Execute a command using an external tool."""
    print("Running:", " ".join([cmd, *args]))
    try:
        app_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        result = subprocess.run(
            [cmd, *args],
            cwd=app_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=True,
        )
        return result.stdout.decode("utf-8")
    except Exception as e:
        return str(e)


def generate(config: configparser.ConfigParser, item: Plot) -> str:
    """Generate plot files."""
    # Arg format: (flag, name, required, type, default, description)
    global_defaults = {
        "terrain_greyscale": False,
        "debug": False,
        "normalize": False,
        "halve": 1,
        "nothreads": False,
        "spatial_data_files": config["signalserver"]["elevation_data_dir"],
        "lidar_data_dir": config["signalserver"]["lidar_data_dir"],
        "user_data_files": config["signalserver"]["user_data_dir"],
        "clutter_data_files": config["signalserver"]["clutter_data_dir"],
        "color_profile": config["signalserver"]["color_profile"],
    }

    # Build string of arguments for signalserver.
    command_args = []
    p2pa_args = []
    for key in global_args.keys():
        arg = global_args[key]
        if arg["type"] == bool:
            if key in config["signalserver"]:
                value = (
                    config["signalserver"].getboolean(key)
                    if key in config["signalserver"]
                    else global_defaults[key]
                )
                if value:
                    command_args.append(arg["flag"])
        elif not arg["depends"] or any(getattr(item, i) for i in arg["depends"]):
            if key in config["signalserver"]:
                command_args.append(arg["flag"])
                command_args.append(str(config["signalserver"][key]))

    for key in plot_args["plot"].keys():
        arg = plot_args["plot"][key]
        table = Plot.__table__
        if arg["flag"]:
            if (
                arg["depends"]
                and "do_p2p_analysis" in arg["depends"]
                and any(getattr(item, i) for i in arg["depends"])
            ):
                if isinstance(table.columns[key].type, Boolean):
                    if hasattr(item, key) and getattr(item, key):
                        p2pa_args.append(arg["flag"])
                else:
                    if hasattr(item, key) and getattr(item, key):
                        p2pa_args.append(arg["flag"])
                        p2pa_args.append(str(getattr(item, key)))
            elif not arg["depends"] or any(getattr(item, i) for i in arg["depends"]):
                if isinstance(table.columns[key].type, Boolean):
                    if hasattr(item, key) and getattr(item, key):
                        command_args.append(arg["flag"])
                else:
                    if hasattr(item, key) and getattr(item, key):
                        command_args.append(arg["flag"])
                        command_args.append(str(getattr(item, key)))

    for key in plot_args["antenna"].keys():
        arg = plot_args["antenna"][key]
        table = Antenna.__table__
        if key == "filename":
            command_args.append(arg["flag"])
            command_args.append(
                os.path.join(
                    config["signalserver"]["antenna_profiles_dir"],
                    item.antenna.type,
                    item.antenna.filename,
                )
            )
        elif arg["flag"]:
            if (
                arg["depends"]
                and "do_p2p_analysis" in arg["depends"]
                and any(getattr(item, i) for i in arg["depends"])
            ):
                if isinstance(table.columns[key].type, Boolean):
                    if hasattr(item, key) and getattr(item, key):
                        p2pa_args.append(arg["flag"])
                else:
                    if hasattr(item, key) and getattr(item, key):
                        p2pa_args.append(arg["flag"])
                        p2pa_args.append(str(getattr(item, key)))
            elif not arg["depends"] or any(getattr(item, i) for i in arg["depends"]):
                if isinstance(table.columns[key].type, Boolean):
                    if hasattr(item.antenna, key) and getattr(item.antenna, key):
                        command_args.append(arg["flag"])
                else:
                    if hasattr(item.antenna, key) and getattr(item.antenna, key):
                        command_args.append(arg["flag"])
                        command_args.append(str(getattr(item.antenna, key)))

    for key in plot_args["station"].keys():
        arg = plot_args["station"][key]
        table = Station.__table__
        if arg["flag"]:
            if (
                arg["depends"]
                and "do_p2p_analysis" in arg["depends"]
                and any(getattr(item, i) for i in arg["depends"])
            ):
                if key.startswith("rx_"):
                    station = item.station2
                    key = key[3:]
                else:
                    station = item.station1
                if isinstance(table.columns[key].type, Boolean):
                    if hasattr(station, key) and getattr(station, key):
                        p2pa_args.append(arg["flag"])
                elif key == "polarization":
                    if hasattr(station, key) and getattr(station, key) == "horizontal":
                        p2pa_args.append(arg["flag"])
                else:
                    if hasattr(station, key) and getattr(station, key):
                        p2pa_args.append(arg["flag"])
                        p2pa_args.append(str(getattr(station, key)))
            elif not arg["depends"] or any(getattr(item, i) for i in arg["depends"]):
                if key.startswith("rx_"):
                    station = item.station2
                    key = key[3:]
                else:
                    station = item.station1
                if isinstance(table.columns[key].type, Boolean):
                    if hasattr(station, key) and getattr(station, key):
                        command_args.append(arg["flag"])
                elif key == "polarization":
                    if hasattr(station, key) and getattr(station, key) == "horizontal":
                        command_args.append(arg["flag"])
                else:
                    if hasattr(station, key) and getattr(station, key):
                        command_args.append(arg["flag"])
                        command_args.append(str(getattr(station, key)))

    item_path = os.path.join(config["signalservergui"]["output_dir"], str(item.id))
    try:
        os.makedirs(item_path)
    except:
        pass
    file_base = os.path.join(item_path, item.name)
    command_args.extend(["-o", file_base])

    # Use 'signalserverHD' if resolution is set to 3600.
    if item.resolution == 3600:
        command = config["signalserver"]["path"] + "HD"
    else:
        command = config["signalserver"]["path"]
    # Run signalserver command and capture output for use in kml.
    dimensions = run(command, command_args).split("|")
    run(
        config["convert"]["path"],
        [
            f"{file_base}.ppm",
            "-transparent",
            "white",
            "-alpha",
            "set",
            "-background",
            "none",
            "-channel",
            "A",
            "-evaluate",
            "multiply",
            str(item.opacity),
            f"{file_base}.{config['convert']['output_type']}",
        ],
    )

    if item.do_p2p_analysis:
        p2pa_args.append("-ng")
        command_args.extend(p2pa_args)
        results = run(command, command_args)
        make_analysis_plot(item, file_base, results, config["convert"]["output_type"])
        report = parse_p2p_anaylsis(f"{file_base}.txt")
        with open(f"{file_base}.json", "w") as f:
            f.write(report.to_json())
        make_kmz(item, file_base, dimensions, config["convert"]["output_type"], report)
    else:
        make_kmz(item, file_base, dimensions, config["convert"]["output_type"])

    with ZipFile(f"{file_base}.zip", "w") as zip:
        for filename in glob.glob(f"{item_path}/*"):
            if "zip" not in filename:
                zip.write(filename, os.path.basename(filename))
    return ""


def make_kmz(
    item: Plot,
    file_base: str,
    dimensions: list,
    image_type="png",
    report: AnalysisReport = None,
):
    """Generate a keyhole markup file representing the plot."""
    # TODO(Justin): Convert units to metric if plot is using imperial units.
    azimuth = 0
    description = f"Longitude: {item.station1.longitude} Latitude:{item.station1.latitude} Height: {item.station1.height}"
    kml = simplekml.Kml()

    # Create kml style for use in various objects.
    no_icon_style = simplekml.Style()
    no_icon_style.iconstyle.icon.href = None
    start_style = simplekml.Style()
    start_style.labelstyle.color = simplekml.Color.green
    start_style.labelstyle.scale = 2
    start_style.iconstyle.color = simplekml.Color.green
    start_style.iconstyle.icon.href = (
        "http://maps.google.com/mapfiles/kml/pushpin/grn-pushpin.png"
    )
    start_style.linestyle.color = simplekml.Color.green
    start_style.linestyle.width = 8
    start_style.linestyle.gxlabelvisibility = 1
    start_style.polystyle.color = simplekml.Color.green
    start_style.polystyle.fill = 0
    end_style = simplekml.Style()
    end_style.labelstyle.color = simplekml.Color.red
    end_style.labelstyle.scale = 2
    end_style.iconstyle.color = simplekml.Color.red
    end_style.iconstyle.icon.href = (
        "http://maps.google.com/mapfiles/kml/pushpin/red-pushpin.png"
    )
    end_style.linestyle.color = simplekml.Color.red
    end_style.linestyle.width = 8
    end_style.linestyle.gxlabelvisibility = 1
    end_style.polystyle.color = simplekml.Color.red
    end_style.polystyle.fill = 0
    view_style = simplekml.Style()
    view_style.iconstyle.color = simplekml.Color.blue
    view_style.iconstyle.icon.href = (
        "http://maps.google.com/mapfiles/kml/pushpin/blue-pushpin.png"
    )
    view_style.linestyle.color = simplekml.Color.blue
    view_style.linestyle.width = 0
    view_style.linestyle.gxlabelvisibility = False
    view_style.polystyle.color = simplekml.Color.blue
    view_style.polystyle.fill = 0
    valid_line_style = simplekml.Style()
    valid_line_style.linestyle.color = simplekml.Color.green
    valid_line_style.linestyle.width = 2
    valid_line_style.linestyle.gxlabelvisibility = 1
    valid_line_style.polystyle.color = "aa00ff00"  # Green with transparency
    valid_line_style.polystyle.fill = 1
    invalid_line_style = simplekml.Style()
    invalid_line_style.linestyle.color = simplekml.Color.red
    invalid_line_style.linestyle.width = 2
    invalid_line_style.linestyle.gxlabelvisibility = 1
    invalid_line_style.polystyle.color = "aa0000ff"  # Red with transparency
    invalid_line_style.polystyle.fill = 1

    # Add map point for station1 to kml
    station1 = kml.newpoint(name=f"Station 1: {item.station1.name}")
    station1.description = description
    station1.coords = [
        (item.station1.longitude, item.station1.latitude, item.station1.height)
    ]
    station1.style = start_style
    station1.extrude = True
    station1.lookat.longitude = item.station1.longitude
    station1.lookat.latitude = item.station1.latitude
    station1.lookat.altitudemode = simplekml.AltitudeMode.relativetoground
    station1.lookat.altitude = item.station1.height + 100
    station1.lookat.range = 2500
    station1.lookat.tilt = 80
    station1.lookat.heading = azimuth + 10
    station1.altitudemode = simplekml.AltitudeMode.relativetoground
    # Embed plot image in kml.
    plot_file = kml.addfile(f"{file_base}.{image_type}")
    # Add plot to kml as a ground overlay.
    plot = kml.newgroundoverlay(name=f"Plot: {item.name}")
    plot.style = valid_line_style
    plot.icon.href = plot_file
    plot.altitude = item.station1.height
    plot.altitudemode = simplekml.AltitudeMode.relativetoground
    plot.latlonbox.north = dimensions[1]
    plot.latlonbox.east = dimensions[2]
    plot.latlonbox.south = dimensions[3]
    plot.latlonbox.west = dimensions[4]

    if item.do_p2p_analysis:
        # Add additional components to kml for p2p analysis.
        geodesic = pyproj.Geod(ellps="WGS84")
        azimuth, back_azimuth, distance = geodesic.inv(
            item.station1.longitude,
            item.station1.latitude,
            item.station2.longitude,
            item.station2.latitude,
        )
        with open(f"{file_base}_ppa.{image_type}", "rb") as image_file:
            # Load analysis image, base64 encode, embed in description using SVG tag.
            description = f"""\
<![CDATA[
    <svg xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink' height='480' width='640'>
        <image xlink:href='data&colon;image/{image_type};base64,{base64.b64encode(image_file.read()).decode()}' />
    </svg>
]]>"""
        # Build description text of analysis.
        # TODO(Justin): Create better description using new AnalysisReport class.
        with open(file_base + ".txt") as analysis:
            description += "<p><ul>"
            for line in analysis:
                description += f"<li>{line}</li>"
            description += f"</ul></p><p>Azimuth: {azimuth:0.2f}</p>"
        kml.addfile(f"{file_base}_ppa.{image_type}")
        # Add analyasis items to station1.
        station1.description = description
        station1.lookat.heading = azimuth + 10
        # Hide plot overlay by default when including P2P analysis.
        plot.visibility = False
        # Add station2 to kml.
        station2 = kml.newpoint(name=f"Station 2: {item.station2.name}")
        station2.description = description
        station2.coords = [
            (item.station2.longitude, item.station2.latitude, item.station2.height)
        ]
        station2.style = end_style
        station2.extrude = True
        station2.lookat.longitude = item.station2.longitude
        station2.lookat.latitude = item.station2.latitude
        station2.lookat.altitudemode = simplekml.AltitudeMode.relativetoground
        station2.lookat.altitude = item.station2.height + 100
        station2.lookat.range = 2500
        station2.lookat.tilt = 80
        station2.lookat.heading = back_azimuth + 10
        station2.altitudemode = simplekml.AltitudeMode.relativetoground
        # Add segmented line if link is obstructed.
        if report and report.link.obstructions:
            clear_los_path = kml.newlinestring(name="Clear Line of Sight Path")
            clear_los_path.style = valid_line_style
            clear_los_path.description = description
            clear_los_path.altitudemode = simplekml.AltitudeMode.relativetoground
            clear_los_path.extrude = True
            clear_los_path.coords = [
                (item.station1.longitude, item.station1.latitude, item.station1.height),
                (
                    report.link.obstructions[0].longitude,
                    report.link.obstructions[0].latitude,
                    report.link.obstructions[0].height,
                ),
            ]
            obstructed_los_path = kml.newlinestring(
                name="Obstructed Line of Sight Path"
            )
            obstructed_los_path.style = invalid_line_style
            obstructed_los_path.altitudemode = simplekml.AltitudeMode.relativetoground
            obstructed_los_path.extrude = True
            path_points = []
            for obs in report.link.obstructions:
                path_points.append((obs.longitude, obs.latitude, obs.height))
            path_points.append(
                (item.station2.longitude, item.station2.latitude, item.station2.height),
            )
            obstructed_los_path.coords = path_points
        else:
            # Add single line path if link is unobstructed.
            los_path = kml.newlinestring(name="Line of Sight Path")
            los_path.style = valid_line_style
            los_path.description = description
            los_path.altitudemode = simplekml.AltitudeMode.relativetoground
            los_path.extrude = True
            los_path.coords = [
                (item.station1.longitude, item.station1.latitude, item.station1.height),
                (item.station2.longitude, item.station2.latitude, item.station2.height),
            ]
    kml.savekmz(f"{file_base}.kmz")


def db_to_norm(db: float) -> float:
    """Convert decibel value to normal."""
    return 10 ** (db / 20.0)


def convert_ant_file(ant_file: str, azimuth_offset=0, elevation_offset=0) -> None:
    """Convert antenna profile (.ant) to signalserver format (.az, .el)."""
    base_filename, ext = os.path.splitext(ant_file)
    az_filename = base_filename + ".az"
    el_filename = base_filename + ".el"
    with open(ant_file, "r") as ant:
        with open(az_filename, "w") as az:
            # azimuth offset as provided by
            az.write(f"{float(azimuth_offset):0.1f}\n")
            # Read the first 360 lines of the file
            for i in range(360):
                az.write(f"{i:d}\t{db_to_norm(float(next(ant))):0.4f}\n")
        with open(el_filename, "w") as el:
            # mechanical downtilt, azimuth of tilt
            el.write(f"{float(elevation_offset):0.1f}\t{float(azimuth_offset):0.1f}\n")
            # Read the lines for elevations +10 through -90).
            # The rest of the .ant is unused.
            for i, line in enumerate(list(ant)[80:181], -10):
                el.write(f"{i:d}\t{db_to_norm(float(line)):0.4f}\n")


def make_analysis_plot(
    item: Plot, file_base: str, results: str, image_type="png"
) -> None:
    """Generate a P2P analysis graph image from signalserver analysis files."""
    curvature = [
        (float(line.split(" ")[0]), float(line.split(" ")[1]))
        for line in open(file_base + "_curvature")
    ]
    fresnel = [
        (float(line.split(" ")[0]), float(line.split(" ")[1]))
        for line in open(file_base + "_fresnel")
    ]
    fresnel60 = [
        (float(line.split(" ")[0]), float(line.split(" ")[1]))
        for line in open(file_base + "_fresnel60")
    ]
    profile = [
        (float(line.split(" ")[0]), float(line.split(" ")[1]))
        for line in open(file_base + "_profile")
    ]
    reference = [
        (float(line.split(" ")[0]), float(line.split(" ")[1]))
        for line in open(file_base + "_reference")
    ]

    reference_df = pd.DataFrame(reference, columns=["Distance", "Value"])
    profile_df = pd.DataFrame(profile, columns=["Distance", "Value"])
    curvature_df = pd.DataFrame(curvature, columns=["Distance", "Value"])
    fresnel_bottom_df = pd.DataFrame(fresnel, columns=["Distance", "Value"])
    fresnel60_bottom_df = pd.DataFrame(fresnel60, columns=["Distance", "Value"])
    fresnel_top_df = fresnel_bottom_df.copy()
    fresnel_top_df["Value"] = fresnel_top_df["Value"].multiply(-1)
    fresnel60_top_df = fresnel60_bottom_df.copy()
    fresnel60_top_df["Value"] = fresnel60_top_df["Value"].multiply(-1)
    fig = Figure()
    fig.add_trace(
        Scatter(
            x=reference_df["Distance"],
            y=reference_df["Value"],
            mode="lines",
            line=dict(shape="linear", color="rgb(0, 0, 0)", width=4, dash="dot"),
            name="Line of Sight",
        )
    )
    fig.add_trace(
        Scatter(
            x=curvature_df["Distance"],
            y=curvature_df["Value"],
            mode="lines",
            line=dict(shape="linear", color="rgb(100, 100, 100)"),
            name="Earth Curvature",
        )
    )

    fig.add_trace(
        Scatter(
            x=fresnel60_bottom_df["Distance"],
            y=fresnel60_bottom_df["Value"],
            mode="lines",
            line=dict(shape="linear", color="rgb(235, 60, 0)"),
            name="First Fresnel Zone (60%)",
        )
    )
    fig.add_trace(
        Scatter(
            x=fresnel_bottom_df["Distance"],
            y=fresnel_bottom_df["Value"],
            mode="lines",
            line=dict(shape="linear", color="rgb(150, 180, 0)"),
            name="First Fresnel Zone (100%)",
        )
    )

    fig.add_trace(
        Scatter(
            x=profile_df["Distance"],
            y=profile_df["Value"],
            mode="lines",
            line=dict(shape="linear", color="rgb(101, 56, 24)"),
            name="Terrain Profile",
            fill="tozeroy",
        )
    )
    # fig.update_xaxes(type="log")
    # fig.update_yaxes(type="log")
    units = ("km", "m") if item.use_metric_units else ("mi", "ft")
    fig.update_layout(
        title="Site to Site Analysis",
        xaxis=dict(
            tickmode="auto",
            ticksuffix=units[0],
        ),
        yaxis=dict(
            tickmode="auto",
            ticksuffix=units[1],
        ),
        height=480,
        width=640,
    )
    fig.write_image(f"{file_base}_ppa.{image_type}")
    # fig.show()


def parse_p2p_anaylsis(analysis_file):
    """Parse raw signalserver analysis file(.txt) into an AnalysisReport object."""
    base_filename, _ = os.path.splitext(analysis_file)
    # curvature_file = base_filename + "_curvature"
    # fresnel_file = base_filename + "_fresnel"
    # fresnel60_file = base_filename + "_fresnel60"
    # profile_file = base_filename + "_profile"
    # reference_file = base_filename + "_reference"
    return AnalysisReport.from_file(analysis_file)
