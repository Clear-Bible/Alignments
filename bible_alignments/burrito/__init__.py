"""Code for working with alignment data in Scripture Burrito format."""

from bible_alignments import ROOT, DATAPATH, SRCPATH

from .AlignmentGroup import Document, Metadata, AlignmentReference, AlignmentRecord, AlignmentGroup

# probably don't need the other types
from .AlignmentType import TranslationType
from .AlignmentSet import AlignmentSet
from .manager import Manager, VerseData
from .BaseToken import BaseToken, asbool
from .source import Source, SourceReader
from .target import Target, TargetReader


__all__ = [
    "ROOT",
    "DATAPATH",
    "SRCPATH",
    # AlignmentGroup
    "Document",
    "Metadata",
    "AlignmentReference",
    "AlignmentRecord",
    "AlignmentGroup",
    # AlignmentSet
    "AlignmentSet",
    # AlignmentType
    "TranslationType",
    # BaseToken
    "BaseToken",
    "asbool",
    # manager
    "Manager",
    "VerseData",
    # source
    "Source",
    "SourceReader",
    # target
    "Target",
    "TargetReader",
    # "TargetWriter",
]
