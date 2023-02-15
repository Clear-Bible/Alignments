"""Process alignment data formatted by Grape City.

These alignments were then handed down to Global Bible Initiative (GBI), and then Clear Bible. Note that some of the target texts were typed in by hand, so may have minor differences from authoritative editions. 

The source alignment data is in JSON, with a list of objects
representing verse data. Each verse object has three keys:

- manuscript: a single key "words" whose value is a list of source
  text word/morph objects, with properties like "id", "text", "lemma",
  etc.
- translation: a single key "words" whose value is a list of target
  text word/morph objects, with properties like "id", "text",
  "isPunc", etc.
- links: a list of lists of lists, each terminal list containing one or more indexes into the manuscript and translation words (zero-based). So an element of links like [[0], [0, 1]] means the first word of the source text is aligned with the first two words of the target text.

"""


from dataclasses import dataclass
import json
from pathlib import Path
from typing import Union

#
ROOT = Path(__file__).parent.parent.parent
# these don't belong here
OTJSON = ROOT / "data/eng/ylt/ylt.ot.alignment.json"
NTJSON = ROOT / "data/eng/ylt/ylt.nt.alignment.json"

# type that's either None (undefined) or a float. This allows 0.0 as a
# declared value.
nonefloat = Union[str, None]

# these attribute names match the source data for simplicity


@dataclass
class Manuscript:
    """Manage manuscript data for a word/morph."""

    # Identifies the word/morph in BBCCCVVVWWWP format
    id: str
    # ?
    altId: str
    # surface form: omit this for copyrighted sources
    text: str
    # Strongs number
    strong: str
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

    # TODO: enumerate and validate part of speech values

    @staticmethod
    def fromjsondict(jdict: dict[str, str]) -> "Manuscript":
        """Return a Manuscript instance for a dictionary read from JSON."""
        # convert id attr to a str
        jdict["id"] = str(jdict["id"])
        if len(jdict["id"]) == 11:
            # add missing leading zero: fragile hack!
            jdict["id"] = "0" + jdict["id"]
        return Manuscript(**jdict)


@dataclass
class Translation:
    """Manage translation data for a word."""

    # Identifies the word/morph in BBCCCVVVWWWP format
    # note, no word part: so this doesn't support sub-word tokens
    id: str
    # ?
    altId: str
    # surface form: omit this for copyrighted sources
    text: str
    # ?
    transType: str
    # is this token punctuation?
    # Not always set, at least not for YLT
    isPunc: bool
    # is this token primary? Not sure what the semantics are.
    isPrimary: bool

    @staticmethod
    def fromjsondict(jdict: dict[str, str]) -> "Translation":
        """Return a Manuscript instance for a dictionary read from JSON."""
        # convert id attr to a str
        jdict["id"] = str(jdict["id"])
        if len(jdict["id"]) == 10:
            # add missing leading zero: fragile hack!
            jdict["id"] = "0" + jdict["id"]
        return Translation(**jdict)


@dataclass
class AlignmentGroup:
    """Manage alignment data for a word.

    Zero or more items, typically 1, or 2 if many-to-many. The values
    are indexes into the sequences of sourceitems and targetitems.

    Confidence defaults to undefined (None): if provided, it should be
    a float from 0.0-1.0 inclusive. Not provided for manual alignments
    (no assumption that human aligners are perfect).

    """

    sourceitems: tuple
    targetitems: tuple
    # empty by default
    confidence: nonefloat = None

    def __repr__(self) -> str:
        """Return a printed representation."""
        return f"<AGroup: [{self.sourceitems}, {self.targetitems}]>"


class VerseData:
    """Manages data for a single verse.

    alignmentgroups values are indexes into source/targetitems, so order matters.
    """

    verseid: str = ""
    sourceitems: list = []
    targetitems: list = []
    alignmentgroups: list = []
    # empty by default
    confidence: nonefloat = None

    def __init__(self, versedata: dict[str, dict]):
        """Initialize VerseData instance."""
        self.sourceitems = [Manuscript.fromjsondict(w) for w in versedata["manuscript"]["words"]]
        self.targetitems = [Translation.fromjsondict(w) for w in versedata["translation"]["words"]]
        # need more logic here for handling confidence scores
        self.alignmentgroups = [AlignmentGroup(ag[0], ag[1]) for ag in versedata["links"]]
        self.verseid = self.sourceitems[0].id[:8]

    def __repr__(self) -> str:
        """Return a printed representation."""
        return f"<VerseData({self.verseid})>"

    def aligned_items(self, itemsattr: "targetitems") -> list:
        """Return a list of source or target items that are in alignment groups."""
        assert itemsattr in ["sourceitems", "targetitems"], f"Invalid itemsattr value: {itemsattr}"
        included = sorted([ti for ag in self.alignmentgroups for ti in getattr(ag, itemsattr)])
        return [getattr(self, itemsattr)[titem] for titem in included]

    # possible extensions
    # - display unaligned source/target items
    # - validate no double grouping
    # - default order seems to be source sequence: might want target sequence too


class Reader:
    """Manages data read from Grape City JSON."""

    verseitems: list = []

    def __init__(self, jsonfile: Path):
        """Initialize Reader instance."""
        with jsonfile.open(encoding="utf-8") as f:
            self.verseitems = [VerseData(v) for v in json.load(f)]
