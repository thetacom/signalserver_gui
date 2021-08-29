#! /usr/bin/env python
"""A lightweight web gui for signalserver."""
# TODO(Justin): Remove unused imports
import sys
import os

path = os.path.dirname(sys.modules[__name__].__file__)
path = os.path.join(path, "..")
sys.path.insert(0, path)

import configparser
import functools
import glob
import os
import re
import shutil

from bottle import (
    HTTPError,
    abort,
    delete,
    error,
    get,
    install,
    jinja2_template,
    post,
    redirect,
    request,
    route,
    run,
    static_file,
)
from bottle.ext import sqlalchemy
from sqlalchemy import create_engine, event, literal
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.sql.sqltypes import Boolean, Float, Integer

from signalserver_gui import model
from signalserver_gui import utils
from signalserver_gui.model import Antenna, Plot, Station, global_args, plot_args

# from model import Base, Antenna, Station, Plot, _fk_pragma_on_connect

engine = model.init()
plugin = sqlalchemy.Plugin(
    engine,
    model.Base.metadata,
    keyword="db",
    create=True,
    commit=True,
    use_kwargs=False,
)
install(plugin)
template = functools.partial(jinja2_template, template_lookup=["templates"])
config = configparser.ConfigParser()


@get("/")
def index():
    """Render the index page."""
    messages = [
        {
            "title": "Welcome!",
            "message": "Welcome to Signal Server GUI!",
        },
    ]

    parts = {"title": "Home"}
    if messages:
        parts["messages"] = messages
    return template("index.html", parts)


@get("/favicon.ico")
def favicon():
    """Serve favicon.ico."""
    return static_file("favicon.ico", root="./static/img")


@get("/img/<filepath:path>")
def server_images(filepath):
    """Serve static image files."""
    return static_file(filepath, root="./static/img")


@get("/js/<filepath:path>")
def server_javascript(filepath):
    """Serve static javascript files."""
    return static_file(filepath, root="./static/js")


@get("/css/<filepath:path>")
def server_stylesheets(filepath):
    """Serve static stylesheet files."""
    return static_file(filepath, root="./static/css")


@get("/download/<filename:path>")
def download(filename):
    """Server download files."""
    return static_file(filename, root="downloads", download=filename)


@error(404)
def error404(error):
    """Render the error page."""
    return "Nothing here, sorry"


@get("/search")
def search(db):
    """Render the station search page."""
    search_type = request.query.type
    search = request.query.q
    search_type_col = literal("plot").label("type")
    if search_type == "stations":
        query = db.query(Station).filter(Station.name.like(f"%{search}%"))
    elif search_type == "antennas":
        query = db.query(Antenna).filter(Antenna.name.like(f"%{search}%"))
    elif search_type == "plots":
        query = db.query(Plot).filter(Plot.name.like(f"%{search}%"))
    else:
        search_type_col = literal("plot").label("type")
        q1 = db.query(
            Plot.id.label("id"), Plot.name.label("name"), search_type_col
        ).where(Plot.name.like(f"%{search}%"))
        search_type_col = literal("antenna").label("type")
        q2 = db.query(
            Antenna.id.label("id"),
            Antenna.name.label("name"),
            search_type_col,
        ).where(Antenna.name.like(f"%{search}%"))
        search_type_col = literal("station").label("type")
        q3 = db.query(
            Station.id.label("id"),
            Station.name.label("name"),
            search_type_col,
        ).where(Station.name.like(f"%{search}%"))
        query = q1.union(q2).union(q3)
    if query and request.query.sort_by:
        # print(dir(query))
        if request.query.sort_by == "id":
            if request.query.sort_dir == "desc":
                query = query.order_by(Station.id.desc())
            else:
                query = query.order_by(Station.id.asc())
        elif request.query.sort_by == "name":
            if request.query.sort_dir == "desc":
                query = query.order_by(Station.name.desc())
            else:
                query = query.order_by(Station.name.asc())
        elif request.query.sort_by == "type":
            if request.query.sort_dir == "desc":
                query = query.order_by(search_type_col.desc())
            else:
                query = query.order_by(search_type_col.asc())
    results = query.all()
    parts = {
        "search_type": search_type,
        "search": search,
        "sort_by": request.query.sort_by,
        "sort_dir": request.query.sort_dir,
        "results": results,
    }
    return template("search.html", parts)


@get("/<item_type>s")
def list_items(item_type, db):
    """Render list items page."""
    if item_type == "station":
        items = db.query(Station).all()
    elif item_type == "antenna":
        items = db.query(Antenna).all()
    elif item_type == "plot":
        items = db.query(Plot).all()
    else:
        redirect("/")
    parts = {"type": item_type, "items": items}
    return template("list.html", parts)


@get("/plot/<id:int>/generate")
def plot_generate(id, db):
    """Render the generate plot page."""
    q = db.query(Plot).filter_by(id=id)
    item = q.first()
    if item:
        utils.generate(config, item)
    redirect(f"/plot/{id}/files")


@get("/plot/<id:int>/files")
def plot_files(id, db):
    """Show available file for the current plot."""
    q = db.query(Plot).filter_by(id=id)
    item = q.first()
    files = [
        (
            os.path.basename(file),
            os.path.join(
                os.path.basename(os.path.dirname(file)), os.path.basename(file)
            ),
        )
        for file in glob.glob(f"downloads/{item.id}/*")
    ]
    grouped_files = {
        "Analysis Report": [],
        "KML": [],
        "Zip": [],
        "Image": [],
        "Other": [],
    }
    for file in files:
        if re.match(
            r".+(\.txt|\.json|_curvature|_fresnel|_fresnel60|_profile|_reference)$",
            file[0],
        ):
            grouped_files["Analysis Report"].append(file)
        elif re.match(r".+\.(kml|kmz)$", file[0]):
            grouped_files["KML"].append(file)
        elif re.match(r".+\.(zip)$", file[0]):
            grouped_files["Zip"].append(file)
        elif re.match(r".+\.(png|jpg|bmp|ppm)$", file[0]):
            grouped_files["Image"].append(file)
        else:
            grouped_files["Other"].append(file)
    # print("File Count:", len(files))
    if len(files) == 0:
        redirect(f"/plot/{id}/generate")
    parts = {
        "type": "plot",
        "item": item,
        "files": grouped_files,
        "image_type": config["convert"]["output_type"],
    }
    return template("files.html", parts)


@get("/<item_type>/<id:int>/delete")  # Delete confirmation page
@post(
    "/<item_type>/<id:int>/delete"
)  # Delete the station and redirect to stations list
def delete_item(item_type, id, db):
    """Delete item and render the item list page."""
    messages = []
    parts = {}
    if item_type == "station":
        item_class = Station
    elif item_type == "antenna":
        item_class = Antenna
    elif item_type == "plot":
        item_class = Plot
        antennas = db.query(Antenna.id.label("id"), Antenna.name.label("name")).all()
        stations = db.query(Station.id.label("id"), Station.name.label("name")).all()
        parts.update(
            {
                "antennas": antennas,
                "stations": stations,
            }
        )
    else:
        redirect("/")
    if request.method == "POST":
        # dirty_item = db.query(item_class).filter_by(id=id).first()
        dirty_item = db.query(item_class).get(id)
        name = dirty_item.name
        if (
            (
                item_type == "antenna"
                and db.query(Plot).filter_by(antenna_id=id).count() == 0
            )
            or (
                item_type == "station"
                and db.query(Plot).filter_by(station1_id=id).count() == 0
            )
            or (
                item_type == "station"
                and db.query(Plot).filter_by(station2_id=id).count() == 0
            )
        ):
            try:
                antenna_type = dirty_item.type if item_type == "antenna" else ""
                db.delete(dirty_item)
                if item_type == "antenna":
                    for f in glob.glob(
                        os.path.join("data/antennas", antenna_type, name + ".*")
                    ):
                        os.remove(f)
            except Exception as e:
                messages.append(
                    {
                        "message": e,
                        "title": f"Deleting {item_type} {name} failed.",
                        "type": "danger",
                    }
                )

            else:
                redirect(f"/{item_type}s?message=DeleteSuccessful")
        else:
            messages.append(
                {
                    "message": "Cannot delete. One or more plots depend on this item.",
                    "title": f"Deleting {item_type} {name} failed.",
                    "type": "danger",
                }
            )

    if id:
        item = db.query(item_class).filter_by(id=id).first()
    else:
        item = request.forms
    parts["item"] = item
    parts.update(
        {
            "request": request,
            "type": item_type,
            "table": item_class.__table__,
            "args": plot_args,
        }
    )
    if messages:
        parts["messages"] = messages
    return template("delete.html", parts)


@get("/<item_type>/<id:int>/<action>")  # Edit station
@post("/<item_type>/<id:int>/<action>")  # Update station and render updated edit page
@get("/<item_type>s/<action>")
@post("/<item_type>s/<action>")
def action_item(item_type, action, db, id=0):
    """Render the new item page."""
    if action not in ["new", "edit"]:
        redirect("/")
    messages = []
    parts = {}
    if item_type == "station":
        item_class = Station
    elif item_type == "antenna":
        item_class = Antenna
    elif item_type == "plot":
        item_class = Plot
        antennas = db.query(Antenna.id.label("id"), Antenna.name.label("name")).all()
        stations = db.query(Station.id.label("id"), Station.name.label("name")).all()
        parts.update(
            {
                "antennas": antennas,
                "stations": stations,
            }
        )
    else:
        redirect("/")

    if id:
        item = db.query(item_class).filter_by(id=id).first()
    else:
        item = request.forms
    parts["item"] = item

    if request.method == "POST":
        if action == "new":
            try:
                antenna_file = request.files.get("filename")
                if antenna_file:
                    original_filename, ext = os.path.splitext(antenna_file.filename)
                    if ext != ".ant":
                        raise (Exception(f"{ext} - Unsupported filetype."))
                    save_path = f"data/antennas/{request.forms.get('type')}/"
                    if not os.path.exists(save_path):
                        os.makedirs(save_path)
                    filename = request.forms.get("name") + ".ant"
                    file_path = os.path.join(save_path, filename)
                    antenna_file.save(file_path, overwrite=True)
                    utils.convert_ant_file(file_path)
                    request.forms["filename"] = filename
                # new_item = item_class(**request.forms)
                params = {}
                for col in item_class.__table__.columns:
                    value = request.forms.get(col.name)
                    if col.name in ["id", "created", "last_updated"]:
                        pass
                    elif isinstance(col.type, Boolean):
                        if value:
                            params[col.name] = True
                        else:
                            params[col.name] = False
                    elif value:
                        if isinstance(col.type, Integer):
                            params[col.name] = int(value)
                        elif isinstance(col.type, Float):
                            params[col.name] = float(value)
                        else:
                            params[col.name] = value
                new_item = item_class(**params)
                db.add(new_item)
                db.commit()

            except Exception as e:
                messages.append(
                    {"message": e, "title": f"Item creation failed.", "type": "danger"}
                )
            else:
                redirect(
                    f"/{item_type}/{new_item.id}/edit?message=ItemAddedSuccessfully"
                )
        else:
            try:
                dirty_item = db.get(item_class, id)
                for col in item_class.__table__.columns:
                    value = request.forms.get(col.name)
                    if isinstance(col.type, Boolean):
                        if value != None:
                            setattr(dirty_item, col.name, True)
                        else:
                            setattr(dirty_item, col.name, False)
                    elif value:
                        if isinstance(col.type, Integer):
                            setattr(dirty_item, col.name, int(value))
                        elif isinstance(col.type, Float):
                            setattr(dirty_item, col.name, float(value))
                        else:
                            setattr(dirty_item, col.name, value)
                # db.query(item_class).filter_by(id=id).update(request.forms)
                db.commit()
            except Exception as e:
                messages.append(
                    {"message": e, "title": f"Item update failed.", "type": "danger"}
                )

            else:
                messages.append(
                    {"message": f"Item update successful.", "type": "success"}
                )

    parts.update(
        {
            "request": request,
            "type": item_type,
            "action": action,
            "table": item_class.__table__,
            "args": plot_args,
        }
    )
    if messages:
        parts["messages"] = messages
    return template("form.html", parts)


@get("/<item_type>/<id:int>")
def view_item(item_type, id, db):
    """Render the item view page."""
    if item_type == "station":
        q = db.query(Station).filter_by(id=id)
    elif item_type == "antenna":
        q = db.query(Antenna).filter_by(id=id)
    elif item_type == "plot":
        q = db.query(Plot).filter_by(id=id)
    else:
        redirect("/")
    item = q.first()
    parts = {"type": item_type, "item": item}
    return template("view.html", parts)


@get("/clean")
def clean_generated_files():
    for file in glob.glob(f"downloads/*"):
        shutil.rmtree(file)
    redirect("/")


@get("/config")
def get_config():
    """Render the config page."""
    tools = {
        "signal-server": (
            config["signal-server"]["path"],
            True if utils.which(config["signal-server"]["path"]) else False,
        ),
        "signal-server": (
            config["signal-server"]["path"],
            True if utils.which(config["signal-server"]["path"] + "HD") else False,
        ),
        "convert": (
            config["convert"]["path"],
            True if utils.which(config["convert"]["path"]) else False,
        ),
    }
    parts = {
        "title": "Config",
        "config": config,
        "tools": tools,
        "global_args": global_args,
    }
    return template("config.html", parts)


if __name__ == "__main__":
    if os.path.isfile("config.ini"):
        try:
            config.read("config.ini")
            # Check config for required sections and items
            if "signal-server-gui" not in config:
                raise (Exception("Missing 'signalserver-gui' section in config."))
            elif "data_dir" not in config["signal-server-gui"]:
                raise (
                    Exception(
                        "Missing 'data_dir' value in 'signal-server-gui' section of config."
                    )
                )
            elif "output_dir" not in config["signal-server-gui"]:
                raise (
                    Exception(
                        "Missing 'output_dir' value in 'signal-server-gui' section of config."
                    )
                )
            elif "signal-server" not in config:
                raise (Exception("Missing 'signal-server' section in config."))
            elif "path" not in config["signal-server"]:
                raise (
                    Exception(
                        "Missing 'path' value in 'signal-server' section of config."
                    )
                )
            elif "convert" not in config:
                raise (Exception("Missing 'convert' section in config."))
            elif "path" not in config["convert"]:
                raise (
                    Exception("Missing 'path' value in 'convert' section of config.")
                )

            if "antenna_profiles_dir" not in config["signal-server"]:
                config["signal-server"]["antenna_profiles_dir"] = os.path.join(
                    config["signal-server-gui"]["data_dir"], "antennas"
                )
            if "elevation_data_dir" not in config["signal-server"]:
                config["signal-server"]["elevation_data_dir"] = os.path.join(
                    config["signal-server-gui"]["data_dir"], "elevation"
                )
            if "lidar_data_dir" not in config["signal-server"]:
                config["signal-server"]["lidar_data_dir"] = os.path.join(
                    config["signal-server-gui"]["data_dir"], "lidar"
                )
            if "user_data_dir" not in config["signal-server"]:
                config["signal-server"]["user_data_dir"] = os.path.join(
                    config["signal-server-gui"]["data_dir"], "user"
                )
            if "clutter_data_dir" not in config["signal-server"]:
                config["signal-server"]["clutter_data_dir"] = os.path.join(
                    config["signal-server-gui"]["data_dir"], "clutter"
                )
            if "color_profiles_dir" not in config["signal-server"]:
                config["signal-server"]["color_profiles_dir"] = os.path.join(
                    config["signal-server-gui"]["data_dir"], "color_profiles"
                )
            if "color_profile" not in config["signal-server"]:
                config["signal-server"]["color_profile"] = os.path.join(
                    config["signal-server"]["color_profiles_dir"], "rainbow.dcf"
                )
        except Exception as e:
            print(
                "Invalid config.ini, Missing mandatory settings. Exiting...",
                e,
            )
            exit()
    else:
        print("No config.ini preset. Exiting...")
        exit()
    run(host="localhost", port=8080, reloader=True, debug=True)
