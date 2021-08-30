"""Module contains declarative Plot class for database."""
from datetime import datetime
from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import declarative_base, foreign, relationship

Base = declarative_base()


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
