"""This module contains the AnalysisReport Link Obstruction class."""


class Obstruction:
    """The AnalysisReport Link Obstruction class."""

    units = {
        "distance": {
            "imperial": [("ft", "foot", "feet"), ("mi", "mile", "miles")],
            "metric": [("m", "meter", "meters"), ("km", "kilometer", "kilometers")],
        }
    }

    def __init__(
        self,
        longitude: float,
        latitude: float,
        distance: float,
        height: float,
        metric: bool = False,
    ) -> None:
        """Initialize a new Obstruction instance."""
        self.longitude = longitude
        self.latitude = latitude
        self.distance = distance
        self.height = height
        self.metric = metric

    @property
    def metric(self) -> bool:
        """Getter/Setter for free_space_path_loss property."""
        return self._metric

    @metric.setter
    def metric(self, new_value: bool = True) -> None:
        self._metric = new_value

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
    def distance(self) -> float:
        """Getter/Setter for distance property."""
        return self._distance

    @distance.setter
    def distance(self, new_value: float) -> None:
        self._distance = new_value

    @property
    def height(self) -> float:
        """Getter/Setter for height property."""
        return self._height

    @height.setter
    def height(self, new_value: float) -> None:
        self._height = new_value

    @property
    def metric_height(self) -> float:
        """Getter/Setter for height property."""
        if self.metric:
            return self._height
        else:
            return self._height / 3.28084

    @metric_height.setter
    def metric_height(self, new_value: float) -> None:
        if self.metric:
            self._height = new_value
        else:
            self._height = new_value * 3.28084

    def with_units(self, value: float, abbr: bool = True, large: bool = False) -> str:
        """Convert a distance number to a string with units."""
        type = "metric" if self.metric else "imperial"
        size = 1 if large else 0
        plurality = 2 if value >= 2 else 1
        if abbr:
            result = f"{value} {self.units['distance'][type][size][0]}"
        else:
            result = f"{value} {self.units['distance'][type][size][plurality]}"
        return result

    @classmethod
    def from_string(cls, descriptor: str):
        """Create new Obstruction object from descriptor string.

        Obstruction instance factory method.
        """
        print(f"New Obstruction: {descriptor}")
        try:
            # 51.5082 N,   0.5014 W, 20.27 miles, 118.11 feet AMSL
            metric = False if "mile" in descriptor else True
            parts = [i.strip() for i in descriptor.strip().split(", ")]
            longitude = (
                -float(parts[1].split(" ")[0])
                if parts[1].split(" ")[1] == "W"
                else float(parts[1].split(" ")[0])
            )
            latitude = (
                float(parts[0].split(" ")[0])
                if parts[0].split(" ")[1] == "N"
                else -(float(parts[0].split(" ")[0]))
            )
            distance = float(parts[2].split(" ")[0])
            height = float(parts[3].split(" ")[0])
            return Obstruction(longitude, latitude, distance, height, metric)
        except Exception as e:
            raise (
                Exception("Unable to parse obstruction descriptor. {e}\n{descriptor}")
            )

    def __str__(self) -> str:
        """Return human readable string representation of an Obstruction instance."""
        return f"({self.longitude}, {self.latitude}) - {self.with_units(self.distance, abbr=False, large=True)}, {self.with_units(self.height)} AMSL.\n"
