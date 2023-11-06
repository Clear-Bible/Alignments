"""Read alignment data from Grape City.

Note that some of the target texts were typed in by hand, so may have
minor differences from authoritative editions.

>>> from bible_alignments import grapecity, config
>>> cfg = config.Configuration(sourceid='WLC', targetid='ESV', targetlanguage='eng', processid='manual')
>>> rd = grapecity.Reader(configuration=cfg)
"""

from collections import UserDict
from dataclasses import dataclass, field
import itertools
from pathlib import Path
import json

import pandas as pd

from biblelib.word import bcvwpid

from bible_alignments import config, gcsource, gctarget


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

    def verseid(self) -> str:
        """Return verse ID for grouping by verse."""
        return self.identifier.split(".")[0]

    @property
    def sources(self) -> list[str]:
        """Return a sorted list of source tokens."""
        return sorted(self.sourceitems)

    @property
    def targets(self) -> list[str]:
        """Return a sorted list of target tokens."""
        return sorted(self.targetitems)

    def display(self) -> None:
        """Display text for alignments."""
        print(f"{self.identifier}: {[s.token for s in self.sourceitems]}\t{[s.token for s in self.targetitems]}")


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
    def from_aglist(aglist: list[AlignmentGroup]) -> "AlignmentSet":
        """Return an AlignmentSet for a list of AlignmentGroups."""
        assert aglist, f"List must not be empty: {aglist}"
        verseID = aglist[0].verseid()
        aset = AlignmentSet(verseid=verseID)
        aset.sources = [item for ag in aglist for item in ag.sourceitems]
        aset.targets = [item for ag in aglist for item in ag.targetitems]
        aset.items = aglist
        return aset

    @property
    def usfm(self) -> str:
        """Return a USFM reference for versid."""
        return str(bcvwpid.BCVID(self.verseid).to_usfm())

    def coordinates(self) -> set[tuple[int, int]]:
        """Return a sequence of pairs indicating token positions in the verse.

        Decrement positions by 1 for zero-based indexing."""
        return {(src.position - 1, trg.position - 1) for ag in self.items for src in ag.sources for trg in ag.targets}

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


def verseid(ag: AlignmentGroup) -> str:
    """Return verse ID for grouping by verse."""
    return ag.identifier.split(".")[0]


class Reader(UserDict):
    """Read alignment data and integrate source and target."""

    # def __init__(self, sourceid: str, targetid: str, languageid: str, processid: str) -> None:
    def __init__(self, configuration: config.Configuration) -> None:
        """Initialize Reader instance."""
        super().__init__(self)
        self.cfg = configuration
        self.sourcereader = gcsource.Reader(self.cfg)
        # these have all the source and target tokens
        self.sourcesbyverse = {
            bcvref: [pair[1] for pair in g]
            for bcvref, g in itertools.groupby(self.sourcereader.items(), lambda pair: pair[0][:8])
        }
        self.targetreader = gctarget.Reader(self.cfg)
        self.targetsbyverse = {
            bcvref: [pair[1] for pair in g]
            for bcvref, g in itertools.groupby(self.targetreader.items(), lambda pair: pair[0][:8])
        }
        self.data = self.read_alignments(self.cfg.alignmentspath)

    def read_alignments(self, alignmentspath: Path) -> dict[str, AlignmentGroup]:
        """Load alignment data from alignmentspath and return an AlignmentGroup dict.

        Also (re)computes dependent value alignmentsets.
        """
        # load all the alignments: not grouped by verse
        with alignmentspath.open(encoding="utf-8") as f:
            # have to side-effect self.data here for verse_groups()
            self.data = {
                agid: AlignmentGroup(identifier=agid, sourceitems=sourceitems, targetitems=targetitems, meta=metadict)
                for aldict in json.load(f)
                if (agid := aldict["id"])
                if (sourceitems := tuple([self.sourcereader[s] for s in aldict["source_ids"]]))
                if (targetitems := tuple([self.targetreader[t] for t in aldict["target_ids"]]))
                if (metadict := aldict["meta"])
            }
        # todo: group this by reference, then make dataframe a method
        # here with a reference paraneter so it can also access
        # sources/targetsbyverse.
        # BCV reference -> AlignmentSet
        # these only have the aligned sources and targets
        self.alignmentsets = {
            aset.verseid: aset for vg in self.verse_groups() if (aset := AlignmentSet.from_aglist(vg))
        }
        return self.data

    def display(self) -> None:
        """Display configuration information for a Reader."""
        print(f"Source:\t{self.cfg.sourceid}\t({len(self.sourcereader)} words)")
        print(f"Target:\t{self.cfg.targetid}\t({len(self.targetreader)} words)")
        print(f"Process:\t{self.cfg.processid}")
        print(f"{len(self)} alignments")

    def source_concordance(self, value: str, attr: str = "lemma") -> list[AlignmentGroup]:
        """Return alignment groups whose source attr value is value."""
        return [ag for ag in self.data.values() if value in [getattr(s, attr) for s in ag.sourceitems]]

    def verse_groups(self) -> list[list[AlignmentGroup]]:
        """Return a list of lists of AlignmentGroups, by verse."""
        return [list(g) for k, g in itertools.groupby(self.values(), verseid)]

    def write_references(self) -> None:
        """Write out references for AlignmentSets, one to a line."""
        # this could go in config
        referencespath = self.cfg.sourcepath.parent / "references" / f"{self.cfg.identifier}-refline.txt"
        with referencespath.open("w") as f:
            for aset in self.alignmentsets:
                f.write(f"{aset.usfm}\n")

    # ToDo:
    # - option for representing isPrimary on the target: maybe *bold*?
    def dataframe(self, verseid: str, hitmark: str = "-G-", missmark: str = "  ") -> pd.DataFrame:
        """Return a DataFrame showing alignments for verseid, a BCV reference.

        Target terms for column names, source terms for
        index. Alignments are indicated with the hitmark string:
        otherwise the missmark string is used.

        """
        # these are only the aligned tokens
        sources = [item.token for item in self.sourcesbyverse[verseid]]
        targets = [item.token for item in self.targetsbyverse[verseid]]
        df = pd.DataFrame(columns=targets, index=sources)
        goldcoords = self.alignmentsets[verseid].coordinates()
        for coord in goldcoords:
            df.iat[coord] = hitmark
        return df.fillna(value=missmark)
