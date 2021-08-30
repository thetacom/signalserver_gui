"""This module contains the AnalysisReport class."""
import json
from typing import Union
from .site import Site
from .propagation_model import PropagationModel
from .link import Link


class AnalysisReport:
    """The AnalysisReport class."""

    def __init__(
        self, transmitter: Site, receiver: Site, model: PropagationModel, link: Link
    ) -> None:
        """Initialize a new AnalysisReport instance."""
        self._transmitter = transmitter
        self._receiver = receiver
        self._model = model
        self._link = link

    @property
    def transmitter(self) -> Site:
        """Getter for transmitter property."""
        return self._transmitter

    @property
    def receiver(self) -> Site:
        """Getter for receiver property."""
        return self._receiver

    @property
    def model(self) -> PropagationModel:
        """Getter for model property."""
        return self._model

    @property
    def link(self) -> Link:
        """Getter for link property."""
        return self._link

    @classmethod
    def from_file(cls, report_filename: str):
        """Parse an analysis report file and extract all details.

        AnalysisReport instance factory method.
        """
        transmitter = Site.from_file(report_filename, "tx")
        receiver = Site.from_file(report_filename, "rx")
        model = PropagationModel.from_file(report_filename)
        link = Link.from_file(report_filename)
        return AnalysisReport(transmitter, receiver, model, link)

    def __str__(self):
        """Return a human readable string representation of a AnalysisReport instance."""
        report_string = f"""\
Analysis Report:

{self.transmitter}

{self.receiver}

{self.model}

{self.link}
"""
        return report_string

    def to_json(self):
        """Return AnalysisReport in json."""
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
