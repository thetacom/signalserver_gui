"""This module contains the Site class."""
from typing import Union


class Site:
    """The AnalysisReport Site class."""

    units = {
        "distance": {
            "imperial": [("ft", "foot", "feet"), ("mi", "mile", "miles")],
            "metric": [("m", "meter", "meters"), ("km", "kilometer", "kilometers")],
        }
    }

    def __init__(
        self,
        site,
        longitude=0.0,
        latitude=0.0,
        elevation=0.0,
        height=0.0,
        distance=0.0,
        azimuth=0.0,
        downtilt=0.0,
        use_metric=False,
    ):
        """Initialize a new Site instance."""
        self.site = site
        self.longitude = longitude
        self.latitude = latitude
        self.elevation = elevation
        self.height = height
        self.distance = distance
        self.azimuth = azimuth
        self.downtilt = downtilt
        self.use_metric = use_metric

    @property
    def use_metric(self) -> bool:
        """Getter/Setter for free_space_path_loss property."""
        return self._use_metric

    @use_metric.setter
    def use_metric(self, new_value: bool = True) -> None:
        self._use_metric = new_value

    @property
    def site(self) -> str:
        """Getter/Setter for site property."""
        return self._site

    @site.setter
    def site(self, new_value: str) -> None:
        self._site = new_value

    @property
    def longitude(self) -> float:
        """Getter/Setter for longitude property."""
        return self._longitude

    @longitude.setter
    def longitude(self, new_value: float) -> None:
        self._longitude = new_value

    @property
    def latitude(self) -> float:
        """Getter/Setter for latitude property."""
        return self._latitude

    @latitude.setter
    def latitude(self, new_value: float) -> None:
        self._latitude = new_value

    @property
    def elevation(self) -> float:
        """Getter/Setter for elevation property."""
        return self._elevation

    @elevation.setter
    def elevation(self, new_value: float) -> None:
        self._elevation = new_value

    @property
    def height(self) -> float:
        """Getter/Setter for height property."""
        return self._height

    @height.setter
    def height(self, new_value: float) -> None:
        self._height = new_value

    @property
    def distance(self) -> float:
        """Getter/Setter for distance property."""
        return self._distance

    @distance.setter
    def distance(self, new_value: float) -> None:
        self._distance = new_value

    @property
    def azimuth(self) -> float:
        """Getter/Setter for azimuth property."""
        return self._azimuth

    @azimuth.setter
    def azimuth(self, new_value: float) -> None:
        self._azimuth = new_value

    @property
    def downtilt(self) -> float:
        """Getter/Setter for downtilt property."""
        return self._downtilt

    @downtilt.setter
    def downtilt(self, new_value: float) -> None:
        self._downtilt = new_value

    def with_units(self, value: float, abbr: bool = True, large: bool = False) -> str:
        """Convert a distance number to a string with units."""
        type = "metric" if self.use_metric else "imperial"
        size = 1 if large else 0
        plurality = 2 if value >= 2 else 1
        if abbr:
            result = f"{value} {self.units['distance'][type][size][0]}"
        else:
            result = f"{value} {self.units['distance'][type][size][plurality]}"
        return result

    @classmethod
    def from_file(cls, report_filename: str, type="tx"):
        """Parse an analysis report file a extract Transmitter details.

        Site instance factory method.
        """
        if type in ["tx", "rx"]:
            new_site = cls(type)
        else:
            raise (Exception(f"{type} - Invalid Site type."))
        try:
            if "mile" in open(report_filename).read():
                new_site.use_metric = False
            else:
                new_site.use_metric = True
            in_target_section = False
            with open(report_filename) as report:
                for line in report:
                    if type == "tx":
                        if in_target_section:
                            if line.startswith("Site location:"):
                                new_site.longitude, new_site.latitude = map(
                                    float, line.strip().split(": ")[1].split(", ")
                                )
                            elif line.startswith("Ground elevation:"):
                                new_site.elevation = float(
                                    line.strip().split(": ")[1].split(" ")[0]
                                )
                            elif line.startswith("Antenna height:"):
                                new_site.height = float(
                                    line.strip().split(": ")[1].split(" ")[0]
                                )
                            elif line.startswith("Distance to Rx:"):
                                new_site.distance = float(
                                    line.strip().split(": ")[1].split(" ")[0]
                                )
                            elif line.startswith("Azimuth to Rx:"):
                                new_site.azimuth = float(
                                    line.strip().split(": ")[1].split(" ")[0]
                                )
                            elif line.startswith("Downtilt angle to Rx:"):
                                new_site.downtilt = float(
                                    line.strip().split(": ")[1].split(" ")[0]
                                )
                                in_target_section = False
                        else:
                            if line.startswith("Transmitter site:"):
                                in_target_section = True
                    else:
                        if in_target_section:
                            if line.startswith("Site location:"):
                                new_site.longitude, new_site.latitude = map(
                                    float, line.strip().split(": ")[1].split(", ")
                                )
                            elif line.startswith("Ground elevation:"):
                                new_site.elevation = float(
                                    line.strip().split(": ")[1].split(" ")[0]
                                )
                            elif line.startswith("Antenna height:"):
                                new_site.height = float(
                                    line.strip().split(": ")[1].split(" ")[0]
                                )
                            elif line.startswith("Distance to Tx:"):
                                new_site.distance = float(
                                    line.strip().split(": ")[1].split(" ")[0]
                                )
                            elif line.startswith("Azimuth to Tx:"):
                                new_site.azimuth = float(
                                    line.strip().split(": ")[1].split(" ")[0]
                                )
                            elif line.startswith("Downtilt angle to Tx:"):
                                new_site.downtilt = float(
                                    line.strip().split(": ")[1].split(" ")[0]
                                )
                                in_target_section = False
                        else:
                            if line.startswith("Receiver site:"):
                                in_target_section = True

            return new_site
        except Exception as err:
            raise (Exception(f"A problem occurred while parsing report file. {err}"))

    def __str__(self):
        """Return a human readable string representation of a Site instance."""
        site_string = f"""\
Site: {self.site}
Site location: {self.longitude:0.2f}, {self.latitude:0.2f}
Ground elevation: {self.with_units(self.elevation, abbr=False)} AMSL
Antenna height: {self.with_units(self.height, abbr=False)} AGL
Distance to remote site: {self.with_units(self.distance, abbr=False, large=True)}
Azimuth to remote site: {self.azimuth:0.2f} degrees grid
Downtilt angle to remote site: {self.downtilt:0.4f} degrees
"""
        return site_string
