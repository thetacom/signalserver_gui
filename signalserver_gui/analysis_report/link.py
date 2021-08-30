"""This module contains the AnalysisReport Link class."""
from typing import List
from .obstruction import Obstruction


class Link:
    """The AnalysisReport Link class."""

    units = {
        "distance": {
            "imperial": [("ft", "foot", "feet"), ("mi", "mile", "miles")],
            "metric": [("m", "meter", "meters"), ("km", "kilometer", "kilometers")],
        }
    }

    def __init__(
        self,
        free_space_path_loss: float = 0.0,
        computed_path_loss: float = 0.0,
        terrain_shielding_attenuation: float = 0.0,
        field_strength_at_rx: float = 0.0,
        power_level_at_rx: float = 0.0,
        power_density_at_rx: float = 0.0,
        voltage_50ohm_dipole: float = 0.0,
        voltage_75ohm_dipole: float = 0.0,
        longley_rice_errors: int = 0,
        rx_adjustment_to_clear_obstructions: float = 0.0,
        rx_adjustment_to_clear_first_fresnel_zone: float = 0.0,
        rx_adjustment_to_clear_first_fresnel_zone60: float = 0.0,
        obstructions: List[Obstruction] = [],
        use_metric=False,
    ):
        """Initialize a new AnalysisReport Link instance."""
        self.free_space_path_loss = free_space_path_loss
        self.computed_path_loss = computed_path_loss
        self.terrain_shielding_attenuation = terrain_shielding_attenuation
        self.field_strength_at_rx = field_strength_at_rx
        self.power_level_at_rx = power_level_at_rx
        self.power_density_at_rx = power_density_at_rx
        self.voltage_50ohm_dipole = voltage_50ohm_dipole
        self.voltage_75ohm_dipole = voltage_75ohm_dipole
        self.longley_rice_errors = longley_rice_errors
        self.rx_adjustment_to_clear_obstructions = rx_adjustment_to_clear_obstructions
        self.rx_adjustment_to_clear_first_fresnel_zone = (
            rx_adjustment_to_clear_first_fresnel_zone
        )
        self.rx_adjustment_to_clear_first_fresnel_zone60 = (
            rx_adjustment_to_clear_first_fresnel_zone60
        )
        self._obstructions = obstructions
        self._use_metric = use_metric

    @property
    def use_metric(self) -> bool:
        """Getter/Setter for free_space_path_loss property."""
        return self._use_metric

    @use_metric.setter
    def use_metric(self, new_value: bool = True) -> None:
        self._use_metric = new_value

    @property
    def free_space_path_loss(self) -> float:
        """Getter/Setter for free_space_path_loss property."""
        return self._free_space_path_loss

    @free_space_path_loss.setter
    def free_space_path_loss(self, new_value: float) -> None:
        self._free_space_path_loss = new_value

    @property
    def computed_path_loss(self) -> float:
        """Getter/Setter for computed_path_loss property."""
        return self._computed_path_loss

    @computed_path_loss.setter
    def computed_path_loss(self, new_value: float) -> None:
        self._computed_path_loss = new_value

    @property
    def terrain_shielding_attenuation(self) -> float:
        """Getter/Setter for terrain_shielding_attenuation property."""
        return self._terrain_shielding_attenuation

    @terrain_shielding_attenuation.setter
    def terrain_shielding_attenuation(self, new_value: float) -> None:
        self._terrain_shielding_attenuation = new_value

    @property
    def power_level_at_rx(self) -> float:
        """Getter/Setter for power_level_at_rx property."""
        return self._power_level_at_rx

    @power_level_at_rx.setter
    def power_level_at_rx(self, new_value: float) -> None:
        self._power_level_at_rx = new_value

    @property
    def power_density_at_rx(self) -> float:
        """Getter/Setter for power_density_at_rx property."""
        return self._power_density_at_rx

    @power_density_at_rx.setter
    def power_density_at_rx(self, new_value: float) -> None:
        self._power_density_at_rx = new_value

    @property
    def voltage_50ohm_dipole(self) -> float:
        """Getter/Setter for voltage_50ohm_dipole property."""
        return self._voltage_50ohm_dipole

    @voltage_50ohm_dipole.setter
    def voltage_50ohm_dipole(self, new_value: float) -> None:
        self._voltage_50ohm_dipole = new_value

    @property
    def voltage_75ohm_dipole(self) -> float:
        """Getter/Setter for voltage_75ohm_dipole property."""
        return self._voltage_75ohm_dipole

    @voltage_75ohm_dipole.setter
    def voltage_75ohm_dipole(self, new_value: float) -> None:
        self._voltage_75ohm_dipole = new_value

    @property
    def longley_rice_errors(self) -> int:
        """Getter/Setter for longley_rice_errors property."""
        return self._longley_rice_errors

    @longley_rice_errors.setter
    def longley_rice_errors(self, new_value: int) -> None:
        self._longley_rice_errors = new_value

    @property
    def rx_adjustment_to_clear_obstructions(self) -> float:
        """Getter/Setter for rx_adjustment_to_clear_obstructions property."""
        return self._rx_adjustment_to_clear_obstructions

    @rx_adjustment_to_clear_obstructions.setter
    def rx_adjustment_to_clear_obstructions(self, new_value: float) -> None:
        self._rx_adjustment_to_clear_obstructions = new_value

    @property
    def rx_adjustment_to_clear_first_fresnel_zone(self) -> float:
        """Getter/Setter for rx_adjustment_to_clear_first_fresnel_zone property."""
        return self._rx_adjustment_to_clear_first_fresnel_zone

    @rx_adjustment_to_clear_first_fresnel_zone.setter
    def rx_adjustment_to_clear_first_fresnel_zone(self, new_value: float) -> None:
        self._rx_adjustment_to_clear_first_fresnel_zone = new_value

    @property
    def rx_adjustment_to_clear_first_fresnel_zone60(self) -> float:
        """Getter/Setter for rx_adjustment_to_clear_first_fresnel_zone60 property."""
        return self._rx_adjustment_to_clear_first_fresnel_zone60

    @rx_adjustment_to_clear_first_fresnel_zone60.setter
    def rx_adjustment_to_clear_first_fresnel_zone60(self, new_value: float) -> None:
        self._rx_adjustment_to_clear_first_fresnel_zone60 = new_value

    @property
    def obstructions(self) -> List[Obstruction]:
        """Getter for obstructions property."""
        return self._obstructions

    @obstructions.setter
    def obstructions(self, obstructions: List[Obstruction]) -> None:
        """Setter for obstructions property."""
        self._obstructions = obstructions

    def add_obstruction(self, new_item: Obstruction) -> None:
        """Add a new obstruction to the obstruction list."""
        self.obstructions.append(new_item)

    def add_obstruction_from_str(self, descriptor: str) -> None:
        """Add a new obstruction to the obstruction list."""
        self.obstructions.append(Obstruction.from_string(descriptor))

    @classmethod
    def from_file(cls, report_filename):
        """Parse an analysis report file a extract Link details.

        Link instance factory method.
        """
        new_link = Link()
        try:
            in_target_section = False
            adjustment_lines = 0
            if "mile" in open(report_filename).read():
                new_link.use_metric = False
            else:
                new_link.use_metric = True
            with open(report_filename) as report:
                obstructions = []
                for line in report:
                    if in_target_section:
                        if line.startswith("Free space path loss:"):
                            new_link.free_space_path_loss = float(
                                line.strip().split(": ")[1].split(" ")[0]
                            )
                        elif line.startswith("Computed path loss:"):
                            new_link.computed_path_loss = float(
                                line.strip().split(": ")[1].split(" ")[0]
                            )
                        elif line.startswith("Attenuation due to"):
                            new_link.terrain_shielding_attenuation = float(
                                line.strip().split(": ")[1].split(" ")[0]
                            )
                        elif line.startswith("Field strength"):
                            new_link.field_strength_at_rx = float(
                                line.strip().split(": ")[1].split(" ")[0]
                            )
                        elif line.startswith("Signal power level"):
                            new_link.power_level_at_rx = float(
                                line.strip().split(": ")[1].split(" ")[0]
                            )
                        elif line.startswith("Signal power density"):
                            new_link.power_density_at_rx = float(
                                line.strip().split(": ")[1].split(" ")[0]
                            )
                        elif line.startswith("Voltage across 50 ohm"):
                            new_link.voltage_50ohm_dipole = float(
                                line.strip().split(": ")[1].split(" ")[0]
                            )
                        elif line.startswith("Voltage across 75 ohm"):
                            new_link.voltage_75ohm_dipole = float(
                                line.strip().split(": ")[1].split(" ")[0]
                            )
                        elif line.startswith("Longley-Rice model"):
                            new_link.longley_rice_errors = int(
                                line.strip().split(": ")[1].split(" ")[0]
                            )
                        elif (
                            "Antenna at Rx must be raised" in line
                            and adjustment_lines == 0
                        ):
                            adjustment_lines += 1
                            new_link.rx_adjustment_to_clear_obstructions = float(
                                line.strip().split("at least ")[1].split(" ")[0]
                            )
                        elif "No obstructions to LOS path" in line:
                            adjustment_lines += 1
                        elif (
                            "Antenna at Rx must be raised" in line
                            and adjustment_lines == 1
                        ):
                            adjustment_lines += 1
                            new_link.rx_adjustment_to_clear_first_fresnel_zone = float(
                                line.strip().split("at least ")[1].split(" ")[0]
                            )
                        elif (
                            "Antenna at Rx must be raised" in line
                            and adjustment_lines == 2
                        ):
                            adjustment_lines += 1
                            new_link.rx_adjustment_to_clear_first_fresnel_zone60 = (
                                float(line.strip().split("at least ")[1].split(" ")[0])
                            )
                        elif line.startswith("    "):
                            obstructions.append(Obstruction.from_string(line))
                            # new_link.add_obstruction_from_str(line)
                    else:
                        if line.startswith("Summary for the link between Tx and Rx:"):
                            in_target_section = True
            new_link.obstructions = obstructions
            return new_link
        except Exception as e:
            raise (Exception(f"A problem occurred while parsing report file. {e}"))

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

    def __str__(self) -> str:
        """Human readable representation of AnalysisReport Link instance."""
        link_string = f"""\
Link Summary:
Free space path loss: {self.free_space_path_loss} dB
Computed path loss: {self.computed_path_loss} dB
Attenuation due to terrain shielding: {self.terrain_shielding_attenuation} dB
Field strength at Rx: {self.field_strength_at_rx} dBuV/meter
Signal power level at Rx: {self.power_level_at_rx} dBm
Signal power density at Rx: {self.power_density_at_rx} dBW per square meter
Voltage across 50 ohm dipole at Rx: {self.voltage_50ohm_dipole} uV
Voltage across 75 ohm dipole at Rx: {self.voltage_50ohm_dipole} uV
Longley-Rice model error number: {self.longley_rice_errors}

- Antenna at Rx must be raised to at least {self.with_units(self.rx_adjustment_to_clear_obstructions, abbr=False)} AGL to clear all obstructions detected.
- Antenna at Rx must be raised to at least {self.with_units(self.rx_adjustment_to_clear_first_fresnel_zone, abbr=False)} AGL to clear the first Fresnel zone.
- Antenna at Rx must be raised to at least {self.with_units(self.rx_adjustment_to_clear_first_fresnel_zone60, abbr=False)} AGL to clear 60% of the first Fresnel zone.

Obstructions:
"""
        if self.obstructions:
            for obs in self.obstructions:
                link_string += str(obs)
        else:
            link_string += "None\n"
        return link_string
