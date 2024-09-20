"""Test code in burrito.AlignmentRecord

Does not test writing files.
"""

import pytest

from bible_alignments.burrito import Metadata, Document, AlignmentReference, AlignmentRecord, AlignmentGroup


@pytest.fixture
def groupmeta() -> Metadata:
    """Return a Metadata instance."""
    return Metadata(creator="GrapeCity")


@pytest.fixture
def recordmeta() -> Metadata:
    """Return a Metadata instance."""
    return Metadata(origin="manual", status="created", id="0708e5ff-2fd1-407b-97df-57f77f0d4a5f")


@pytest.fixture
def document() -> Document:
    """Return a Document instance with default scheme."""
    return Document(docid="SBLGNT")


@pytest.fixture
def documentwlcm() -> Document:
    """Return a Document instance with default scheme."""
    return Document(docid="WLCM")


@pytest.fixture
def reference_sblgnt(document: Document) -> AlignmentReference:
    """Return a AlignmentReference instance for SBLGNT."""
    return AlignmentReference(document=document, selectors=["n41004003001", "n41004003002"])


@pytest.fixture
def reference_wlcm(documentwlcm: Document) -> AlignmentReference:
    """Return a AlignmentReference instance for SBLGNT."""
    return AlignmentReference(document=documentwlcm, selectors=["o01004003001", "o01004003002"])


@pytest.fixture
def reference_bsb(document: Document) -> AlignmentReference:
    """Return a AlignmentReference instance for BSB."""
    return AlignmentReference(document=Document(docid="BSB"), selectors=["410040030021"])


@pytest.fixture
def reference_bsb_ot(document: Document) -> AlignmentReference:
    """Return a AlignmentReference instance for BSB."""
    return AlignmentReference(document=Document(docid="BSB"), selectors=["010040030021"])


@pytest.fixture
def record(
    recordmeta: Metadata, reference_sblgnt: AlignmentReference, reference_bsb: AlignmentReference
) -> AlignmentRecord:
    """Return a AlignmentReference instance."""
    return AlignmentRecord(
        meta=recordmeta,
        references={"source": reference_sblgnt, "target": reference_bsb},
    )


@pytest.fixture
def recordwlcm(
    recordmeta: Metadata, reference_wlcm: AlignmentReference, reference_bsb_ot: AlignmentReference
) -> AlignmentRecord:
    """Return a AlignmentReference instance."""
    return AlignmentRecord(
        meta=recordmeta,
        references={"source": reference_wlcm, "target": reference_bsb_ot},
    )


@pytest.fixture
def group(groupmeta: Metadata, record: AlignmentRecord) -> AlignmentGroup:
    """Return a AlignmentGroup instance."""
    return AlignmentGroup(
        documents=(Document(docid="SBLGNT"), Document(docid="BSB")),
        meta=groupmeta,
        records=[record],
        roles=("source", "target"),
    )


# empty case just for testing TopLevelGroups
@pytest.fixture
def groupwlcm(groupmeta: Metadata, recordwlcm: AlignmentRecord) -> AlignmentGroup:
    """Return a AlignmentGroup instance."""
    return AlignmentGroup(
        documents=(Document(docid="WLCM"), Document(docid="BSB")),
        meta=groupmeta,
        records=[recordwlcm],
        roles=("source", "target"),
    )


class TestMetadataGroup:
    """Test Metadata()."""

    def test_init(self, groupmeta: Metadata) -> None:
        """Test initialization."""
        assert groupmeta.creator == "GrapeCity"
        assert not groupmeta.created
        assert "_fieldnames" not in groupmeta._fieldnames

    def test_asdict(self, groupmeta: Metadata) -> None:
        """Test asdict()."""
        metadict = groupmeta.asdict()
        assert "creator" in metadict
        assert groupmeta.asdict() == {"creator": "GrapeCity"}
        with pytest.raises(AssertionError):
            assert "created" in metadict


class TestDocument:
    """Test Document()."""

    def test_init(self, document: Document) -> None:
        """Test initialization."""
        assert document.docid == "SBLGNT"
        # Group should downgrade this to BCVW but that's not here
        assert document.scheme == "BCVWP"
        assert document.sourceid.canon == "nt"

    def test_wlcm(self) -> None:
        doc = Document(docid="WLCM")
        assert doc.scheme == "BCVWP"
        assert doc.sourceid.canon == "ot"

    def test_bsb(self) -> None:
        doc = Document(docid="BSB")
        # downgraded scheme
        assert doc.scheme == "BCVW"
        assert doc.sourceid is None


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
        assert record.meta.asdict() == {
            "id": "0708e5ff-2fd1-407b-97df-57f77f0d4a5f",
            "origin": "manual",
            "status": "created",
        }
        assert record.__hash__() == hash("0708e5ff-2fd1-407b-97df-57f77f0d4a5f")
        assert "source" in record.roles
        # the source
        source = record.references["source"]
        assert source.docid == "SBLGNT"
        assert source.scheme == "BCVWP"

    def test_incomplete(self, recordmeta: Metadata, reference_bsb: AlignmentReference, record: AlignmentRecord) -> None:
        """Test incomplete."""
        assert not record.incomplete
        alrec = AlignmentRecord(
            meta=recordmeta,
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
        assert "source" in group.roles
        assert group.meta.creator == "GrapeCity"
        assert group.canon == "nt"
        assert isinstance(group.records, list)
        assert isinstance(group.records[0], AlignmentRecord)

    def test_asdict(self, group: AlignmentGroup) -> None:
        """Test asdict()."""
        recdict = group.asdict()
        assert len(recdict) == 3
        for k in ["meta", "type", "records"]:
            assert k in recdict
