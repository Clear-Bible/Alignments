"""Read alignment data from Grape City.

Note that some of the target texts were typed in by hand, so may have
minor differences from authoritative editions.

"""

from collections import UserDict
from dataclasses import dataclass, field
import itertools
import json
from typing import Union

from src import config, gcsource, gctarget

# from . import config, gcsource, gctarget

# type that's either None (undefined) or a float. This allows 0.0 as a
# declared value.
nonefloat = Union[str, None]


@dataclass
class AlignmentGroup:
    """Manage alignment data for a word.

    sourceitems and targetitems are sequences of zero or more items,
    typically 1, or 2 if many-to-many. The values are instances of Source  indexes into the
    sequences of sourceitems and targetitems.

    Confidence defaults to undefined (None): if provided, it should be
    a float from 0.0-1.0 inclusive. Not provided for manual alignments
    (no assumption that human aligners are perfect).

    """

    identifier: str
    sourceitems: tuple
    targetitems: tuple
    # empty by default
    meta: dict = field(default_factory=dict)

    def __repr__(self) -> str:
        """Return a printed representation."""
        return f"<AGroup({self.identifier}): [{self.sourceitems}, {self.targetitems}]>"

    @property
    def issourcename(self) -> bool:
        """Return True if a single source term with pos=Name."""
        return len(self.sourceitems) == 1 and self.sourceitems[0].pos == "Name"

    def display(self) -> None:
        """Display text for alignments."""
        print(f"{self.identifier}: {[s.token for s in self.sourceitems]}\t{[s.token for s in self.targetitems]}")


def verseid(ag):
    """Key function for grouping by verse.

    Takes an alignment group and return the verse ID.
    """
    # not sure why this doesn't work
    # assert isinstance(ag, AlignmentGroup), f"Arg must be an AlignmentGroup instance: {ag}"
    assert ag.__class__.__name__ == "AlignmentGroup", f"Arg must be an AlignmentGroup instance: {ag}"
    return ag.identifier.split(".")[0]


@dataclass
class AlignmentSet:
    """Manage all the alignment data for a verse."""

    verseid: str
    sources: list = field(default_factory=list)
    targets: list = field(default_factory=list)
    items: list = field(default_factory=list)

    def __repr__(self) -> str:
        """Return a printed representation."""
        return f"<AlignmentSet({self.verseid})>"

    @staticmethod
    def from_aglist(aglist) -> "AlignmentSet":
        """Return an AlignmentSet for a list of AlignmentGroups."""
        assert aglist, f"List must not be empty: {aglist}"
        verseID = verseid(aglist[0])
        aset = AlignmentSet(verseid=verseID)
        aset.sources = [item for ag in aglist for item in ag.sourceitems]
        aset.targets = [item for ag in aglist for item in ag.targetitems]
        aset.items = aglist
        return aset

    # def namesets(self, sourceattr: str = "text") -> list:
    #     """Return a list of lists pairing a source name with target term(s).

    #     By default, the text attribute for the source is provided, or
    #     you can specify a different sourceattr.

    #     """
    #     return [
    #         (getattr(ag.sourceitems[0], sourceattr), t.text)
    #         for ag in self.items
    #         if ag.issourcename
    #         for t in ag.targetitems
    #     ]


class Reader(UserDict):
    """Read alignment data and integrate source and target."""

    def __init__(self, sourceid: str, targetid: str, languageid: str, processid: str) -> None:
        """Initialize Reader instance."""
        self.sourceid = sourceid
        self.targetid = targetid
        self.languageid = languageid
        self.processid = processid
        super().__init__(self)
        self.sourcereader = gcsource.Reader(sourceid, targetid)
        self.targetreader = gctarget.Reader(sourceid, targetid)
        # check here if a valid language
        # check here if a valid combination of sourceid, targetid, process
        alignmentdir = config.ALIGNMENTS / languageid / targetid
        # load all the alignments: not grouped by verse
        with (alignmentdir / f"{sourceid}-{targetid}-{processid}.json").open(encoding="utf-8") as f:
            self.data = {
                agid: AlignmentGroup(identifier=agid, sourceitems=sourceitems, targetitems=targetitems, meta=metadict)
                for aldict in json.load(f)
                # only a single key
                if (agid := list(aldict.keys())[0])
                # map the source identifiers to instances
                if (sourceitems := [self.sourcereader[s] for s in aldict[agid][sourceid]])
                # map the target identifiers to instances
                if (targetitems := [self.targetreader[t] for t in aldict[agid][targetid]])
                if (metadict := aldict[agid]["meta"])
            }

    def display(self) -> None:
        """Display configuration information for a Reader."""
        print(f"Source:\t{self.sourceid}\t({len(self.sourcereader)} words)")
        print(f"Target:\t{self.targetid}\t({len(self.targetreader)} words)")
        print(f"Process:\t{self.processid}")
        print(f"{len(self)} alignments")

    def source_concordance(self, value: str, attr: str = "lemma") -> list[AlignmentGroup]:
        """Return alignment groups whose source attr value is value."""
        return [ag for ag in self.data.values() if value in [getattr(s, attr) for s in ag.sourceitems]]

    def verse_groups(self) -> list[list[AlignmentGroup]]:
        """Return a list of lists of AlignmentGroups, by verse."""
        return [list(g) for k, g in itertools.groupby(self.values(), verseid)]
