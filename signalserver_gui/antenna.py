"""Module contains declarative Antenna class for database."""
from datetime import datetime
from sqlalchemy import (
    Column,
    DateTime,
    Float,
    Integer,
    String,
)
from sqlalchemy.orm import declarative_base

Base = declarative_base()


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
