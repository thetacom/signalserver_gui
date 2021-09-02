"""Module loads signalserver_gui.db with test sites and plots."""
import configparser
import os

from signalserver_gui import model
from signalserver_gui.antenna import Antenna
from signalserver_gui.station import Station
from signalserver_gui.plot import Plot

config = configparser.ConfigParser()


def load_test_data(db):
    """Insert test stations and plots into database."""
    test_items = [
        {
            "type": "station",
            "columns": {
                "name": "TEST1_groundlevel",
                "latitude": 51.5,
                "longitude": -0.5,
                "height": 1,
            },
        },
        {
            "type": "station",
            "columns": {
                "name": "Close_to_TEST1_groundlevel",
                "latitude": 51.35,
                "longitude": -0.34,
                "height": 10,
            },
        },
        {
            "type": "station",
            "columns": {
                "name": "TEST2_height_25",
                "latitude": 51.5,
                "longitude": -0.5,
                "height": 25,
            },
        },
        {
            "type": "station",
            "columns": {
                "name": "Aerial_Test",
                "latitude": 51.5,
                "longitude": -0.5,
                "height": 1000,
            },
        },
        {
            "type": "station",
            "columns": {
                "name": "TEST WITH SPACES",
                "latitude": 50.5,
                "longitude": -1.5,
                "height": 1,
            },
        },
        {
            "type": "station",
            "columns": {
                "name": "TEST2",
                "latitude": 53.5,
                "longitude": -10.5,
                "height": 1,
            },
        },
        {
            "type": "station",
            "columns": {
                "name": "TEST3",
                "latitude": 52.5,
                "longitude": 10.5,
                "height": 50,
            },
        },
        {
            "type": "station",
            "columns": {
                "name": "TEST4",
                "latitude": 51.5,
                "longitude": -20.5,
                "height": 50,
            },
        },
        {
            "type": "plot",
            "columns": {
                "name": "Generic_Dipole_Plot_TEST1",
                "frequency": 400,
                "radius": 25,
                "station1_id": 1,
                "station2_id": 2,
                "antenna_id": 1,
            },
        },
        {
            "type": "plot",
            "columns": {
                "name": "Generic_Dipole_Plot_TEST1_opacity_half",
                "frequency": 500,
                "radius": 25,
                "station1_id": 1,
                "station2_id": 2,
                "antenna_id": 1,
                "opacity": 0.5,
            },
        },
        {
            "type": "plot",
            "columns": {
                "name": "Generic_Dipole_Plot_TEST2",
                "frequency": 600,
                "radius": 25,
                "station1_id": 2,
                "station2_id": 1,
                "antenna_id": 1,
            },
        },
        {
            "type": "plot",
            "columns": {
                "name": "Generic_Dipole_Plot_TEST3",
                "frequency": 600,
                "radius": 25,
                "station1_id": 1,
                "station2_id": 2,
                "antenna_id": 1,
                "do_p2p_analysis": True,
            },
        },
        {
            "type": "plot",
            "columns": {
                "name": "Generic_Dipole_Plot_PM2-LOS",
                "propagation_model": 2,
                "propagation_mode": 1,
                "frequency": 700,
                "radius": 25,
                "station1_id": 2,
                "station2_id": 1,
                "antenna_id": 1,
                "opacity": 1.0,
            },
        },
        {
            "type": "plot",
            "columns": {
                "name": "Generic_Dipole_Plot_PM2-LOS2",
                "propagation_model": 2,
                "propagation_mode": 1,
                "frequency": 700,
                "radius": 25,
                "station1_id": 1,
                "station2_id": 2,
                "antenna_id": 1,
                "opacity": 1.0,
            },
        },
        {
            "type": "plot",
            "columns": {
                "name": "Generic_Dipole_Plot_PM3-Hata",
                "propagation_model": 3,
                "propagation_mode": 1,
                "frequency": 700,
                "radius": 25,
                "station1_id": 1,
                "station2_id": 2,
                "antenna_id": 1,
                "opacity": 1.0,
            },
        },
        {
            "type": "plot",
            "columns": {
                "name": "Generic_Dipole_Plot_PM4-ECC33",
                "propagation_model": 4,
                "propagation_mode": 1,
                "frequency": 700,
                "radius": 25,
                "station1_id": 1,
                "station2_id": 2,
                "antenna_id": 1,
                "opacity": 1.0,
            },
        },
        {
            "type": "plot",
            "columns": {
                "name": "Generic_Dipole_Plot_PM5-SUI",
                "propagation_model": 5,
                "propagation_mode": 1,
                "frequency": 700,
                "radius": 25,
                "station1_id": 1,
                "station2_id": 2,
                "antenna_id": 1,
                "opacity": 1.0,
            },
        },
        {
            "type": "plot",
            "columns": {
                "name": "Generic_Dipole_Plot_PM6-COST-Hata",
                "propagation_model": 6,
                "propagation_mode": 1,
                "frequency": 700,
                "radius": 25,
                "station1_id": 1,
                "station2_id": 2,
                "antenna_id": 1,
                "opacity": 1.0,
            },
        },
        {
            "type": "plot",
            "columns": {
                "name": "Generic_Dipole_Plot_PM7-FSPL",
                "propagation_model": 7,
                "propagation_mode": 1,
                "frequency": 700,
                "radius": 25,
                "station1_id": 1,
                "station2_id": 2,
                "antenna_id": 1,
                "opacity": 1.0,
            },
        },
        {
            "type": "plot",
            "columns": {
                "name": "Generic_Dipole_Plot_PM8-ITWOM",
                "propagation_model": 8,
                "propagation_mode": 1,
                "frequency": 700,
                "radius": 25,
                "station1_id": 1,
                "station2_id": 2,
                "antenna_id": 1,
                "opacity": 1.0,
            },
        },
        {
            "type": "plot",
            "columns": {
                "name": "Generic_Dipole_Plot_PM9-Ericsson",
                "propagation_model": 9,
                "propagation_mode": 1,
                "frequency": 700,
                "radius": 25,
                "station1_id": 1,
                "station2_id": 2,
                "antenna_id": 1,
                "opacity": 1.0,
            },
        },
        {
            "type": "plot",
            "columns": {
                "name": "Generic_Dipole_Plot_PM10-Plane",
                "propagation_model": 10,
                "propagation_mode": 1,
                "frequency": 700,
                "radius": 25,
                "station1_id": 1,
                "station2_id": 2,
                "antenna_id": 1,
                "opacity": 1.0,
            },
        },
        {
            "type": "plot",
            "columns": {
                "name": "Generic_Dipole_Plot_PM11-Egli",
                "propagation_model": 11,
                "propagation_mode": 1,
                "frequency": 700,
                "radius": 25,
                "station1_id": 1,
                "station2_id": 2,
                "antenna_id": 1,
                "opacity": 1.0,
            },
        },
        {
            "type": "plot",
            "columns": {
                "name": "Generic_Dipole_Plot_PM12-Soil",
                "propagation_model": 12,
                "propagation_mode": 1,
                "frequency": 700,
                "radius": 25,
                "station1_id": 1,
                "station2_id": 2,
                "antenna_id": 1,
                "opacity": 1.0,
            },
        },
        {
            "type": "plot",
            "columns": {
                "name": "Generic_Dipole_Plot_Aerial",
                "frequency": 800,
                "radius": 50,
                "station1_id": 2,
                "station2_id": 3,
                "antenna_id": 1,
                "opacity": 0.5,
            },
        },
        {
            "type": "plot",
            "columns": {
                "name": "DB413-B_Plot",
                "use_dbm": True,
                "frequency": 900,
                "radius": 50,
                "station1_id": 1,
                "station2_id": 2,
                "antenna_id": 2,
                "opacity": 1.0,
            },
        },
        {
            "type": "plot",
            "columns": {
                "name": "Generic_Yagi_Plot_PM2-LOS",
                "propagation_model": 2,
                "frequency": 1000,
                "station1_id": 2,
                "station2_id": 1,
                "antenna_id": 3,
                "opacity": 0.75,
            },
        },
        {
            "type": "plot",
            "columns": {
                "name": "Generic_Cardio_Plot",
                "frequency": 1100,
                "station1_id": 1,
                "station2_id": 2,
                "antenna_id": 4,
            },
        },
        {
            "type": "plot",
            "columns": {
                "name": "Generic_Ellipse_Plot",
                "frequency": 1200,
                "station1_id": 1,
                "station2_id": 2,
                "antenna_id": 5,
            },
        },
    ]
    for item in test_items:
        pass
        if item["type"] == "antenna":
            new_row = Antenna(**item["columns"])
        elif item["type"] == "station":
            new_row = Station(**item["columns"])
        else:
            new_row = Plot(**item["columns"])
        db.add(new_row)
    db.commit()


if __name__ == "__main__":
    try:
        if os.path.isfile("config.ini"):
            config.read("config.ini")
            # Check config for required sections and items
            if "signalservergui" not in config:
                raise (
                    Exception("Missing required 'signalserver-gui' section in config.")
                )
            elif "database_dir" not in config["signalservergui"]:
                raise (
                    Exception(
                        "Missing required 'database_dir' value in 'signalservergui' section of config."
                    )
                )
        else:
            raise (Exception("Missing config file (config.ini)."))

    except Exception as e:
        print(e)
        exit()
    db_file = os.path.join(
        config["signalservergui"]["database_dir"], "signalserver_gui.db"
    )
    db = model.db_file_init(db_file)
    load_test_data(db)
