"""Test code in bible_alignments.__init__"""

from bible_alignments import burrito


class TestInit:
    """Test imports and varialbes."""

    def test_init(self) -> None:
        """Test initialization."""
        assert burrito.DATAPATH.parent == burrito.ROOT
