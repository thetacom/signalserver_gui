"""Module contains declarative class definitions for database."""
# TODO(Justin): Clean up unused imports.
from datetime import datetime
import os
from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    Sequence,
    String,
    Text,
    create_engine,
    event,
    literal,
)
from sqlalchemy.orm import declarative_base, foreign, mapper, relationship, sessionmaker

Base = declarative_base()


def _fk_pragma_on_connect(dbapi_con, con_record):
    """Add database hook to enable foreign keys."""
    dbapi_con.execute("pragma foreign_keys=ON")


def init(db_path: str):
    """Initialize the sqlite database engine."""
    db_file = os.path.join(db_path, "signalserver_gui.db")
    engine = create_engine(f"sqlite:///{db_file}", echo=False)
    event.listen(engine, "connect", _fk_pragma_on_connect)
    return engine


class Antenna(Base):
    """Class representing an entry in the database's Antenna table."""

    __tablename__ = "antennas"
    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=True, nullable=False)
    filename = Column(String(50), nullable=False)
    type = Column(String(50), nullable=False)
    rx_gain = Column(Float, default=0.0)
    rx_threshhold = Column(Float, default=0.0)
    created = Column(DateTime, default=datetime.now)
    last_updated = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    def __init__(self, name, filename, type, rx_gain=0.0, rx_threshhold=0.0):
        """Initialize a new Antenna instance."""
        self.name = name
        self.filename = filename
        self.rx_gain = rx_gain
        self.rx_threshhold = rx_threshhold
        self.type = type

    def __repr__(self):
        """Return a string representation of an Antena instance."""
        if self.id:
            return f"<Antenna({self.id:d}, '{self.name:s}')>"
        else:
            return f"<Antenna(New, '{self.name:s}')>"


class Station(Base):
    """Class representing an entry in the database's Station table."""

    __tablename__ = "stations"
    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=True, nullable=False)
    latitude = Column(Float, default=0.00, nullable=False)
    longitude = Column(Float, default=0.00, nullable=False)
    height = Column(Float, default=1, nullable=False)
    geography = Column(String(50), default="north america", nullable=False)
    state = Column(String(50), default="n/a", nullable=False)
    polarization = Column(String(10), default="vertical", nullable=False)
    rotation = Column(Float, default=0.0, nullable=False)
    downtilt = Column(Float, default=0.0, nullable=False)
    downtilt_direction = Column(Float, default=0.0, nullable=False)
    created = Column(DateTime, default=datetime.now)
    last_updated = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    def __init__(
        self,
        name,
        latitude=0.0,
        longitude=0.0,
        height=30,
        geography="North Americal",
        state="N/A",
        polarization="vertical",
        rotation=0.0,
        downtilt=0.0,
        downtilt_direction=0.0,
    ):
        """Initialize a new Station instance."""
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.height = height
        self.geography = geography
        self.state = state
        self.polarization = polarization
        self.rotation = rotation
        self.downtilt = downtilt
        self.downtilt_direction = downtilt_direction

    def __repr__(self):
        """Return a string representation of a Station instance."""
        if self.id:
            return f"<Station('{self.id:d}', '{self.name:s}')>"
        else:
            return f"<Station(New, '{self.name:s}')>"


class Plot(Base):
    """Class representing an entry in the database's Plot table."""

    __tablename__ = "plots"
    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=True, nullable=False)
    do_p2p_analysis = Column(Boolean, default=False, nullable=False)
    use_metric_units = Column(Boolean, default=False, nullable=False)
    use_lidar = Column(Boolean, default=False, nullable=False)
    use_udt = Column(Boolean, default=False, nullable=False)
    use_dbm = Column(Boolean, default=False, nullable=False)
    use_knife_edge_diffraction = Column(Boolean, default=False, nullable=False)
    frequency = Column(Float, nullable=False)
    opacity = Column(Float, default=1.0, nullable=False)
    effective_radiated_power = Column(Float, default=0.0, nullable=False)
    ground_clutter = Column(Float)
    resample_reduction_factor = Column(Integer)
    terrain_code = Column(Integer)
    terrain_dialectric = Column(Float)
    terrain_conductivity = Column(Float)
    climate_code = Column(Integer)
    itm_reliability = Column(Integer)
    itm_confidence = Column(Integer)
    radius = Column(Integer, default=25, nullable=False)
    resolution = Column(Integer, default=600, nullable=False)
    propagation_model = Column(Integer)
    propagation_mode = Column(Integer)
    antenna_id = Column(Integer, ForeignKey("antennas.id"), nullable=False)
    station1_id = Column(Integer, ForeignKey("stations.id"), nullable=False)
    station2_id = Column(
        Integer,
        ForeignKey("stations.id"),
        CheckConstraint("station1_id != station2_id"),
        nullable=True,
    )
    antenna = relationship("Antenna", foreign_keys=[antenna_id])
    station1 = relationship("Station", foreign_keys=[station1_id])
    station2 = relationship("Station", foreign_keys=[station2_id])
    created = Column(DateTime, default=datetime.now)
    last_updated = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    def __init__(
        self,
        name,
        frequency,
        antenna_id,
        station1_id,
        station2_id=None,
        do_p2p_analysis=False,
        use_metric_units=False,
        use_lidar=False,
        use_udt=False,
        use_dbm=False,
        use_knife_edge_diffraction=False,
        opacity=1.0,
        effective_radiated_power=0.0,
        radius=25,
        propagation_model=None,
        propagation_mode=None,
        terrain_code=None,
        terrain_dialectric=None,
        terrain_conductivity=None,
        climate_code=None,
        itm_reliability=None,
        itm_confidence=None,
        resolution=None,
        ground_clutter=None,
        resample_reduction_factor=None,
    ):
        """Initialize a new Plot instance."""
        self.name = name
        self.do_p2p_analysis = do_p2p_analysis
        self.use_metric_units = use_metric_units
        self.use_lidar = use_lidar
        self.use_udt = use_udt
        self.use_dbm = use_dbm
        self.use_knife_edge_diffraction = use_knife_edge_diffraction
        self.opacity = opacity
        self.effective_radiated_power = effective_radiated_power
        self.frequency = frequency
        self.radius = radius
        self.resolution = resolution
        self.propagation_model = propagation_model
        self.propagation_mode = propagation_mode
        self.terrain_code = terrain_code
        self.terrain_dialectric = terrain_dialectric
        self.terrain_conductivity = terrain_conductivity
        self.climate_code = climate_code
        self.itm_reliability = itm_reliability
        self.itm_confidence = itm_confidence
        self.ground_clutter = ground_clutter
        self.resample_reduction_factor = resample_reduction_factor
        self.antenna_id = antenna_id
        self.station1_id = station1_id
        self.station2_id = station2_id

    def __repr__(self):
        """Return a string representation of a Plot instance."""
        if self.id:
            return f"<Plot('{self.id:d}', '{self.name:s}')>"
        else:
            return f"<Plot(New, '{self.name:s}')>"

    def rf_units(self):
        """Return appropriate RF units depending on plot configuration."""
        # TODO(Justin): Refactor unit handling into separate module.
        if self.use_dbm:
            return "dBm"
        else:
            return "dBuV/m"

    def distance_units(self):
        """Return appropriate distance units depending on plot configuration."""
        # TODO(Justin): Refactor unit handling into separate module.
        if self.use_metric_units:
            return "m"
        else:
            return "ft"


# Map all global parameters to their various attributes.
global_args = {
    "terrain_greyscale": {
        "flag": "-t",
        "type": bool,
        "depends": None,
        "hint": "Terrain greyscale background",
    },
    "debug": {
        "flag": "-dbg",
        "type": bool,
        "depends": None,
        "hint": "Verbose debug messages",
    },
    "normalize": {
        "flag": "-ng",
        "type": bool,
        "depends": ["do_p2p_analysis"],
        "hint": "Normalise Path Profile graph",
    },
    "halve": {
        "flag": "-haf",
        "type": int,
        "depends": None,
        "hint": "Halve 1 or 2 (optional)",
    },
    "nothreads": {
        "flag": "-nothreads",
        "type": bool,
        "depends": None,
        "hint": "Turn off threaded processing",
    },
    "elevation_data_dir": {
        "flag": "-sdf",
        "type": str,
        "depends": None,
        "hint": "Directory containing SRTM derived .sdf DEM tiles (may be .gz or .bz2).",
    },
    "lidar_data_dir": {
        "flag": "-lid",
        "type": str,
        "depends": ["use_lidar"],
        "hint": "ASCII grid tile (LIDAR) with dimensions and resolution defined in header.",
    },
    "user_data_dir": {
        "flag": "-udt",
        "type": str,
        "depends": ["use_udt"],
        "hint": "User defined point clutter as decimal co-ordinates: 'latitude,longitude,height'.",
    },
    "clutter_data_files": {
        "flag": "-clt",
        "type": str,
        "depends": None,
        "hint": "MODIS 17-class wide area clutter in ASCII grid format.",
    },
    #    "color_profile": {
    #        "flag": "-color",
    #        "type": str,
    #        "depends": None,
    #        "hint": "File to pre-load .scf/.lcf/.dcf for Signal/Loss/dBm color palette.",
    #    },
}

# Map all plot related parameters to their various attributes.
plot_args = {
    "plot": {
        "id": {
            "flag": None,
            "depends": None,
            "hint": "Auto assigned upon creation.",
            "form": {"type": "ignore"},
        },
        "created": {
            "flag": None,
            "depends": None,
            "hint": "Auto assigned upon creation.",
            "form": {"type": "ignore"},
        },
        "last_updated": {
            "flag": None,
            "depends": None,
            "hint": "Auto update upon modification.",
            "form": {"type": "ignore"},
        },
        "name": {
            "flag": None,
            "depends": None,
            "hint": "Must be unique and at least 11 characters long.",
            "form": {
                "type": "text",
                "parameters": {"placeholder": "Plot Name", "required": True},
            },
        },
        "antenna_id": {
            "flag": None,
            "depends": None,
            "hint": "Antenna profile to use for Station 1 and Station 2. (Required).",
            "form": {
                "type": "select_item",
                "select_type": "antenna",
                "parameters": {"required": True},
            },
        },
        "station1_id": {
            "flag": None,
            "depends": None,
            "hint": "Transmitter station (Required).",
            "form": {
                "type": "select_item",
                "select_type": "station",
                "parameters": {"required": True},
            },
        },
        "station2_id": {
            "flag": None,
            "depends": None,
            "hint": "Receiver station (Required for p2p analysis).",
            "form": {
                "type": "select_item",
                "select_type": "station",
                "parameters": {"required": False},
            },
        },
        "do_p2p_analysis": {
            "flag": None,
            "depends": None,
            "hint": "Also perform point to point analysis.",
            "form": {
                "type": "checkbox",
                "parameters": {"default": False, "required": True},
            },
        },
        "use_metric_units": {
            "flag": "-m",
            "depends": None,
            "hint": "Use metric units in leiu of imperial units for distance measurements.",
            "form": {
                "type": "checkbox",
                "parameters": {"default": False, "required": True},
            },
        },
        "use_lidar": {
            "flag": None,
            "depends": None,
            "hint": "Include lidar options.",
            "form": {
                "type": "checkbox",
                "parameters": {"default": False, "required": True},
            },
        },
        "use_udt": {
            "flag": None,
            "depends": None,
            "hint": "Include user data options.",
            "form": {
                "type": "checkbox",
                "parameters": {"default": False, "required": True},
            },
        },
        "use_dbm": {
            "flag": "-dbm",
            "depends": None,
            "hint": "Plot Rxd signal power instead of field strength in dBuV/m",
            "form": {
                "type": "checkbox",
                "parameters": {"default": False, "required": True},
            },
        },
        "use_knife_edge_diffraction": {
            "flag": "-ked",
            "depends": None,
            "hint": "Knife edge diffraction (Already on for ITM)",
            "form": {
                "type": "checkbox",
                "parameters": {"default": False, "required": True},
            },
        },
        "opacity": {
            "flag": None,
            "depends": None,
            "hint": "Opacity of plot image (0.0-1.0).",
            "form": {
                "type": "range",
                "parameters": {
                    "min": 0.05,
                    "max": 1.0,
                    "step": 0.05,
                    "default": 1,
                    "required": True,
                },
            },
        },
        "effective_radiated_power": {
            "flag": "-erp",
            "depends": None,
            "hint": "Tx Total Effective Radiated Power in Watts (dBd) inc Tx+Rx gain. 2.14dBi = 0dBd",
            "form": {
                "type": "range",
                "parameters": {
                    "min": 1,
                    "max": 100000,
                    "step": 1,
                    "default": 10,
                    "units": "Watts",
                    "required": True,
                },
            },
        },
        "frequency": {
            "flag": "-f",
            "depends": None,
            "hint": "Tx Frequency (MHz) 20MHz to 100GHz (LOS after 20GHz).",
            "form": {
                "type": "text",
                "parameters": {
                    "placeholder": "20 - 100000",
                    "units": "MHz",
                    "required": True,
                },
            },
        },
        "radius": {
            "flag": "-R",
            "depends": None,
            "hint": "Radius (Units depended on the 'use_metric' option)",
            "form": {
                "type": "range",
                "parameters": {
                    "min": 5,
                    "max": 75,
                    "step": 5,
                    "default": 25,
                    "units": "miles/kilometers",
                    "required": True,
                },
            },
        },
        "resolution": {
            "flag": "-res",
            "depends": None,
            "hint": "Pixels per tile. 300/600/1200/3600 (Optional. LIDAR res is within the tile)",
            "form": {
                "type": "select",
                "parameters": {
                    "options": [300, 600, 1200, 3600],
                    "default": 1200,
                    "required": True,
                },
            },
        },
        "propagation_model": {
            "flag": "-pm",
            "depends": None,
            "hint": "Propagation model. 1: ITM, 2: LOS, 3: Hata, 4: ECC33, 5: SUI, 6: COST-Hata, 7: FSPL, 8: ITWOM, 9: Ericsson, 10: Plane earth, 11: Egli VHF/UHF, 12: Soil",
            "form": {
                "type": "select_tuple",
                "parameters": {
                    "options": [
                        ("", "none"),
                        (1, "itm"),
                        (2, "los"),
                        (3, "hata"),
                        (4, "ecc33"),
                        (5, "sui"),
                        (6, "cost hata"),
                        (7, "fspl"),
                        (8, "itwom"),
                        (9, "ericsson"),
                        (10, "plane earth"),
                        (11, "egli vhf/uhf"),
                        (12, "soil"),
                    ],
                    "default": "1",
                },
            },
        },
        "propagation_mode": {
            "flag": "-pe",
            "depends": None,
            "hint": "Propagation model mode: 1:Urban, 2:Suburban, 3:Rural",
            "form": {
                "type": "select_tuple",
                "parameters": {
                    "options": [
                        ("", "none"),
                        (1, "urban"),
                        (2, "suburban"),
                        (3, "rural"),
                    ]
                },
            },
        },
        "terrain_code": {
            "flag": "-te",
            "depends": None,
            "hint": "Terrain code 1-6 (optional - 1. Water, 2. Marsh, 3. Farmland, 4. Mountain, 5. Desert, 6. Urban",
            "form": {
                "type": "select_tuple",
                "parameters": {
                    "options": [
                        ("", "none"),
                        (1, "water"),
                        (2, "marsh"),
                        (3, "farmland"),
                        (4, "mountain"),
                        (5, "desert"),
                        (6, "urban"),
                    ]
                },
            },
        },
        "terrain_dialectric": {
            "flag": "-terdic",
            "depends": None,
            "hint": "Terrain dielectric value 2-80 (optional)",
            "form": {
                "type": "range",
                "parameters": {"min": 2, "max": 80, "step": 1, "default": 2},
            },
        },
        "terrain_conductivity": {
            "flag": "-tercon",
            "depends": None,
            "hint": "Terrain conductivity 0.01-0.0001 (optional)",
            "form": {
                "type": "range",
                "parameters": {
                    "min": 0.0001,
                    "max": 0.01,
                    "step": 0.0001,
                    "required": False,
                    "default": 0.0001,
                },
            },
        },
        "climate_code": {
            "flag": "-cl",
            "depends": None,
            "hint": "Climate code 1-7 (optional - 1. Equatorial 2. Continental subtropical 3. Maritime subtropical 4. Desert 5. Continental temperate 6. Maritime temperate (Land) 7. Maritime temperate (Sea)",
            "form": {
                "type": "select_tuple",
                "parameters": {
                    "options": [
                        ("", "none"),
                        (1, "equatorial"),
                        (2, "continental subtropical"),
                        (3, "maritime subtropical"),
                        (4, "desert"),
                        (5, "continental temperate"),
                        (6, "maritime temperate (land)"),
                        (7, "maritime temperate (sea)"),
                    ]
                },
            },
        },
        "itm_reliability": {
            "flag": "-rel",
            "depends": None,
            "hint": "Reliability for ITM model (% of 'time') 1 to 99 (optional, default 50%)",
            "form": {
                "type": "range",
                "parameters": {
                    "min": 1,
                    "max": 99,
                    "step": 1,
                    "default": 50,
                    "units": "%",
                },
            },
        },
        "itm_confidence": {
            "flag": "-conf",
            "depends": None,
            "hint": "Confidence for ITM model (% of 'situations') 1 to 99 (optional, default 50%)",
            "form": {
                "type": "range",
                "parameters": {
                    "min": 1,
                    "max": 99,
                    "step": 1,
                    "default": 50,
                    "units": "%",
                },
            },
        },
        "ground_clutter": {
            "flag": "-gc",
            "depends": None,
            "hint": "Random ground clutter (Units depend on the 'use_metric' option).",
            "form": {
                "type": "text",
                "parameters": {
                    "placeholder": "0",
                    "units": "feet/meters",
                    "required": False,
                },
            },
        },
        "resample_reduction_factor": {
            "flag": "-resample",
            "depends": ["use_lidar"],
            "hint": "Reduce Lidar resolution by specified factor (2 : 50%)",
            "form": {
                "type": "range",
                "parameters": {
                    "min": 1,
                    "max": 8,
                    "step": 1,
                    "default": 1,
                    "units": "x",
                },
            },
        },
    },
    "antenna": {
        "id": {
            "flag": None,
            "depends": None,
            "hint": "Auto assigned upon creation.",
            "form": {"type": "ignore"},
        },
        "created": {
            "flag": None,
            "depends": None,
            "hint": "Auto assigned upon creation.",
            "form": {"type": "ignore"},
        },
        "last_updated": {
            "flag": None,
            "depends": None,
            "hint": "Auto update upon modification.",
            "form": {"type": "ignore"},
        },
        "name": {
            "flag": "",
            "depends": None,
            "hint": "Must be unique and at least 11 characters long.",
            "form": {
                "type": "text",
                "parameters": {"placeholder": "ABC-123v(4)", "required": True},
            },
        },
        "type": {
            "flag": None,
            "depends": None,
            "hint": "Antenna style.",
            "form": {
                "type": "select",
                "parameters": {
                    "options": [
                        "cardio",
                        "corner",
                        "dipole",
                        "ellipse",
                        "ground",
                        "mobile",
                        "panel",
                        "yagi",
                    ],
                    "default": "dipole",
                },
            },
        },
        "rx_gain": {
            "flag": "-rxg",
            "depends": ["do_p2p_analysis"],
            "hint": "Rx gain dBd (optional for PPA text report)",
            "form": {
                "type": "range",
                "parameters": {
                    "min": 0,
                    "max": 120,
                    "step": 3,
                    "default": 0,
                    "units": "dB",
                },
            },
        },
        "rx_threshhold": {
            "flag": "-rt",
            "depends": None,
            "hint": "Rx Threshold (dB / dBm / dBuV/m)",
            "form": {
                "type": "range",
                "parameters": {
                    "min": -120,
                    "max": 0,
                    "step": 3,
                    "default": 0,
                    "units": "dBm",
                },
            },
        },
        "filename": {
            "flag": "-ant",
            "depends": None,
            "hint": "Antenna pattern file (.ant) converted to .az and .el files on upload.",
            "form": {
                "type": "file",
                "parameters": {"accept": ".ant", "required": True},
            },
        },
    },
    "station": {
        "id": {
            "flag": None,
            "depends": None,
            "hint": "Auto assigned upon creation.",
            "form": {"type": "ignore"},
        },
        "created": {
            "flag": None,
            "depends": None,
            "hint": "Auto assigned upon creation.",
            "form": {"type": "ignore"},
        },
        "last_updated": {
            "flag": None,
            "depends": None,
            "hint": "Auto update upon modification.",
            "form": {"type": "ignore"},
        },
        "name": {
            "flag": "",
            "depends": None,
            "hint": "Must be unique and at least 11 characters long.",
            "form": {
                "type": "text",
                "parameters": {"placeholder": "Station123", "required": True},
            },
        },
        "geography": {
            "flag": None,
            "depends": None,
            "hint": "The country the station physically resides in if outside the United States.",
            "form": {
                "type": "select",
                "parameters": {
                    "options": [
                        "north america",
                        "central america",
                        "south america",
                        "europe",
                        "africa",
                        "asia",
                        "caribbean",
                        "oceania",
                    ]
                },
                "default": "north america",
            },
        },
        "state": {
            "flag": None,
            "depends": None,
            "hint": "The State the station physically resides in.",
            "form": {
                "type": "select",
                "parameters": {
                    "options": ["n/a", "alabama", "alaska", "arizona", "arkansas"]
                },
            },
        },
        "latitude": {
            "flag": "-lat",
            "depends": None,
            "hint": "Station latitude (decimal degrees) -70/+70",
            "form": {
                "type": "range",
                "parameters": {"min": -70, "max": 70, "step": 0.01, "default": 0.00},
            },
        },
        "longitude": {
            "flag": "-lon",
            "depends": None,
            "hint": "Station longitude (decimal degrees) -180/+180",
            "form": {
                "type": "range",
                "parameters": {"min": -180, "max": 180, "step": 0.01, "default": 0.00},
            },
        },
        "height": {
            "flag": "-txh",
            "depends": None,
            "hint": "Tx Height (above ground)",
            "form": {
                "type": "text",
                "parameters": {
                    "placeholder": "Height AGL",
                    "required": True,
                    "default": 1,
                },
            },
        },
        "polarization": {
            "flag": "-hp",
            "depends": None,
            "hint": "Horizontal Polarisation (default=vertical)",
            "form": {
                "type": "select",
                "parameters": {
                    "options": ["horizontal", "vertical"],
                    "default": "vertical",
                },
            },
        },
        "rotation": {
            "flag": "-rot",
            "depends": None,
            "hint": "(  0.0 - 359.0 degrees, default 0.0) Antenna Pattern Rotation",
            "form": {
                "type": "range",
                "parameters": {"min": 0, "max": 359, "step": 0.1, "default": 0.0},
            },
        },
        "downtilt": {
            "flag": "-dt",
            "depends": None,
            "hint": "( -10.0 - 90.0 degrees, default 0.0) Antenna Downtilt",
            "form": {
                "type": "range",
                "parameters": {"min": -10, "max": 90, "step": 0.1, "default": 0.0},
            },
        },
        "downtilt_direction": {
            "flag": "-dtdir",
            "depends": None,
            "hint": "( 0.0 - 359.0 degrees, default 0.0) Antenna Downtilt Direction",
            "form": {
                "type": "range",
                "parameters": {"min": 0, "max": 359, "step": 0.1, "default": 0.0},
            },
        },
        "rx_height": {
            "flag": "-rxh",
            "depends": ["do_p2p_analysis"],
            "hint": "Rx height above ground (optional. Default=1)",
            "form": {"type": "ignore"},
        },
        "rx_latitude": {
            "flag": "-rla",
            "depends": ["do_p2p_analysis"],
            "hint": "Rx Latitude for PPA (decimal degrees) -70/+70",
            "form": {"type": "ignore"},
        },
        "rx_longitude": {
            "flag": "-rlo",
            "depends": ["do_p2p_analysis"],
            "hint": "Rx Longitude for PPA (decimal degrees) -180/+180",
            "form": {"type": "ignore"},
        },
    },
}
