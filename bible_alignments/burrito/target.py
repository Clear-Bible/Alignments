"""Manage the target/translation data for Grape City (gc) alignment data.

>>> from bible_alignments.burrito import target
# Reading is normally done by Manager

>>> from bible_alignments import TARGETS
>>> tr = target.TargetReader(TARGETS / "eng/nt_BSB.tsv")
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
>>> tw.write_tsv(TARGETS / "rus/RUSSYN.tsv")
"""

from collections import UserDict
from dataclasses import dataclass
from pathlib import Path
import re
from typing import Any, Callable, Optional
from warnings import warn

from unicodecsv import DictReader, DictWriter

from biblelib.word import bcvwpid

from .BaseToken import BaseToken, asbool
from .util import groupby_bcv

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
    _input_fields: tuple = (
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
    # just the minimal standard set: override elsewhere if you want more
    _output_fields: tuple = (
        "id",
        "text",
        "source_verse",
        "skip_space_after",
        "exclude",
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
    def same_source_verse(self) -> bool:
        """Return True if source_verse.bcv matches: otherwise indicates versification differences."""
        return self.bcv == self.source_verse

    @property
    def _display(self) -> str:
        """Return a displayable string for key data."""
        return f"{self.id}: {self.text}\t\t ({self.transType!r}, {self.isPunc}, {self.isPrimary})"

    def display(self) -> None:
        """Print a readable display of the key data."""
        print(self._display)

    def asdict(
        self,
        fields: tuple[str] = _output_fields,
        omitfalse: bool = True,
        omittext: bool = False,
    ) -> dict[str, str]:
        """Marshall data to a dict for output.

        With omitfalse = True (the default), only write True values
        for boolean fields.

        With omittext = True, replace altid and text with a
        placeholder: use this for copyrighted texts that cannot be
        redisstributed.

        """
        outdict = {k: getattr(self, k) for k in fields}
        for field in fields:
            if field in self._boolean_fields:
                outdict[field] = "" if (omitfalse and not outdict[field]) else asbool(outdict[field])
        if omittext:
            for omitfield in ["altId", "text"]:
                if omitfield in fields:
                    outdict[omitfield] = "--"
        return outdict


class TargetReader(UserDict):
    """Read Target TSV data into a dict, with identifiers as keys.

    Record data is normalized in some ways as it is read:
    - Convert old-style token identifiers
    - Normalize Unicode text to NKFC
    - Normalize Strong's numbers

    Verse-level indices in altId are also revised: some data had errors.
    """

    inmap = {v: k for k, v in Target._input_fields}

    def __init__(self, tsvpath: Path, idheader: str = "id", keepwordpart: bool = False, strict: bool = False) -> None:
        """Initialize a Reader instance.

        With keepwordpart (default is False), keep the part/subword
        index when creating a token id. Current convention is to never
        keep word parts for target texts.

        """
        super().__init__()
        self.tsvpath = tsvpath
        assert (
            self.tsvpath.exists()
        ), f"No such path as {tsvpath}:\npattern is targets/<targetid>/<canon>_<targetid>.tsv"
        # assumes conventoins
        self.identifier = self.tsvpath.stem
        self.badtokens = {}
        with self.tsvpath.open("rb") as f:
            reader = DictReader(f, delimiter="\t")
            for row in reader:
                assert idheader in row, f"Missing ID header '{idheader}'"
                # adjust name of id column if a different header
                if idheader != "id":
                    idrow = {("id" if k == idheader else k): v for k, v in row.items()}
                else:
                    idrow = row
                # this takes the identifier verbatim: if it has a
                # canon prefix or a word part. So normalize when
                # writing, using bcvwpid.BCVWPID.get_id() and
                # appropriate parameters.
                identifier = idrow["id"]
                # hacky
                if len(identifier) == 12 and not keepwordpart:
                    identifier = idrow["id"] = idrow["id"][0:11]
                deserialized = {self.inmap[k]: v for k, v in idrow.items() if k in self.inmap}
                if identifier in self:
                    warn(f"{identifier} is duplicated in {self.tsvpath}")
                self.data[identifier] = Target(**deserialized)
                # check for empty tokens
                if self.data[identifier].isempty:
                    if strict:
                        warn(f"Empty text for target token {identifier}")
                    self.badtokens[identifier] = self.data[identifier]
        if self.badtokens:
            print(f"{self.identifier} has {len(self.badtokens)} target tokens with empty text: see self.badtokens.")

    def write_tsv(
        self,
        outpath: Path,
        excludefn: Optional[Callable] = None,
        fields: tuple[str] = (
            "id",
            "source_verse",
            "text",
            "skip_space_after",
            "exclude",
        ),
    ) -> None:
        """Write Targets as TSV.

        This outputs according to the most recent standard, but it does _not_
        correct data errors (e.g. it does not decide if characters are
        actually punctuation, or should not have a following space).

        This outputs a reduced set of standard fields, in an order
        that matches kathairo: you can specify otherwise.

        With excludefn, apply this (boolean) function to the token and
        assign the result as the exclude value. This overwrites any
        existing exclude values.

        """
        if not fields:
            fields = tuple(dict(Target._output_fields).values())
        if excludefn:
            if "exclude" not in fields:
                fields = fields + ("exclude",)
        with outpath.open("wb") as f:
            writer = DictWriter(f, fieldnames=fields, delimiter="\t")
            writer.writeheader()
            for targetinst in self.values():
                trgdict = targetinst.asdict()
                # normalize to not include canon prefix or part ID
                trgdict["id"] = bcvwpid.BCVWPID(trgdict["id"]).get_id(prefix=False, part_index=False)
                if excludefn:
                    trgdict["exclude"] = excludefn(targetinst)
                writer.writerow(trgdict)

    def write_vref(self, outpath: Path) -> None:
        """Write a list of verse references for the target tokens."""
        with outpath.open("w") as f:
            self.bcv = groupby_bcv(list(self.values()), bcvfn=lambda t: t.bcv)
            for bcv in self.bcv:
                f.write(f"{bcv}\n")

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
