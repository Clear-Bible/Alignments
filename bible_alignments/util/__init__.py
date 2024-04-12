"""Utilities for processing alignment data."""

from bible_alignments import ROOT, DATAPATH, SRCPATH

from .strongs import normalize_strongs

# from .vref import BibleReader, EngNTReader, EngOTReader, OrgNTReader, OrgOTReader, Reader

__all__ = [
    # bible_alignments
    "ROOT",
    "DATAPATH",
    "SRCPATH",
    # strongs
    "normalize_strongs",
]
