"""Test code in bible_alignments.burrito.catalog."""

import pytest

from bible_alignments.burrito import AlignmentSet, Catalog, DATAPATH


@pytest.fixture
def aset() -> AlignmentSet:
    """Return a AlignmentSet instance."""
    return AlignmentSet(sourceid="SBLGNT", targetid="BSB", alternateid="manual", targetlanguage="eng")


class TestAlignmentSet:
    """Test the AlignmentSet class."""

    def test_init(self, aset: AlignmentSet) -> None:
        """Test the constructor."""
        assert aset.identifier == "SBLGNT-BSB-manual"
        assert aset.datapath == DATAPATH
        assert aset.canon == "nt"
        assert aset.check_files() == True

    def test_canon(self) -> None:
        """Test the canon property."""
        wlc = AlignmentSet(sourceid="WLC", targetid="BSB", alternateid="manual", targetlanguage="eng")
        assert wlc.canon == "ot"
        # should also test X value for not nt or ot

    def test_sourceid(self) -> None:
        """Test the constructor with various id values."""
        with pytest.raises(ValueError):
            AlignmentSet(sourceid="SBLGNT!", targetid="BSB", targetlanguage="eng")
        with pytest.raises(ValueError):
            AlignmentSet(sourceid="SBL-GNT", targetid="BSB", targetlanguage="eng")
        with pytest.raises(ValueError):
            AlignmentSet(sourceid="SBL.GNT", targetid="BSB", targetlanguage="eng")

    def test_noalternateid(self) -> None:
        """Test the constructor without alternateid value."""
        cat = AlignmentSet(sourceid="SBLGNT", targetid="BSB", targetlanguage="eng")
        assert cat.identifier == "SBLGNT-BSB"

    def test_paths(self, aset: AlignmentSet) -> None:
        """Test the source, target, alignment, and TOML paths."""
        assert aset.sourcepath == DATAPATH / "sources/SBLGNT.tsv"
        assert aset.targetpath == DATAPATH / "targets/eng/nt_BSB.tsv"
        assert aset.langtargetdirpath == DATAPATH / "alignments/eng/BSB"
        assert aset.alignmentpath == DATAPATH / "alignments/eng/BSB/SBLGNT-BSB-manual.json"
        assert aset.tomlpath == DATAPATH / "alignments/eng/BSB/SBLGNT-BSB-manual.toml"


class TestCatalog:
    """Test the Catalog class."""

    def test_init(self) -> None:
        """Test the constructor."""
        ctlg = Catalog()
        assert "eng" in ctlg.languages
        assert "SBLGNT-BSB-manual" in ctlg["eng"]
        assert ctlg["eng"]["SBLGNT-BSB-manual"].identifier == "SBLGNT-BSB-manual"
        assert ctlg.get_alignmentset(language="eng", identifier="SBLGNT-BSB-manual").identifier == "SBLGNT-BSB-manual"
        assert "arb" in ctlg.get_languages()
        assert "SBLGNT-BSB-manual" in ctlg.get_alignmentset_ids("eng")

    def test_nodata(self) -> None:
        """Test failing for no data."""
        ctlg = Catalog()
        with pytest.raises(AssertionError):
            # wrong language
            ctlg.get_alignmentset(language="eng", identifier="NA28-HSB-manual")
        with pytest.raises(AssertionError):
            # wrong targetid
            ctlg.get_alignmentset(language="hin", identifier="NA28-BSB-manual")
