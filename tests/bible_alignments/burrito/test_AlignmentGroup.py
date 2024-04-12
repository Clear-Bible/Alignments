"""Test code in bible_alignments.burrito.AlignmentRecord

Does not test writing files.
"""

import pytest

from bible_alignments.burrito import Metadata, Document, AlignmentReference, AlignmentRecord, AlignmentGroup


@pytest.fixture
def meta() -> Metadata:
    """Return a Metadata instance."""
    return Metadata(creator="GrapeCity")


@pytest.fixture
def document() -> Document:
    """Return a Document instance with default scheme."""
    return Document(docid="SBLGNT")


@pytest.fixture
def reference_sblgnt(document: Document) -> AlignmentReference:
    """Return a AlignmentReference instance for SBLGNT."""
    return AlignmentReference(document=document, selectors=["n41004003001", "n41004003002"])


@pytest.fixture
def reference_bsb(document: Document) -> AlignmentReference:
    """Return a AlignmentReference instance for BSB."""
    return AlignmentReference(document=Document(docid="BSB"), selectors=["410040030021"])


@pytest.fixture
def record(meta: Metadata, reference_sblgnt: AlignmentReference, reference_bsb: AlignmentReference) -> AlignmentRecord:
    """Return a AlignmentReference instance."""
    return AlignmentRecord(
        meta=meta,
        references={"source": reference_sblgnt, "target": reference_bsb},
    )


@pytest.fixture
def group(meta: Metadata, record: AlignmentRecord) -> AlignmentGroup:
    """Return a AlignmentGroup instance."""
    return AlignmentGroup(
        documents=(Document(docid="SBLGNT"), Document(docid="BSB")),
        meta=meta,
        records=[record],
        roles=("source", "targt"),
    )


class TestMetadata:
    """Test Metadata()."""

    def test_init(self, meta: Metadata) -> None:
        """Test initialization."""
        assert meta.creator == "GrapeCity"
        assert not meta.created
        assert "_fieldnames" not in meta._fieldnames

    def test_asdict(self, meta: Metadata) -> None:
        """Test asdict()."""
        metadict = meta.asdict()
        assert "creator" in metadict
        assert str(meta.asdict()) == "{'creator': 'GrapeCity'}"
        with pytest.raises(AssertionError):
            assert "created" in metadict


class TestDocument:
    """Test Document()."""

    def test_init(self, document: Document) -> None:
        """Test initialization."""
        assert document.docid == "SBLGNT"
        assert document.scheme == "BCVWP"


class TestReference:
    """Test Reference()."""

    def test_init(self, reference_sblgnt: AlignmentReference) -> None:
        """Test initialization."""
        assert reference_sblgnt.docid == "SBLGNT"
        assert reference_sblgnt.scheme == "BCVWP"
        assert "n41004003002" in reference_sblgnt.selectors
        # ensure selectors are sorted
        assert reference_sblgnt.selectors == ["n41004003001", "n41004003002"]

    def test_incomplete(self, reference_sblgnt: AlignmentReference) -> None:
        """Test incomplete."""
        assert not reference_sblgnt.incomplete
        alref = AlignmentReference(document=Document(docid="SBLGNT"), selectors=["n41004003001", "MISSING"])
        assert alref.incomplete

    def test_asdict_hoisted(self, reference_sblgnt: AlignmentReference) -> None:
        """Test asdict(hoist=True)."""
        refdict = reference_sblgnt.asdict()
        assert len(refdict) == 1
        assert set(refdict["selectors"]) == set(["n41004003001", "n41004003002"])

    def test_asdict_not_hoisted(self, reference_sblgnt: AlignmentReference) -> None:
        """Test asdict(hoist=False)."""
        refdict = reference_sblgnt.asdict(hoist=False)
        assert len(refdict) >= 3
        assert refdict["docid"] == "SBLGNT"
        assert refdict["scheme"] == "BCVWP"


class TestAlignmentRecord:
    """Test AlignmentRecord()."""

    def test_init(self, record: AlignmentRecord) -> None:
        """Test initialization."""
        #         assert "source" in ref.roles
        assert record.meta.creator == "GrapeCity"
        assert "source" in record.roles
        # the source
        source = record.references["source"]
        assert source.docid == "SBLGNT"
        assert source.scheme == "BCVWP"

    def test_incomplete(self, meta: Metadata, reference_bsb: AlignmentReference, record: AlignmentRecord) -> None:
        """Test incomplete."""
        assert not record.incomplete
        alrec = AlignmentRecord(
            meta=meta,
            references={
                "source": AlignmentReference(document=Document(docid="SBLGNT"), selectors=["n41004003001", "MISSING"]),
                "target": reference_bsb,
            },
        )

        assert alrec.incomplete

    def test_source_values(self, record: AlignmentRecord) -> None:
        """Test source_selectors and source_bcv."""
        assert record.source_selectors == ["n41004003001", "n41004003002"]
        assert record.source_bcv == "41004003"

    def test_asdict_positional(self, record: AlignmentRecord) -> None:
        """Test asdict()."""
        recdict = record.asdict(positional=True)
        # too fragile
        # assert len(recdict) == 1
        assert "references" in recdict
        assert len(recdict["references"]) == 2

    def test_asdict_default(self, record: AlignmentRecord) -> None:
        """Test asdict()."""
        recdict = record.asdict(positional=False)
        # too fragile
        # assert len(recdict) == 2
        for role in record.roles:
            assert role in recdict

    def test_asdict_withmeta(self, record: AlignmentRecord) -> None:
        """Test asdict()."""
        recdict = record.asdict(
            withmeta=True,
        )
        assert len(recdict) == 3
        for role in record.roles:
            assert role in recdict
        assert "meta" in recdict


class TestAlignmentGroup:
    """Test AlignmentGroup()."""

    def test_init(self, group: AlignmentGroup) -> None:
        """Test initialization."""
        #         assert "source" in ref.roles
        assert group.meta.creator == "GrapeCity"

    def test_asdict(self, group: AlignmentGroup) -> None:
        """Test asdict()."""
        recdict = group.asdict()
        assert len(recdict) == 3
        for k in ["meta", "type", "records"]:
            assert k in recdict
