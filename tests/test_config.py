"""Pytest tests for config."""

from pathlib import Path

from bible_alignments import config


class TestConfig:
    """Test config."""

    def test_values(self) -> None:
        """Test values."""
        # not much to test here
        assert Path(__file__).parent.parent == config.ROOT
