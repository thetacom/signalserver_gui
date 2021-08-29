"""This module contains the AnalysisReport PropagationModel class."""


class PropagationModel:
    """The AnalysisReport PropagationModel class."""

    def __init__(
        self,
        model: str = "",
        subtype: str = "",
        dielectric_constant: float = 0.0,
        earth_conductivity: float = 0.0,
        atmospheric_bending: float = 0.0,
        frequency: float = 0.0,
        radio_climate: str = "",
        polarization: str = "",
        fraction_of_situations: float = 0.5,
        fraction_of_time: float = 0.5,
        rx_gain: float = 0.0,
        tx_erp_plus_rx_gain: float = 0.0,
        tx_erp_minus_rx_gain: float = 0.0,
        tx_eirp_plus_rx_gain: float = 0.0,
        tx_eirp_minus_rx_gain: float = 0.0,
    ):
        """Initialize a new PropagationModel instance."""
        self.model = model
        self.subtype = subtype
        self.dielectric_constant = dielectric_constant
        self.earth_conductivity = earth_conductivity
        self.atmospheric_bending = atmospheric_bending
        self.frequency = frequency
        self.radio_climate = radio_climate
        self.polarization = polarization
        self.fraction_of_situation = fraction_of_situations
        self.fraction_of_time = fraction_of_time
        self.rx_gain = rx_gain
        self.tx_erp_plus_rx_gain = tx_erp_plus_rx_gain
        self.tx_erp_minus_rx_gain = tx_erp_minus_rx_gain
        self.tx_eirp_plus_rx_gain = tx_eirp_plus_rx_gain
        self.tx_eirp_minus_rx_gain = tx_eirp_minus_rx_gain

    @property
    def model(self) -> str:
        """Getter/Setter for model property."""
        return self._model

    @model.setter
    def model(self, new_value: str) -> None:
        self._model = new_value

    @property
    def subtype(self) -> str:
        """Getter/Setter for site property."""
        return self._subtype

    @subtype.setter
    def subtype(self, new_value: str) -> None:
        self._subtype = new_value

    @property
    def dielectric_constant(self) -> float:
        """Getter/Setter for dielectric_constant property."""
        return self._dielectric_constant

    @dielectric_constant.setter
    def dielectric_constant(self, new_value: float) -> None:
        self._dielectric_constant = new_value

    @property
    def earth_conductivity(self) -> float:
        """Getter/Setter for earth_conductivity property."""
        return self._earth_conductivity

    @earth_conductivity.setter
    def earth_conductivity(self, new_value: float) -> None:
        self._earth_conductivity = new_value

    @property
    def atmospheric_bending(self) -> float:
        """Getter/Setter for atmospheric_bending property."""
        return self._atmospheric_bending

    @atmospheric_bending.setter
    def atmospheric_bending(self, new_value: float) -> None:
        self._atmospheric_bending = new_value

    @property
    def frequency(self) -> float:
        """Getter/Setter for frequency property."""
        return self._frequency

    @frequency.setter
    def frequency(self, new_value: float) -> None:
        self._frequency = new_value

    @property
    def radio_climate(self) -> str:
        """Getter/Setter for radio_climate property."""
        return self._radio_climate

    @radio_climate.setter
    def radio_climate(self, new_value: str) -> None:
        self._radio_climate = new_value

    @property
    def polarization(self) -> str:
        """Getter/Setter for polarization property."""
        return self._polarization

    @polarization.setter
    def polarization(self, new_value: str) -> None:
        self._polarization = new_value

    @property
    def fraction_of_situation(self) -> float:
        """Getter/Setter for fraction_of_situation property."""
        return self._fraction_of_situation

    @fraction_of_situation.setter
    def fraction_of_situation(self, new_value: float) -> None:
        self._fraction_of_situation = new_value

    @property
    def fraction_of_time(self) -> float:
        """Getter/Setter for fraction_of_time property."""
        return self._fraction_of_time

    @fraction_of_time.setter
    def fraction_of_time(self, new_value: float) -> None:
        self._fraction_of_time = new_value

    @property
    def rx_gain(self) -> float:
        """Getter/Setter for rx_gain property."""
        return self._rx_gain

    @rx_gain.setter
    def rx_gain(self, new_value: float) -> None:
        self._rx_gain = new_value

    @property
    def tx_erp_plus_rx_gain(self) -> float:
        """Getter/Setter for tx_erp_plus_rx_gain property."""
        return self._tx_erp_plus_rx_gain

    @tx_erp_plus_rx_gain.setter
    def tx_erp_plus_rx_gain(self, new_value: float) -> None:
        self._tx_erp_plus_rx_gain = new_value

    @property
    def tx_erp_minus_rx_gain(self) -> float:
        """Getter/Setter for tx_erp_minus_rx_gain property."""
        return self._tx_erp_minus_rx_gain

    @tx_erp_minus_rx_gain.setter
    def tx_erp_minus_rx_gain(self, new_value: float) -> None:
        self._tx_erp_minus_rx_gain = new_value

    @property
    def tx_eirp_plus_rx_gain(self) -> float:
        """Getter/Setter for tx_eirp_plus_rx_gain property."""
        return self._tx_eirp_plus_rx_gain

    @tx_eirp_plus_rx_gain.setter
    def tx_eirp_plus_rx_gain(self, new_value: float) -> None:
        self._tx_eirp_plus_rx_gain = new_value

    @property
    def tx_eirp_minus_rx_gain(self) -> float:
        """Getter/Setter for tx_eirp_minus_rx_gain property."""
        return self._tx_eirp_minus_rx_gain

    @tx_eirp_minus_rx_gain.setter
    def tx_eirp_minus_rx_gain(self, new_value: float) -> None:
        self._tx_eirp_minus_rx_gain = new_value

    @classmethod
    def from_file(cls, report_filename: str):
        """Parse an analysis report file and extract propagation model details.

        PropagationModel instance factory method.
        """
        new_model = cls()
        try:
            in_target_section = False
            with open(report_filename) as report:
                for line in report:
                    if in_target_section:
                        if line.startswith("Propagation model:"):
                            new_model.model = line.strip().split(": ")[1]
                        elif line.startswith("Model sub-type:"):
                            new_model.subtype = line.strip().split(": ")[1]
                        elif line.startswith("Earth's Dielectric Constant:"):
                            new_model.dielectric_constant = float(
                                line.strip().split(": ")[1]
                            )
                        elif line.startswith("Earth's Conductivity:"):
                            new_model.earth_conductivity = float(
                                line.strip().split(": ")[1].split(" ")[0]
                            )
                        elif line.startswith("Atmospheric Bending Constant (N-units):"):
                            new_model.atmospheric_bending = float(
                                line.strip().split(": ")[1].split(" ")[0]
                            )
                        elif line.startswith("Frequency:"):
                            new_model.frequency = float(
                                line.strip().split(": ")[1].split(" ")[0]
                            )
                        elif line.startswith("Radio Climate:"):
                            new_model.radio_climate = line.strip().split("(")[1][:-1]
                        elif line.startswith("Polarization:"):
                            new_model.polarization = (
                                line.strip().split("(")[1][:-1].lower()
                            )
                        elif line.startswith("Fraction of Situations:"):
                            new_model.fraction_of_situation = (
                                float(line.strip().split(": ")[1].strip("%")) / 100
                            )
                        elif line.startswith("Fraction of Time:"):
                            new_model.fraction_of_time = (
                                float(line.strip().split(": ")[1].strip("%")) / 100
                            )
                        elif line.startswith("Receiver gain:"):
                            new_model.rx_gain = float(
                                line.strip().split(": ")[1].split(" ")[0]
                            )
                        elif line.startswith("Transmitter ERP plus"):
                            new_model.tx_erp_plus_rx_gain = float(
                                line.strip().split(": ")[1].split(" ")[0]
                            )
                        elif line.startswith("Transmitter ERP minus"):
                            new_model.tx_erp_minus_rx_gain = float(
                                line.strip().split(": ")[1].split(" ")[0]
                            )
                        elif line.startswith("Transmitter EIRP plus"):
                            new_model.tx_eirp_plus_rx_gain = float(
                                line.strip().split(": ")[1].split(" ")[0]
                            )
                        elif line.startswith("Transmitter EIRP minus"):
                            new_model.tx_eirp_minus_rx_gain = float(
                                line.strip().split(": ")[1].split(" ")[0]
                            )
                    elif line.startswith("Downtilt angle to Tx:"):
                        in_target_section = True
            return new_model
        except Exception as err:
            raise (Exception(f"A problem occurred while parsing report file. {err}"))

    def __str__(self):
        """Return a human-readable representation of a PropagationModel instance."""
        propagation_model_string = f"""\
Propagation model: {self.model}
Model sub-type: {self.subtype}
Earth's Dielectric Constant: {self.dielectric_constant}
Earth's Conductivity: {self.earth_conductivity} Siemens/meter
Atmospheric Bending Constant (N-units): {self.atmospheric_bending} ppm
Frequency: {self.frequency} MHz
Radio Climate: {self.radio_climate}
Polarisation: {self.polarization}
Fraction of Situations: {self.fraction_of_situation/100:0.2f}%
Fraction of Time: {self.fraction_of_time/100:0.2f}%

Receiver gain: {self.rx_gain} dBd
Transmitter ERP plus Receiver gain: {self.tx_erp_plus_rx_gain} Watts
Transmitter ERP minus Receiver gain: {self.tx_erp_minus_rx_gain} dBm
Transmitter EIRP plus Receiver gain: {self.tx_eirp_plus_rx_gain} Watts
Transmitter EIRP minus Receiver gain: {self.tx_eirp_minus_rx_gain} dBm
"""
        return propagation_model_string
