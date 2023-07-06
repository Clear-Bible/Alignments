"""Manage the target data for Grape City (gc) alignments."""

from collections import UserDict
from csv import DictReader
from dataclasses import dataclass

from bible_alignments import config

# these attribute names match the source data for simplicity


@dataclass
class Target:
    """Manage target data for a word."""

    # Identifies the word/morph in BBCCCVVVWWWP format
    # note, no word part: so this doesn't support sub-word tokens
    identifier: str
    # ?
    altId: str
    # surface form: omit this for copyrighted sources
    text: str
    # ?
    transType: str
    # is this token punctuation?
    # Not always set, at least not for YLT
    isPunc: bool
    # if the same word is aligned to multiple source words, the
    # primary word is the content-bearing term? Example from 42004003
    isPrimary: bool
    _fields: tuple = ("identifier", "altId", "text", "transType", "isPunc", "isPrimary")

    def __repr__(self) -> str:
        """Return a printed representation."""
        return f"<Target: {self.identifier}>"

    @staticmethod
    def fromrow(row) -> "Target":
        """Return an instance from a row of data."""
        # convert strings to booleans
        row["isPunc"] = True if row["isPunc"] == "True" else False
        row["isPrimary"] = True if row["isPrimary"] == "True" else False
        return Target(**row)

    @property
    def token(self) -> str:
        """Return text.

        For compatability with Source().
        """
        return self.text

    def display(self) -> None:
        """Print a readable display of the key data."""
        print(f"{self.identifier}: {self.text:<20} ('{self.transType}', {self.isPunc}, {self.isPrimary})")


class Reader(UserDict):
    """Manages target data read from file."""

    def __init__(self, configuration: config.Configuration) -> None:
        """Initialize Reader instance."""
        super().__init__(self)
        with configuration.targetpath.open(encoding="utf-8") as f:
            dictreader = DictReader(f, fieldnames=Target._fields, delimiter="\t")
            self.data = {target.identifier: target for row in dictreader if (target := Target.fromrow(row))}
