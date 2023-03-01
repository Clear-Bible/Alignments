"""Read alignment data from Grape City.

Note that some of the target texts were typed in by hand, so may have
minor differences from authoritative editions.

"""

from collections import UserDict
from dataclasses import dataclass, field
import json
from pathlib import Path
from typing import Union
import tomli

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


# @dataclass
# class AlignmentSet:
#     """Manage all the alignment data for a verse."""

#     verseid: str
#     items: list = field(default_factory=list)

#     def __repr__(self) -> str:
#         """Return a printed representation."""
#         return f"<AlignmentSet({self.verseid})>"

#     def namesets(self, sourceattr: str = "text") -> list:
#         """Return a list of lists pairing a source name with target term(s).

#         By default, the text attribute for the source is provided, or
#         you can specify a different sourceattr.

#         """
#         return [
#             (getattr(ag.sourceitems[0], sourceattr), t.text)
#             for ag in self.items
#             if ag.issourcename
#             for t in ag.targetitems
#         ]


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
