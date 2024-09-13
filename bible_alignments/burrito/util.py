"""Utilities used for burrito data.


>>> from bible_alignments.burrito import util

# group target tokens by verse
>>> from bible_alignments.burrito import DATAPATH, target
>>> tr = target.TargetReader(DATAPATH / "targets/swh/nt_ONEN.tsv", idheader="id")
vd = util.groupby_bcv(tr.values())
"""

from itertools import groupby
from typing import Any, Callable

from .BaseToken import BaseToken


def groupby_bcv(values: list[Any], bcvfn: Callable = BaseToken.to_bcv) -> dict[str, list[Any]]:
    """Group a list of tokens into a dict by their BCV values."""
    return {k: list(g) for k, g in groupby(values, bcvfn)}
