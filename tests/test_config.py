"""Pytest tests for config."""

from pathlib import Path

from bible_alignments import config


class TestConfig:
    """Test config."""

    def test_values(self) -> None:
        """Test values."""
        # not much to test here
        assert Path(__file__).parent.parent == config.ROOT


class TestConfiguration:
    """Test Configuration class."""

    def test_init(self) -> None:
        """Test initialization."""
        vs = config.Configuration(sourceid="WLC", targetid="ESV", targetlanguage="eng", processid="manual")
        assert vs.targetid == "ESV"
        assert vs.sourceid == config.SourceidEnum.WLC
        assert vs.targetlanguage == "eng"
        assert vs.processid == "manual"
        assert vs.sourcepath == config.SOURCES / "WLC-ESV.tsv"
        assert vs.targetpath == config.TARGETS / "WLC-ESV.tsv"
        adirpath = config.ALIGNMENTS / vs.targetlanguage / vs.targetid
        assert vs.alignmentsdirpath == adirpath
        assert vs.alignmentspath == adirpath / "WLC-ESV-manual.json"
        assert vs.configpath == adirpath / "WLC-ESV-manual.toml"
        assert vs.namespath == config.NAMES / "WLC-ESV.tsv"
