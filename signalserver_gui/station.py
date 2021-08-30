"""Module contains declarative Station class for database."""
from datetime import datetime
from sqlalchemy import (
    Column,
    DateTime,
    Float,
    Integer,
    String,
)
from sqlalchemy.orm import relationship
from signalserver_gui import Base


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
    # plots_as_station1 = relationship("Plot", backref="station1")
    # plots_as_station2 = relationship("Plot", backref="station2")

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
