"""Code for working with alignment data in Scripture Burrito format."""

from bible_alignments import ROOT, DATAPATH, SRCPATH

from .AlignmentGroup import Document, Metadata, AlignmentReference, AlignmentRecord, AlignmentGroup

# probably don't need the other types
from .AlignmentType import TranslationType
from .catalog import AlignmentSet, Catalog
from .manager import Manager, VerseData
from .source import Source, SourceReader
from .target import Target, TargetReader

# for output
ALIGNMENTSROOT = ROOT.parent / "Alignments"
REFERENCESPATH = ALIGNMENTSROOT / "data/sources/references"


__all__ = [
    "ROOT",
    "DATAPATH",
    "SRCPATH",
    "ALIGNMENTSROOT",
    "REFERENCESPATH",
    # AlignmentGroup
    "Document",
    "Metadata",
    "AlignmentReference",
    "AlignmentRecord",
    "AlignmentGroup",
    # AlignmentType
    "TranslationType"
    # catalog
    "AlignmentSet",
    "Catalog",
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
