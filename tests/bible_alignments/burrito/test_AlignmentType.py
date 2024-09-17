"""Test code in burrito.AlignmentType."""

# import pytest

from bible_alignments.burrito import AlignmentType


class TestTranslationType:
    """Test TranslationType()."""

    def test_init(self) -> None:
        """Test initialization."""
        transtype = AlignmentType.TranslationType()
        assert transtype.type == "translation"
        assert "source" in transtype.roles
        assert "target" in transtype.roles


# could add tests for other types
# not sure how to test the typing, but non-essential
