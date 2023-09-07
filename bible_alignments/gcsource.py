"""Manage the source data for Grape City (gc) alignments.

When pip-installed, this only includes the LEB data: other data isn't included. 

>>> from bible_alignments import gcsource, config
>>> lebntcfg = config.Configuration(sourceid="NA27", targetid="LEB", targetlanguage="eng", processid="manual")
# read NA/27 GNT data for the LEB alignment
>>> rd = gcsource.Reader(configuration=lebntcfg)
"""

from collections import UserDict
from csv import DictReader
from dataclasses import dataclass

from bible_alignments import config

# these attribute names match the source data for simplicity


@dataclass(order=True)
class Source:
    """Manage source data for a word/morph read from file."""

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

    @property
    def position(self) -> int:
        """Return the word position in the verse."""
        return int(self.identifier[8:11])

    def display(self) -> None:
        """Print a readable display of the key data."""
        print(f"{self.identifier}: {self.text:<20} ('{self.gloss}', '{self.lemma}', {self.pos})")


class Reader(UserDict):
    """Manages source data read from file."""

    def __init__(self, configuration: config.Configuration) -> None:
        """Initialize Reader instance."""
        super().__init__(self)
        with configuration.sourcepath.open(encoding="utf-8") as f:
            dictreader = DictReader(f, delimiter="\t")
            self.data = {source.identifier: source for row in dictreader if (source := Source(**row))}
