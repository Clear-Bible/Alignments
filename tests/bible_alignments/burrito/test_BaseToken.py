"""Test code in src.burrito.BaseToken

Sources and targets are tested more thoroughly in their respective
test files: this only tests common functionality.

"""

import pytest

from bible_alignments.burrito import BaseToken, asbool


@pytest.fixture
def mrk_4_9_4() -> BaseToken:
    """Return a BaseToken instance."""
    return BaseToken(id="410040090051", text="ὦτα", altId="ὦτα-1")


class TestBaseToken:
    """Test BaseToken()."""

    def test_init(self, mrk_4_9_4: BaseToken) -> None:
        """Test initialization."""
        assert mrk_4_9_4.id == "410040090051"
        assert mrk_4_9_4.text == "ὦτα"
        assert mrk_4_9_4.altId[:-2] == mrk_4_9_4.text
        # default values
        assert not mrk_4_9_4.aligned
        assert mrk_4_9_4.text_unique == ""


class TestAsbool:
    """Test asbool()."""

    def test_values(self) -> None:
        """Test values."""
        assert asbool(True) == "y"
        assert asbool(False) == "n"
