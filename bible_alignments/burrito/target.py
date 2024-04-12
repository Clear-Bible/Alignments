"""Manage the target/translation data for Grape City (gc) alignment data.

>>> from bible_alignments.burrito import target
# Reading is normally done by Manager

>>> from bible_alignments import DATAPATH
>>> tr = target.TargetReader(DATAPATH / "targets/eng/nt_BSB.tsv")
# length is the number of tokens
>>> len(tr)
201087
# inspect the 11th word in MRK 4:9
>>> tr["410040090111"].asdict()
{'identifier': '410040090111', 'altId': 'hear-1', 'text': 'hear', 'transType': '', 'isPunc': 'False', 'isPrimary': 'True'}

# Make a new NT target corpus file for Russian from vline data
>>> tw = target.TargetWriter(DATAPATH / "vline/rus/nt_RUSSYN.txt", "nt", "RUSSYN")
>>> len(tw)
160474
# now write it out
>>> tw.write_tsv(DATAPATH / "targets/rus/RUSSYN.tsv")
"""

from collections import UserDict, UserList
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
import re
from string import punctuation
from typing import Any, KeysView
from warnings import warn

from unicodecsv import DictReader, DictWriter

from .BaseToken import BaseToken

# these attribute names match the source data for simplicity


@dataclass(order=True, repr=False)
class Target(BaseToken):
    """Manage data for a target token."""

    # BCV for corresponding source verse
    source_verse: str = ""
    # if True, text displays should not add a space after this token
    skip_space_after: bool = False
    # if True, this token should not be eligible for alignment
    exclude: bool = False
    # ?
    transType: str = ""
    # is this token punctuation?
    # Not always set, at least not for YLT
    isPunc: bool = False
    # if the same word is aligned to multiple source words, the
    # primary word is the content-bearing term? Example from 42004003
    isPrimary: bool = False
    # optional. id of the associated mss token, used in BSB to more easily generate alignment data
    msId: str = ""
    _boolean_fields: tuple = ("skip_space_after", "exclude", "isPunc", "isPrimary")
    _output_fields: tuple = (
        ("id", "id"),
        ("altId", "altId"),
        ("text", "text"),
        ("source_verse", "source_verse"),
        ("skip_space_after", "skip_space_after"),
        ("exclude", "exclude"),
        ("transType", "transType"),
        ("isPunc", "isPunc"),
        ("isPrimary", "isPrimary"),
        # temp
        # ("msId", "msId"),
    )
    # dataclass rules means __hash__ isn't inherited otherwise
    __hash__ = BaseToken.__hash__

    def __post_init__(self) -> None:
        """Compute values after initialization."""
        # set source_verse to match BCV portion of ID if missing
        if not self.source_verse:
            self.source_verse = self.bcv
            # self.source_verse = bcvwpid.to_bcv(self.id)
        truthyre = re.compile("(?i)(y|true)$")
        # booleanize if a string
        for field in self._boolean_fields:
            fieldval = getattr(self, field)
            if isinstance(fieldval, str):
                setattr(self, field, bool(truthyre.match(fieldval)))

    @staticmethod
    def fromjsondict(jdict: dict[str, Any]) -> "Target":
        """Return a Target instance for a dictionary read from JSON."""
        newdict = jdict.copy()
        # convert id attr to a str
        newdict["id"] = str(newdict["id"])
        if len(newdict["id"]) == 10:
            # add missing leading zero: fragile hack!
            newdict["id"] = "0" + newdict["id"]
        # skip_space_after and exclude assume JSON values are "true" or "false"
        if "skip_space_after" in newdict:
            assert isinstance(newdict["skip_space_after"], bool), (
                "Invalid skip_space_after boolean value for " + newdict["id"]
            )
        if "exclude" in newdict:
            assert isinstance(newdict["exclude"], bool), "Invalid exclude boolean value for " + newdict["id"]
        return Target(**newdict)

    @property
    def _display(self) -> str:
        """Return a displayable string for key data."""
        return f"{self.id}: {self.text}\t\t ({self.transType!r}, {self.isPunc}, {self.isPrimary})"

    def display(self) -> None:
        """Print a readable display of the key data."""
        print(self._display)

    def asdict(self, omitfalse: bool = True, omittext: bool = False, omitpartindex: bool = True) -> dict[str, str]:
        """Marshall data to a dict for output.

        With omitfalse = True (the default), only write boolean fields
        if their value is True: otherwise omit them.

        With omitpartindex = True (the default), only include BCVW
        indices.

        With omittext = True, replace altid and text with a
        placeholder: use this for copyrighted texts that cannot be
        redisstributed.

        """
        fdict = dict(self._output_fields)
        outdict = {fdict[k]: getattr(self, k) for k in fdict}
        if omitfalse:
            for field in self._boolean_fields:
                if not outdict[field]:
                    del outdict[field]
        if omittext:
            outdict["altId"] = "--"
            outdict["text"] = "--"
        # by default, drop the final part index
        if omitpartindex:
            outdict["id"] = outdict["id"][:11]
        return outdict


class TargetReader(UserDict):
    """Read Target TSV data into a dict, with identifiers as keys.

    Record data is normalized in some ways as it is read:
    - Convert old-style token identifiers
    - Normalize Unicode text to NKFC
    - Normalize Strong's numbers

    Verse-level indices in altId are also revised: some data had errors.
    """

    inmap = {v: k for k, v in Target._output_fields}

    def __init__(self, tsvpath: Path, idheader: str = "id") -> None:
        """Initialize a Reader instance."""
        super().__init__()
        self.tsvpath = tsvpath
        assert self.tsvpath.exists(), "No such path: pattern is targets/<lang>/<canon>_<targetid>.tsv"
        # assumes conventoins
        self.identifier = self.tsvpath.stem
        # self.canonid, self.targetid = self.identifier.split("_")
        with self.tsvpath.open("rb") as f:
            reader = DictReader(f, delimiter="\t")
            for row in reader:
                assert idheader in row, f"Missing ID header '{idheader}'"
                # adjust name of id column if a different header
                if idheader != "id":
                    idrow = {("id" if k == idheader else k): v for k, v in row.items()}
                else:
                    idrow = row
                identifier = idrow["id"]
                deserialized = {self.inmap[k]: v for k, v in idrow.items() if k in self.inmap}
                if identifier in self:
                    warn(f"{identifier} is duplicated in {self.tsvpath}")
                self.data[identifier] = Target(**deserialized)

    def write_tsv(self, outpath: Path) -> None:
        """Write Targets as TSV.

        This outputs according to the most recent standard, but it does _not_
        correct data errors (e.g. it does not decide if characters are
        actually punctuation, or should not have a following space).

        """
        fields = dict(Target._output_fields).values()
        with outpath.open("wb") as f:
            writer = DictWriter(f, fieldnames=fields, delimiter="\t")
            writer.writeheader()
            for targetinst in self.values():
                writer.writerow(targetinst.asdict())

    def term_tokens(self, term: str, tokenattr: str = "text", lowercase: bool = False) -> list[Target]:
        """Return a list of tokens containing term.

        The attribute used is 'text' by default.

        With lowercase = True (default is False), lower-case term and token values.
        """
        casedterm = term.lower() if lowercase else term
        return [
            token
            for token in self.values()
            if (tokattr := getattr(token, tokenattr))
            if (casedtokenattr := tokattr.lower() if lowercase else tokattr)
            if casedtokenattr == casedterm
        ]


# see internal-alignments for TargetWriter
