"""Pytest tests for config."""

from pathlib import Path

from bible_alignments import config


class TestConfig:
    """Test config."""

    def test_values(self) -> None:
        """Test values."""
        # not much to test here
        assert Path(__file__).parent.parent == config.ROOT


class TestVersionSource:
    """Test VersionSource class."""

    def test_init(self) -> None:
        """Test initialization."""
        vs = config.VersionSource(version="ESV", sourceid="WLC", language="eng", processid="manual")
        assert vs.version == "ESV"
        assert vs.sourceid == config.SourceidEnum.WLC
        assert vs.language == "eng"
        assert vs.processid == "manual"
        assert vs.sourcepath == config.SOURCES / "WLC-ESV.tsv"
        assert vs.targetpath == config.TARGETS / "WLC-ESV.tsv"
        adirpath = config.ALIGNMENTS / vs.language / vs.version
        assert vs.alignmentsdirpath == adirpath
        assert vs.alignmentspath == adirpath / "WLC-ESV-manual.json"
        assert vs.configpath == adirpath / "WLC-ESV-manual.toml"
        assert vs.namespath == config.NAMES / "WLC-ESV.tsv"
