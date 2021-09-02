import configparser
import os

from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker

from signalserver_gui.antenna import Antenna, Base

config = configparser.ConfigParser()


def _fk_pragma_on_connect(dbapi_con, con_record):
    dbapi_con.execute("pragma foreign_keys=ON")







if __name__ == "__main__":
    if os.path.isfile("config.ini"):
        try:
            config.read("config.ini")
        except:
            print("Error parsing config.")
    db_file_init()
