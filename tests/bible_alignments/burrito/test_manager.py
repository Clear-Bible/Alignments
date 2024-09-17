"""Test manager.py and local imports."""

import pytest

from bible_alignments.burrito import DATAPATH, AlignmentSet, Manager, VerseData

# test published version
ENGLANGDATAPATH = DATAPATH / "eng"


@pytest.fixture
def sblgntbsb() -> AlignmentSet:
    """Return a AlignmentSet instance."""
    return AlignmentSet(
        sourceid="SBLGNT", targetid="BSB", targetlanguage="eng", langdatapath=ENGLANGDATAPATH, alternateid="manual"
    )


@pytest.fixture
def mgr(sblgntbsb: AlignmentSet) -> Manager:
    """Return a Manager instance."""
    mgr: Manager = Manager(sblgntbsb)
    return mgr


class TestManager:
    """Test manager.Manager()."""

    def test_init(self, mgr: Manager) -> None:
        """Test initialization."""
        assert mgr.alignmentset.sourceid == "SBLGNT"
        assert mgr.alignmentset.targetid == "BSB"
        assert mgr.sourceitems["n41004003001"].lemma == "ἀκούω"
        assert mgr.targetitems["41004003002"].text == "Listen"
        assert mgr.alignmentrecords["41004003.001"].asdict()["source"] == ["n41004003001", "n41004003002"]
        assert mgr.alignmentrecords["41004003.001"].meta.id == "41004003.001"
        assert mgr.alignmentrecords["41004003.001"].identifier == "41004003.001"
        vd43: VerseData = mgr["41004003"]
        assert vd43.alignments[0][0][0].lemma == "ἀκούω"
        assert vd43.get_texts() == ["“", "Listen", "!", "A", "farmer", "went", "out", "to", "sow", "his", "seed", "."]
        # happens to be the same
        assert vd43.get_texts(unique=True) == [
            "“",
            "Listen",
            "!",
            "A",
            "farmer",
            "went",
            "out",
            "to",
            "sow",
            "his",
            "seed",
            ".",
        ]
        assert vd43.get_texts(typeattr="sources") == ["Ἀκούετε", "ἰδοὺ", "ἐξῆλθεν", "ὁ", "σπείρων", "σπεῖραι"]


class TestWLCMManager:
    alset = AlignmentSet(sourceid="WLCM", targetid="BSB", targetlanguage="eng", langdatapath=ENGLANGDATAPATH)
    manager = Manager(alset)

    def test_init(self) -> None:
        """Test reading WLCM."""
        # target scheme should be downgraded
        # refactored
        # assert self.manager.targetdoc.scheme == "BCVW"
        assert self.alset.sourceid == "WLCM"
        assert self.alset.targetid == "BSB"


# Should add tests for Reason/BadRecord
