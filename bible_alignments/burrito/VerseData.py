"""Class for managing alignments and tokens at the verse level."""

from collections import Counter
from dataclasses import dataclass
from enum import Enum
from typing import Any, Optional

import pandas as pd


from .source import Source
from .target import Target


class DiffReason(Enum):
    """Enumerate constants for alignment differences.."""

    DIFFLEN = "Different number of alignments"
    DIFFSOURCES = "Source selectors differ"
    DIFFTARGETS = "Target selectors differ"


@dataclass
class DiffRecord:
    """Container for data on alignment differences.


    The same verse could have multiple alignment differences.
    """

    # the alignment BCV
    bcvid: str
    # the data in the first alignment
    sources1: tuple[Source, ...]
    targets1: tuple[Target, ...]
    # the data in the second alignment
    sources2: tuple[Source, ...]
    targets2: tuple[Target, ...]
    # why it's different
    diffreason: DiffReason
    # any auxiliary data
    data: tuple = ()

    def __repr__(self) -> str:
        """Return a string representation."""
        basestr = f"<DiffRecord ({self.identifier}): '{self.diffreason.value}'"
        if self.data:
            basestr += ", " + repr(self.data)
        basestr += ">"
        return basestr


@dataclass
class VerseData:
    """Manage alignments, sources, and targets for a verse.

    Verse references are from the source. In a few cases, that means
    """

    # unique identifier for book, chapter, and verse
    bcvid: str
    alignments: list[tuple[list[Source], list[Target]]]
    sources: list[Source]
    targets: list[Target]
    _typeattrs = ["sources", "targets"]

    # def __post_init__(self) -> None:
    #     """Compute values after initialization."""
    #     pass

    def __repr__(self) -> str:
        """Return a string representation."""
        return f"<VerseData: {self.bcvid}>"

    def display(self, termsonly: bool = False) -> None:
        """Display the alignments in a readable view."""
        for sources, targets in self.alignments:
            print("------------")
            if termsonly:
                print(f"{list(src.text for src in sources)}-{list(trg.text for trg in targets)}")
            else:
                for src in sources:
                    print(f"Source: {src._display}")
                for trg in targets:
                    print(f"Target: {trg._display}")

    def table(self) -> None:
        """Display a tabbed table of alignments"""
        for sources, targets in self.alignments:
            print(" ".join([src.text for src in sources]), "\t", " ".join([trg.text for trg in targets]))

    def get_texts(self, typeattr: str = "targets", unique: bool = False) -> list[str]:
        """Return a list of text attributes for target or source items.

        With unique=True, add a numeric suffix as necessary to make
        each item unique. This means duplicated items will no longer
        be exact matches. The index is the position in the list of
        tokens.

        """
        assert typeattr in self._typeattrs, f"typeattr should be one of {self._typeattrs}"
        if unique:
            cnt: Counter = Counter()
            texts: list[str] = []
            for item in getattr(self, typeattr):
                itext = item.text
                if itext in cnt:
                    texts.append(f"{itext}.{cnt[itext]}")
                else:
                    texts.append(itext)
                cnt[itext] = cnt[itext] + 1
        else:
            texts = [item.text for item in getattr(self, typeattr)]
        return texts

    # no typing hints for pd.Dataframe
    def dataframe(self, hitmark: str = "-G-", missmark: str = "  ", srcattr: str = "text") -> Any:
        """Return a DataFrame showing alignments.

        Target terms for column names, source terms for
        index. Alignments are indicated with the hitmark string:
        otherwise the missmark string is used.

        """
        # dict mapping each target instance to aligned source instances
        target_sources = {trg: alpair[0] for alpair in self.alignments for trg in alpair[1]}
        # dict mapping
        dfdata = {
            textdisplay: [(hitmark if (src in target_sources.get(trg, {})) else missmark) for src in self.sources]
            for (index, alpair) in enumerate(self.alignments)
            if (targettextpair := zip(self.targets, self.get_texts("targets", unique=True)))
            for (trg, textdisplay) in targettextpair
        }
        # add source items as index
        return pd.DataFrame(dfdata, index=[getattr(src, srcattr) for src in self.sources])

    @staticmethod
    def _diff_pair(basedict: dict[str, str], pair: tuple[tuple[list[Source], list[Target]]]) -> Optional[DiffRecord]:
        """Compare an alignment pair of Source and Target."""
        if pair[0] != pair[1]:
            # assumes the order (source, target)
            sources1, targets1 = pair[0]
            sources2, targets2 = pair[1]
            if sources1 != sources2:
                return DiffRecord(**basedict, diffreason=DiffReason.DIFFSOURCES, data=(sources1, sources2))
            if targets1 != targets2:
                return DiffRecord(**basedict, diffreason=DiffReason.DIFFTARGETS, data=(targets1, targets2))
        else:
            return None

    def diff(self, other: "VerseData") -> Optional[list[DiffRecord]]:
        """Return a (possibly empty) list of differences between the alignments data.

        If there are a different number of alignments, that's the only
        difference reported. Otherwise compaires all the alignments,
        pairwise.

        """
        assert isinstance(other, VerseData), "Can only compare two VerseData instances."
        basedict = {"bcvid": self.bcvid}
        if len(self.alignments) != len(other.alignments):
            # no point continuing to compare here
            return [DiffRecord(**basedict, diffreason=DiffReason.DIFFLEN)]
        else:
            # use a list comprehension
            diffs: list[DiffRecord] = []
            for pair in zip(self.alignments, other.alignments):
                result = self._diff_pair(basedict, pair)
                if result:
                    diffs.append(result)
            return diffs
