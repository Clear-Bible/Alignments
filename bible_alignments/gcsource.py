"""Manage the source data for Grape City (gc) alignments.

>>> from bible_alignments import gcsource
# read NA/27 GNT data for the LEB alignment
>>> rd = gcsource.Reader(sourceid="NA27", targetid="LEB")
"""

from collections import UserDict
from csv import DictReader
from dataclasses import dataclass

from bible_alignments import config

# these attribute names match the source data for simplicity


@dataclass
class Source:
    """Manage source data for a word/morph."""

    # Identifies the word/morph in BBCCCVVVWWWP format
    identifier: str
    # ?
    altId: str
    # surface form: omit this for copyrighted sources
    text: str
    # Strongs number
    strongs: str
    # English gloss
    gloss: str
    # sometimes a Chinese/alternate language gloss?
    gloss2: str
    # source language lemma
    lemma: str
    # part of speech
    pos: str
    # coded morphological information: need to document the format
    morph: str
    _missing: str = "--"
    _fields: tuple = ("identifier", "altId", "text", "strongs", "gloss", "gloss2", "lemma", "pos", "morph")
    # TODO: enumerate and validate part of speech values

    def __repr__(self) -> str:
        """Return a printed representation."""
        return f"<Source: {self.identifier}>"

    @property
    def token(self) -> str:
        """Return text if available, else lemma."""
        return self.lemma if (self.text == self._missing) else self.text

    def display(self) -> None:
        """Print a readable display of the key data."""
        print(f"{self.identifier}: {self.text:<20} ('{self.gloss}', '{self.lemma}', {self.pos})")


class Reader(UserDict):
    """Manages source data read from file."""

    def __init__(self, configuration: config.Configuration) -> None:
        """Initialize Reader instance."""
        super().__init__(self)
        with configuration.sourcepath.open(encoding="utf-8") as f:
            dictreader = DictReader(f, fieldnames=Source._fields, delimiter="\t")
            self.data = {source.identifier: source for row in dictreader if (source := Source(**row))}
