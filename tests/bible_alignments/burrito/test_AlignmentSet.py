"""Test code in src.burrito.AlignmentSet."""

import pytest

from bible_alignments import DATAPATH, SOURCES
from bible_alignments.burrito import AlignmentSet

ENGLANGDATAPATH = DATAPATH.parent.parent / "alignments-eng/data"
HINLANGDATAPATH = DATAPATH.parent.parent / "alignments-hin/data"


@pytest.fixture
def aset() -> AlignmentSet:
    """Return a AlignmentSet instance."""
    return AlignmentSet(
        sourceid="SBLGNT", targetid="LEB", targetlanguage="eng", langdatapath=ENGLANGDATAPATH, alternateid="manual"
    )


@pytest.fixture
def asethin() -> AlignmentSet:
    """Return a AlignmentSet instance for IRVHin."""
    return AlignmentSet(
        sourceid="SBLGNT", targetid="IRVHin", targetlanguage="hin", langdatapath=HINLANGDATAPATH, alternateid="manual"
    )


class TestAlignmentSet:
    """Test the AlignmentSet class."""

    def test_init(self, aset: AlignmentSet) -> None:
        """Test the constructor."""
        assert aset.identifier == "SBLGNT-LEB-manual"
        assert aset.sourcedatapath == SOURCES
        assert aset.canon == "nt"

    def test_canon(self) -> None:
        """Test the canon property."""
        wlc = AlignmentSet(
            sourceid="WLC", targetid="LEB", targetlanguage="eng", langdatapath=ENGLANGDATAPATH, alternateid="manual"
        )
        assert wlc.canon == "ot"
        # should also test X value for not nt or ot

    def test_sourceid(self) -> None:
        """Test the constructor with various id values."""
        with pytest.raises(ValueError):
            AlignmentSet(sourceid="SBLGNT!", targetid="LEB", targetlanguage="eng")
        with pytest.raises(ValueError):
            AlignmentSet(sourceid="SBL-GNT", targetid="LEB", targetlanguage="eng")
        with pytest.raises(ValueError):
            AlignmentSet(sourceid="SBL.GNT", targetid="LEB", targetlanguage="eng")

    def test_noalternateid(self) -> None:
        """Test the constructor without alternateid value."""
        cat = AlignmentSet(sourceid="SBLGNT", targetid="LEB", targetlanguage="eng")
        assert cat.identifier == "SBLGNT-LEB"

    def test_paths(self, aset: AlignmentSet) -> None:
        """Test the source, target, alignment, and TOML paths."""
        assert aset.sourcepath == SOURCES / "SBLGNT.tsv"
        assert aset.targetpath == ENGLANGDATAPATH / "targets/LEB/nt_LEB.tsv"
        # assert aset.langtargetdirpath == DATAPATH / "alignments/eng/LEB"
        assert aset.alignmentpath == ENGLANGDATAPATH / "alignments/LEB/SBLGNT-LEB-manual.json"
        assert aset.tomlpath == ENGLANGDATAPATH / "alignments/LEB/SBLGNT-LEB-manual.toml"


class TestAlignmentSetHin:
    """Test the AlignmentSet class for Hindi."""

    def test_init(self, asethin: AlignmentSet) -> None:
        """Test the constructor."""
        assert asethin.identifier == "SBLGNT-IRVHin-manual"
        assert asethin.sourcedatapath == SOURCES
        assert asethin.canon == "nt"

    def test_canon(self, asethin: AlignmentSet) -> None:
        """Test the canon property."""
        assert asethin.canon == "nt"
        # should also test X value for not nt or ot

    def test_paths(self, asethin: AlignmentSet) -> None:
        """Test the source, target, alignment, and TOML paths."""
        assert asethin.sourcepath == SOURCES / "SBLGNT.tsv"
        assert asethin.targetpath == HINLANGDATAPATH / "targets/IRVHin/nt_IRVHin.tsv"
        # assert asethin.langtargetdirpath == DATAPATH / "alignments/IRVHin"
        assert asethin.alignmentpath == HINLANGDATAPATH / "alignments/IRVHin/SBLGNT-IRVHin-manual.json"
        assert asethin.tomlpath == HINLANGDATAPATH / "alignments/IRVHin/SBLGNT-IRVHin-manual.toml"
