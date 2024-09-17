"""Configure and run manager to read Burrito alignment data.

Given an alignment set, read the data on file into internal
representations.

This assumes you know what alignment set you're looking for, and that
the data already exists in Scripture Burrito format. Alignment sets
are identified by a language (code), target and source IDs, and a path to the data.

>>> from bible_alignments.burrito import DATAPATH, Manager, AlignmentSet
# your local copy of e.g. Hindi data
>>> targetlang = "hin"
>>> alset = AlignmentSet(targetlanguage=targetlang, targetid="IRVHin", sourceid="SBLGNT", langdatapath=(DATAPATH / targetlang))
>>> mgr = Manager(alset)
>>> mgr["40001024"]
<VerseData: 40001024>

"""

from collections import UserDict
from dataclasses import dataclass
from enum import Enum
from itertools import groupby
import json
from typing import Any, Callable, Optional

from .AlignmentGroup import Document, Metadata, AlignmentGroup, AlignmentReference, AlignmentRecord
from .AlignmentSet import AlignmentSet
from .BadRecord import BadRecord, Reason
from .VerseData import VerseData
from .alignments import AlignmentsReader
from .source import Source, SourceReader
from .target import Target, TargetReader
from .util import groupby_bcv


# create a Manager class to read data into AlignmentGroup instances
# and write them out to files
class Manager(UserDict):
    """Manage data read from Burrito files.

    self is a dict of BCV identifiers -> VerseData instances.
    """

    tokentypeattrs: set[str] = {"source", "target"}
    # the keys under self.bcv
    bcvkeys: tuple[str] = ("sources", "targets", "target_sourceverses", "records", "versedata")

    def __init__(
        self,
        alignmentset: AlignmentSet,
        creator: str = "GrapeCity",
        keeptargetwordpart: bool = False,
        # if True, don't remove bad records
        keepbadrecords: bool = False,
    ) -> None:
        """Initialize a Manager instance for an AlignmentSet.

        With keeptargetwordpart = False (the default), drop a 12th character
        representing the part index for a target token
        ID. keeptargetwordpart does not affect source token identifiers.

        """
        super().__init__()
        self.keeptargetwordpart: bool = keeptargetwordpart
        self.keepbadrecords: bool = keepbadrecords
        # # bad records when processing JSON: set in _make_record
        # self.badrecords: Optional[dict[str, BadRecord]] = {}
        # set in _clean_alignmentrecords
        self.badrecords: Optional[dict[str, BadRecord]] = {}
        # the configuration of alignment data
        self.alignmentset: AlignmentSet = alignmentset
        print(self.alignmentset.displaystr)
        # refactored code: leave bad record checking here, since that
        # also needs source/target TSVs
        alreader: AlignmentsReader = AlignmentsReader(
            alignmentset=self.alignmentset, keeptargetwordpart=self.keeptargetwordpart
        )
        self.alignmentgroup: AlignmentGroup = alreader.read_alignments()
        # keys are token identifiers from source/manuscript data
        self.sourceitems: SourceReader = self.read_sources()
        self.targetitems: TargetReader = self.read_targets()
        # several sets of data, all grouped by BCV
        self.bcv = {
            # The source and target token readers with the TSV data
            "sources": groupby_bcv(list(self.sourceitems.values())),
            "targets": groupby_bcv(list(self.targetitems.values())),
            # by source_verse attribute: this should coordinate with source
            "target_sourceverses": groupby_bcv(list(self.targetitems.values()), bcvfn=lambda t: t.source_verse),
        }
        # The individual AlignmentRecords for convenience: you'll
        # often want them by BCV though
        alrec: dict[str, AlignmentRecord] = {arec.meta.id: arec for arec in self.alignmentgroup.records}
        # drop badrecords: this means
        # alignmentrecords will be smaller than
        # alignmentgroup.records, but will omit some bad data.
        self.alignmentrecords = self._clean_alignmentrecords(alrec)
        if self.badrecords:
            # update alignmentgroup with the right set of records
            self.alignmentgroup.records = list(self.alignmentrecords.values())
        # group sources/targets by verse: they're not all included in alignments
        # group alignment records by bcv
        self.bcv["records"]: dict[str, list[AlignmentRecord]] = groupby_bcv(
            list(self.alignmentrecords.values()), lambda r: r.source_bcv
        )
        # and make VerseData instances
        self.bcv["versedata"] = {
            bcvid: self.make_versedata(bcvid, self.bcv["records"]) for bcvid in self.bcv["records"]
        }
        self.data = self.bcv["versedata"]
        self.check_integrity()

    def _bad_reason(self, arec: AlignmentRecord) -> Optional[BadRecord]:
        """Return a reason instance if the alignment record is malformed, or ''.

        Optionally add a tuple of supporting data.
        """
        # these labels must match what's in BadRecord._reasons
        arecdict = arec.asdict()
        badrecdict = {"identifier": arec.identifier, "record": arec}
        if not arecdict["source"]:
            return BadRecord(**badrecdict, reason=Reason.NOSOURCE)
        elif "" in arecdict["source"]:
            return BadRecord(**badrecdict, reason=Reason.EMPTYSOURCE)
        elif not (arecdict["target"]):
            return BadRecord(**badrecdict, reason=Reason.NOTARGET)
        elif "" in arecdict["target"]:
            return BadRecord(**badrecdict, reason=Reason.EMPTYTARGET)
        elif any([(tok not in self.sourceitems) for tok in arecdict["source"]]):
            missing = [tok for tok in arecdict["source"] if tok not in self.sourceitems]
            return BadRecord(**badrecdict, reason=Reason.MISSINGSOURCE, data=missing)
        elif any([(tok not in self.targetitems) for tok in arecdict["target"]]):
            missing = [tok for tok in arecdict["target"] if tok not in self.targetitems]
            if set(arecdict["target"]).symmetric_difference(set(missing)):
                return BadRecord(**badrecdict, reason=Reason.MISSINGTARGETSOME, data=missing)
            else:
                return BadRecord(**badrecdict, reason=Reason.MISSINGTARGETALL, data=missing)
        else:
            return None

    def _clean_alignmentrecords(self, alrec) -> dict[str, AlignmentRecord]:
        """Find bad alignment records, return good ones."""
        self.badrecords: Optional[dict[str, BadRecord]] = {
            recid: badrec for recid, arec in alrec.items() if (badrec := self._bad_reason(arec)) if badrec
        }
        if self.badrecords:
            keepmsg = "Keeping" if self.keepbadrecords else "Dropping"
            print(f"{keepmsg} {len(self.badrecords)} bad alignment records. Instances in self.badrecords.")
            for reason in Reason:
                rcount = len([mal for mal in self.badrecords.values() if mal.reason == reason])
                if rcount:
                    print(f"{reason.value}\t{rcount}")
        # drop them from alignmentrecords, unless keeping them
        if self.keepbadrecords:
            return alrec
        else:
            return {recid: badrec for recid, badrec in alrec.items() if recid not in self.badrecords}

    def read_sources(self) -> SourceReader:
        """Read source data into SourceReader."""
        return SourceReader(self.alignmentset.sourcepath)

    def read_targets(self) -> TargetReader:
        """Read target data into TargetReader."""
        # may need more single-name target files
        return TargetReader(self.alignmentset.targetpath, keepwordpart=self.keeptargetwordpart)

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
            sources=self.bcv["sources"].get(bcvid, []),
            targets=self.bcv["targets"].get(bcvid, []),
        )

    def display_record(self, alrec: AlignmentRecord) -> None:
        """Print a display for an AlignmentRecord for debugging."""
        print(f"{alrec.meta.id} ------------")
        for src in alrec.source_selectors:
            print(f"Source: {self.sourceitems[src]._display if src else 'None'}")
        for trg in alrec.target_selectors:
            print(f"Target: {self.targetitems[trg]._display if trg else 'None'}")

    def check_integrity(self) -> None:
        """Check the data and print messages for any problems."""
        if len(self.bcv["records"]) != len(self.bcv["versedata"]):
            print(f"{len(self.bcv['records'])} BCV records != {len(self.bcv['versedata'])} VerseData instances.")
        if len(self.bcv["sources"]) < len(self.bcv["records"]):
            print(f"{len(self.bcv['sources'])} BCV sources < {len(self.bcv['records'])} records.")

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
