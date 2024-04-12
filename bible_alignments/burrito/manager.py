"""Configure and run manager to read Burrito alignment data.

Given an alignment set, read the data on file into internal
representations.

This assumes you know what alignment set you're looking for, and that
the data already exists in Scripture Burrito format. Alignment sets
are identified by a language (code) and an alignment set identifier
like 'SBLGNT-BSB-manual'. See catalog.py for help.



>>> from bible_alignments.burrito import Manager, Catalog
>>> alset = Catalog().get_alignmentset(language="eng", identifier="SBLGNT-BSB-manual")
>>> mgr = Manager(alset)
>>> mgr.versedata["40001024"]
<VerseData: 40001024>

"""

from collections import UserDict
from itertools import groupby
import json
from typing import Any, Callable

from biblelib.word import bcvwpid

from .AlignmentGroup import Document, Metadata, AlignmentGroup, AlignmentReference, AlignmentRecord
from .AlignmentType import TranslationType
from .VerseData import VerseData
from .catalog import AlignmentSet
from .source import Source, SourceReader
from .target import Target, TargetReader


# create a Manager class to read data into AlignmentGroup instances
# and write them out to files
class Manager(UserDict):
    """Manage data read from Burrito files."""

    scheme = "BCVWP"
    altype: TranslationType = TranslationType()
    # keys are token identifiers from source/manuscript data
    sourceitems: UserDict[str, Source] = UserDict()
    targetitems: UserDict[str, Target] = UserDict()

    def __init__(self, alset: AlignmentSet, creator: str = "GrapeCity") -> None:
        """Initialize a Manager instance for an AlignmentSet."""
        super().__init__()
        self.alset: AlignmentSet = alset
        print(self.alset.displaystr)
        self.sourcedoc: Document = Document(docid=self.alset.sourceid, scheme=self.scheme)
        self.targetdoc: Document = Document(docid=self.alset.targetid, scheme=self.scheme)
        self.alignmentgroup: AlignmentGroup = self.read_alignments()
        self.alignmentrecords: dict[str, AlignmentRecord] = {arec.meta.id: arec for arec in self.alignmentgroup.records}
        self.sourceitems: SourceReader = self.read_sources()
        self.targetitems: TargetReader = self.read_targets()
        # drop malaligned records
        self.alignmentrecords = self._clean_alignmentrecords()
        # self.verserecords = {k: list(g) for k, g in groupby(self.alignmentrecords.values(), lambda r: r.source_bcv)}
        # group sources/targets by verse: they're not all included in alignments
        # need to handle versification here?
        self.versesources = self.groupby_bcv(list(self.sourceitems.values()))
        self.versetargets = self.groupby_bcv(list(self.targetitems.values()))
        # group by bcv and make VerseData instances
        self.verserecords: dict[str, list[AlignmentRecord]] = self.groupby_bcv(
            list(self.alignmentrecords.values()), lambda r: r.source_bcv
        )
        self.data = {bcvid: self.make_versedata(bcvid, self.verserecords) for bcvid in self.verserecords}

    def _bad_record(self, arec: AlignmentRecord) -> bool:
        """Return True if the alignment record is malformed."""
        arecdict = arec.asdict()
        return (
            not (arecdict["source"])
            or "" in arecdict["source"]
            or not (arecdict["target"])
            or "" in arecdict["target"]
            or any([(tok not in self.sourceitems) for tok in arecdict["source"]])
            or any([(tok not in self.targetitems) for tok in arecdict["target"]])
        )

    def _clean_alignmentrecords(self) -> dict[str, AlignmentRecord]:
        """Find bad alignment records, return good ones."""
        # malaligned if any empty source or target tokens
        self.malaligned: dict[str, AlignmentRecord] = {
            recid: arec for recid, arec in self.alignmentrecords.items() if self._bad_record(arec)
        }
        if self.malaligned:
            print(f"Dropping {len(self.malaligned)} bad alignment records. Instances in self.malaligned.")
        # drop them from alignmentrecords
        return {recid: arec for recid, arec in self.alignmentrecords.items() if recid not in self.malaligned}

    def _make_record(self, alrec: dict[str, Any]) -> AlignmentRecord:
        """Process a single alignment record.

        Many assumptions are encoded here that probably work for
        GrapeCity data, but not necessarily others.

        """
        meta: Metadata = Metadata(**alrec["meta"])
        sourceref: AlignmentReference = AlignmentReference(document=self.sourcedoc, selectors=alrec["source"])
        targetref: AlignmentReference = AlignmentReference(document=self.targetdoc, selectors=alrec["target"])
        return AlignmentRecord(meta=meta, references={"source": sourceref, "target": targetref}, type=self.altype)

    def read_alignments(self) -> AlignmentGroup:
        """Read alignment data into AlignmentGroup."""
        with self.alset.alignmentpath.open("rb") as f:
            agroupdict = json.load(f)
            if isinstance(agroupdict, list):
                raise ValueError(
                    f"{self.alset.alignmentpath} should contain an object, not a list. Perhaps not converted to Burrito"
                    " format yet?"
                )
            meta: Metadata = Metadata(**agroupdict["meta"])
            # assumes default TranslationType to match self.altype,
            # and one value for the whole group: true for GC data, not
            # necessarily others
            assert agroupdict["type"] == self.altype.type, f"Unexpected alignment type: {agroupdict['type']}"
            records: list[AlignmentRecord] = [self._make_record(alrec) for alrec in agroupdict["records"]]
            return AlignmentGroup(
                documents=(
                    self.sourcedoc,
                    self.targetdoc,
                ),
                meta=meta,
                records=records,
                # should be the same throughout
                roles=records[0].roles,
            )

    def read_sources(self) -> SourceReader:
        """Read source data into SourceReader."""
        # once we get single-name source files
        return SourceReader(self.alset.sourcepath)
        # return SourceReader(self.alset.sourcepath.with_name(f"{self.alset.sourceid}-{self.alset.targetid}.tsv"))

    def read_targets(self) -> TargetReader:
        """Read target data into TargetReader."""
        # may need more single-name target files
        return TargetReader(self.alset.targetpath)

    # replace with version in util?
    def groupby_bcv(self, values: list[Any], bcvfn: Callable = Source.to_bcv) -> dict[str, list[Any]]:
        """Group a list of tokens into a dict by their BCV values."""
        return {k: list(g) for k, g in groupby(values, bcvfn)}

    def make_versedata(self, bcvid: str, verserecords: dict[str, list[AlignmentRecord]]) -> VerseData:
        """Return a VerseData instance for a BCV reference."""
        alpairs: list[tuple[list[str], list[str]]] = [
            (ardict["source"], ardict["target"]) for ar in verserecords[bcvid] if (ardict := ar.asdict())
        ]
        alinstpairs: list[tuple[list[Source], list[Target]]] = [
            (sourceinst, targetinst)
            for sources, targets in alpairs
            # what does it mean if tok isn't in sourceinst?? SBLGNT-BSB data
            # drop tokens
            if (sourceinst := [self.sourceitems[tok] for tok in sources if tok in self.sourceitems])
            if (targetinst := [self.targetitems[tok] for tok in targets if tok in self.targetitems])
        ]
        return VerseData(
            bcvid=bcvid,
            alignments=alinstpairs,
            sources=self.versesources[bcvid] if bcvid in self.versesources else [],
            targets=self.versetargets[bcvid] if bcvid in self.versetargets else [],
        )

    def display_record(self, alrec: AlignmentRecord) -> None:
        """Print a display for an AlignmentRecord for debugging."""
        print(f"{alrec.meta.id} ------------")
        for src in alrec.source_selectors:
            print(f"Source: {self.sourceitems[src]._display if src else 'None'}")
        for trg in alrec.target_selectors:
            print(f"Target: {self.targetitems[trg]._display if trg else 'None'}")

    def token_alignments(
        self, term: str, role: str = "source", tokenattr: str = "text", lowercase: bool = False
    ) -> list[Source | Target]:
        """Return a list of alignments whose role tokens contain term."""
        itemreader: SourceReader | TargetReader = self.sourceitems if role == "source" else self.targetitems
        tokendict: dict[str, Source | Target] = {
            token.id: token for token in itemreader.term_tokens(term, tokenattr=tokenattr, lowercase=lowercase)
        }
        selectorset = set(tokendict)
        # collect alignment records that contain these tokens
        token_records = [rec for rec in self.alignmentgroup.records if selectorset.intersection(rec.source_selectors)]
        return token_records


"""
# if you need to re-output an instance `mgr` as conventionalized AlignmentHub, use
# gc2sb.manager.Manager
# don't confuse the two instances of Manager
>>> from src.gc2sb import Manager as gc2sbManager
>>> gc2sbmgr.write_alignment_group(group=mgr.alignmentgroup, alignpath=SOMEPATH)

"""
