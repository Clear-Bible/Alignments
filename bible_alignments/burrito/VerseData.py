"""Class for managing alignments and tokens at the verse level."""

from collections import Counter
from dataclasses import dataclass
from typing import Any

import pandas as pd


from .source import Source
from .target import Target


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

    def get_texts(self, typeattr: str = "targets", unique: bool = False) -> list[str]:
        """Return a list of text attributes for target or source items.

        With unique=True, add a numeric suffix as necessary to make
        each item unique. This means duplicated items will no longer
        be exact matches. The index is the position in the list of
        tokens.

        """
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
