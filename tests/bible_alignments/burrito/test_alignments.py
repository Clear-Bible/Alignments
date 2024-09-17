"""Test AlignmentsReader."""

import pytest

from bible_alignments.burrito import DATAPATH, AlignmentSet, AlignmentsReader, AlignmentRecord

# test internal version
ENGLANGDATAPATH = DATAPATH.parent.parent / "alignments-eng/data"


@pytest.fixture
def sblgntbsb() -> AlignmentSet:
    """Return a AlignmentSet instance."""
    return AlignmentSet(
        sourceid="SBLGNT", targetid="BSB", targetlanguage="eng", langdatapath=ENGLANGDATAPATH, alternateid="manual"
    )


@pytest.fixture
def alreader(sblgntbsb: AlignmentSet) -> AlignmentsReader:
    """Return a AlignmentsReader instance."""
    return AlignmentsReader(sblgntbsb)


class TestAlignmentsReader:
    """Test AlignmentsReader()."""

    def test_init(self, alreader: AlignmentsReader) -> None:
        """Test initialization."""
        assert alreader.scheme == "BCVWP"
        assert alreader.sourcedoc.docid == "SBLGNT"
        assert alreader.targetdoc.docid == "BSB"
        algroup = alreader.alignmentgroup
        alrec: dict[str, AlignmentRecord] = {arec.meta.id: arec for arec in algroup.records}
        assert alrec["41004003.001"].asdict()["source"] == ["n41004003001", "n41004003002"]
        assert alrec["41004003.001"].meta.id == "41004003.001"
        assert alrec["41004003.001"].identifier == "41004003.001"
