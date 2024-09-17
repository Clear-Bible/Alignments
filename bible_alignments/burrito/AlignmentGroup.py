"""Manage data for an alignment record.

This defines AlignmentGroup and supporting dataclasses.

This implements Scripture Burrito Alignment Standard, v 0.3,
https://docs.google.com/document/d/1zR5gsrm3gIoNiHVBlWz5_BBw3N-Ew1-4M5rMsFrPzSw/.

The information model allows some values at multiple levels due to
'hoisting'. This opinionated code:
- defines attributes at the lowest relevant class
- use maximal hoisting for serialization unless overridded

While this aims at generality, the main application supported here is
publishing Bible alignment data. There may therefore be aspects of the
spec that are not supported by this code.

"""

from dataclasses import dataclass, field, fields
import datetime as dt
from itertools import groupby
from typing import Any, Optional

from biblelib.word import bcvwpid

from bible_alignments import SourceidEnum

from .AlignmentType import TranslationType


# hoisting means this can be defined at several different levels, so
# called out as a separate class
@dataclass
class Document:
    """Manage data for an alignment document."""

    # best practices
    # - for source documents: a standard identifier like 'NA28' or
    #   "WLC"
    # - for target documents: a Version Abbreviation value from
    #   digitalbiblelibrary.org is a good choice.
    docid: str
    scheme: str = "BCVWP"
    # only set if a source ID
    sourceid: Optional[SourceidEnum] = None

    def __post_init__(self) -> None:
        """Compute values after initialization."""
        try:
            # set is_source if in the standard list
            self.sourceid = SourceidEnum(self.docid)
        except ValueError:
            self.sourceid = None
            # downgrade BCVWP to BCVW: no subword indices if not source
            if self.scheme == "BCVWP":
                self.scheme = "BCVW"

    def asdict(self) -> dict[str, Any]:
        """Return a dict of values suitable for serialization."""
        return {"docid": self.docid, "scheme": self.scheme}


@dataclass(order=True)
class AlignmentReference:
    """Manage data for an alignment reference."""

    # perhaps over-engineered, but Document data can occur at multiple
    # levels in serialization.
    document: Document
    # selectors identify tokens or other units in a document. For most
    # alignment purposes, these are token identifiers.
    selectors: list[str]

    def __post_init__(self) -> None:
        """Compute values after initialization."""
        # no good for reading alignment hub data
        # assert bool(self.selectors), "Selectors must not be empty."
        self.selectors = sorted(self.selectors)

    def __repr__(self) -> str:
        """Return a printed representation."""
        return f"<{self.docid}: {self.selectors}>"

    @property
    def docid(self) -> str:
        """Return the docid from document, for convenience."""
        return self.document.docid

    @property
    def scheme(self) -> str:
        """Return the scheme from document, for convenience."""
        return self.document.scheme

    @property
    def incomplete(self) -> bool:
        """True if any selectors are MISSING."""
        return any((sel == "MISSING") for sel in self.selectors)

    def asdict(self, hoist: bool = True) -> dict[str, Any]:
        """Return a dict of values suitable for serialization.

        With hoist, omit docid and scheme from document, assuming
        they'll be specified 'higher up'.

        """
        refdict: dict[str, Any] = {"selectors": self.selectors}
        if not hoist:
            refdict.update({"docid": self.docid, "scheme": self.scheme})
        return refdict


@dataclass
class Metadata:
    """Contains metadata for alignment records.

    While all attributes are optional, the attributes creator and
    created are strongly encouraged.

    Other attributes are taken from Dublin Core terms
    (https://www.dublincore.org/specifications/dublin-core/dcmi-terms/#section-2)
    to encourage standardization. This may also be extended to include
    other attributes.

    """

    # these initial attributes mirror DCMI, and typically apply to an
    # AlignmentGroup
    #
    # which version of the alignment spec this conforms to
    conformsTo: str = ""
    # "An entity responsible for making contributions to the
    # resource". Could be used for alignment annotators. If there are
    # multiple values, concatenate with commas.
    contributor: str = ""
    # strongly recommended if available: "Date of creation of the resource."
    created: Optional[dt.datetime] = None
    # strongly recommended if available: "An entity responsible for
    # making the resource."
    # Recommended usage: the organization providing the data.
    creator: str = ""
    # recommended standard values if defined: "NT", "OT", "DC", a USFM
    # abbreviation for Bible book
    coverage: str = ""
    # "An account of the resource."
    description: str = ""
    # for AlignmentRecords: unique identifier
    id: str = ""
    # for AlignmentRecords: how was this alignment originally created?
    # This does *not* capture changes to the original value.
    # common values include 'manual', 'automated' or an algorithm name
    origin: str = ""
    # for ClearAligner to track status. Output here should always be
    # 'created': set in Manager._make_record() so it's not set of AlignmentGroup metadata
    # eventually i may need to separate this into two classes, one for
    # Groups and one for Records.
    status: str = ""
    _fieldnames: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        """Compute values after initialization."""
        self._fieldnames = tuple(sorted(tuple([f.name for f in fields(self) if f.name != "_fieldnames"])))

    def __repr__(self) -> str:
        """Return a printed representation."""
        attrstr: str = " ".join({f"{f}={repr(fattr)}" for f in self._fieldnames if (fattr := getattr(self, f))})
        return f"Metadata({attrstr})"

    # no hoist option here: the caller decides
    def asdict(self) -> dict[str, Any]:
        """Return a dict of values for serialization."""
        metadict = {f: fattr for f in self._fieldnames if (fattr := getattr(self, f))}
        return metadict


@dataclass
class AlignmentRecord:
    """Manage data for an alignment record."""

    # metadata for this record only
    meta: Metadata
    # keys are roles, corresponding to type.roles
    references: dict[str, AlignmentReference]
    # TranslationType wires roles to 'source' and 'target'
    type: TranslationType = field(default_factory=TranslationType)

    def __post_init__(self) -> None:
        """Compute values after initialization."""
        for role in self.roles:
            assert role in self.references, f"role missing from references: {role}"
        assert len(self.roles) == len(self.references), "different numbers of roles and references"

    def __repr__(self) -> str:
        """Return a printed representation."""
        return f"<AlignmentRecord: {repr(self.references)}>"

    def __hash__(self) -> int:
        """Return a hash value for the record."""
        return hash(self.identifier)

    @property
    def identifier(self) -> str:
        """Return the identifier for this record, for convenience."""
        return self.meta.id

    @property
    def roles(self) -> tuple[str, str]:
        """Return the roles for this type, for convenience."""
        return self.type.roles

    def get_selectors(self, role: str) -> list[str]:
        """Return the list of selectors for role."""
        assert role in self.roles, f"Invalid role: {role}"
        return self.references[role].selectors

    @property
    def source_selectors(self) -> list[str]:
        """Return the source selectors for this record."""
        return self.get_selectors("source")

    @property
    def target_selectors(self) -> list[str]:
        """Return the target selectors for this record."""
        return self.get_selectors("target")

    @property
    def source_bcv(self) -> str:
        """Return the source BCV identifier for this record.

        Returns data for the first selector, though multiples should
        have the same BCV.

        """
        if self.source_selectors:
            firstbcv: str = [bcvwpid.to_bcv(sel) for sel in self.source_selectors][0]
            return firstbcv
        else:
            return ""

    @property
    def incomplete(self) -> bool:
        """True if any selectors in references are incomplete."""
        return any(ref.incomplete for ref in self.references.values())

    def asdict(self, positional: bool = False, withmeta: bool = True) -> dict[str, Any]:
        """Return a dict of values suitable for serialization.

        With positional=False (the default), returns a dict whose keys
        are the roles and values are the references. Otherwise, the
        single key is 'references', and the position is determined by
        the position of the roles.

        With withmeta=False (the default), omits record-level
        metadata: otherwise includes it.

        """
        recdict: dict[str, Any] = (
            {"references": self.references.items()}
            if positional
            else {role: ref.selectors for role, ref in self.references.items()}
        )
        if withmeta:
            recdict.update(
                {
                    "meta": self.meta.asdict(),
                }
            )
        return recdict


@dataclass
class AlignmentGroup:
    """Manage a full set of alignment records.

    This is opinionated about the composition of the group:
    - enforces a single type across all records
    """

    # same order and count as roles
    documents: tuple[Document, Document]
    # metadata for the group as a whole
    meta: Metadata
    records: list[AlignmentRecord]
    # keys to AlignmentRecord.references: same order as documents
    roles: tuple[str, str] = ("source", "targt")
    # either "ot" or "nt", based on documents.docid
    sourcedocid: str = ""
    canon: str = ""
    _type: str = ""
    # hoist docid values from reference.document up to this metadata
    _hoist_docid: bool = True

    def __post_init__(self) -> None:
        """Compute values and do checks after initialization."""
        # only a single type across all records
        typeset = {rec.type.type for rec in self.records if self.records}
        assert len(typeset) == 1, f"Multiple AlignmentRecord types found: {typeset}"
        self._type = typeset.pop()
        assert len(self.documents) == len(
            self.roles
        ), f"Must have same number of documents and roles: {self.documents}, {self.roles}"
        # one of the documents should have a non-null sourceid: use it
        # to set the canon for the group
        sourcedocid = self.documents[0].sourceid or self.documents[1].sourceid
        assert (
            sourcedocid
        ), f"Neither {self.documents[0].docid} nor {self.documents[1].docid} are recognized as source texts:\ncheck src/SourceidEnum for completeness."
        self.canon = sourcedocid.canon
        self.sourcedocid = sourcedocid.value

    def __repr__(self) -> str:
        """Return a printed representation."""
        docids: tuple[str, str] = tuple([doc.asdict()["docid"] for doc in self.documents])
        return f"<AlignmentGroup{docids}: {len(self.records)} records>"

    def asdict(self, hoist: bool = True) -> dict[str, Any]:
        """Return a dict of values suitable for serialization.

        This is opinionated about the preferred serialization: hoists
        as much as possible to upper levels.

        """
        # for now
        positional: bool = False
        withmeta: bool = False

        return {
            "meta": self.meta.asdict(),
            "type": self._type,
            "records": [rec.asdict(positional=positional, withmeta=withmeta) for rec in self.records],
        }

    def verserecords(self) -> dict[str, list[AlignmentRecord]]:
        """Return a dict mapping source BCV references to their alignment records."""
        verserecords: dict[str, list[AlignmentRecord]] = {
            k: list(g) for k, g in groupby(self.records, lambda r: r.source_bcv)
        }
        return verserecords
