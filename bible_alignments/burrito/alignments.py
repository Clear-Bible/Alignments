"""Read alignments data.

This provides support for manager.Manager to read the combination of source, target, and alignment data.

>>> from bible_alignments.burrito import DATAPATH, AlignmentSet, alignments
# your local copy of e.g. Hindi data
>>> targetlang = "hin"
>>> alset = AlignmentSet(targetlanguage=targetlang, targetid="IRVHin", sourceid="SBLGNT", langdatapath=(DATAPATH / targetlang))
>>> algroup = alignments.AlignmentsReader(alset).read_alignments()
"""

import json
from typing import Any, Optional


from .AlignmentGroup import Document, Metadata, AlignmentGroup, AlignmentReference, AlignmentRecord
from .AlignmentSet import AlignmentSet
from .AlignmentType import TranslationType


class AlignmentsReader:
    """Read alignments data from a JSON file.

    This does not check for bad records: use manager.Manager for
    robustness.

    """

    scheme = "BCVWP"
    altype: TranslationType = TranslationType()

    def __init__(self, alignmentset: AlignmentSet, keeptargetwordpart: bool = False) -> None:
        """Initialize a Reader instance."""
        self.keeptargetwordpart: bool = keeptargetwordpart
        # the configuration of alignment data
        self.alignmentset: AlignmentSet = alignmentset
        # Document instances for AlignmentGroup
        self.sourcedoc: Document = Document(docid=self.alignmentset.sourceid, scheme=self.scheme)
        self.targetdoc: Document = Document(docid=self.alignmentset.targetid, scheme=self.scheme)
        # Read the data and instantiate an AlignmentGroup (with
        # AlignmentRecords, etc. all the way down)
        self.alignmentgroup: AlignmentGroup = self.read_alignments()
        # can't do all the checking without sources, targets, etc. Use
        # manager.Manager to read the data and collect any bad records
        # if you're not sure about it.

    def _targetid(self, targetid: str) -> str:
        """Return a normalized target ID.

        With self.keeptargetwordpart = False, drop the last digit.
        """
        if not self.keeptargetwordpart and len(targetid) == 12:
            return targetid[:11]
        else:
            return targetid

    def _make_record(self, alrec: dict[str, Any]) -> Optional[AlignmentRecord]:
        """Process a single alignment record.

        Many assumptions are encoded here that probably work for
        GrapeCity data, but not necessarily others.

        """
        metadatadict = alrec["meta"]
        # upgrade patch: 0.2.1 spec renames 'process' as 'origin'
        if "process" in metadatadict:
            metadatadict["origin"] = metadatadict["process"]
            del metadatadict["process"]
        # add a missing status value; retain an existing one
        metadatadict["status"] = metadatadict["status"] if "status" in metadatadict else "created"
        meta: Metadata = Metadata(**metadatadict)
        # if no source selectors, can't compute BCV keys later, which
        # messes up later processes. So drop any record with no source
        # selectors here
        if not alrec["source"]:
            print(f"No source selectors for {alrec['meta']['id']}: dropping the record, adding to self.badrecords.")
        sourceref: AlignmentReference = AlignmentReference(document=self.sourcedoc, selectors=alrec["source"])
        # bad hack here to drop word parts
        trgselectors = [self._targetid(trgid) for trgid in alrec["target"]]
        targetref: AlignmentReference = AlignmentReference(document=self.targetdoc, selectors=trgselectors)
        return AlignmentRecord(meta=meta, references={"source": sourceref, "target": targetref}, type=self.altype)

    def read_alignments(self) -> AlignmentGroup:
        """Read JSON alignments data and return an AlignmentGroup."""
        with self.alignmentset.alignmentpath.open("rb") as f:
            agroupdict = json.load(f)
            if isinstance(agroupdict, list):
                raise ValueError(
                    f"{self.alignmentspath} should contain an object, not a list. Perhaps not converted to Burrito"
                    " format yet?"
                )
            meta: Metadata = Metadata(**agroupdict["meta"])
            # assumes default TranslationType to match self.altype,
            # and one value for the whole group: true for GC data, not
            # necessarily others
            assert agroupdict["type"] == self.altype.type, f"Unexpected alignment type: {agroupdict['type']}"
            records: list[AlignmentRecord] = [
                record for alrec in agroupdict["records"] if (record := self._make_record(alrec)) if record
            ]
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
