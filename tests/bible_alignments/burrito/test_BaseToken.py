"""Test code in burrito.BaseToken

Sources and targets are tested more thoroughly in their respective
test files: this only tests common functionality.

"""

import pytest

from bible_alignments.burrito import BaseToken, asbool, bare_id


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
        assert repr(mrk_4_9_4) == "<BaseToken: 410040090051>"
        assert mrk_4_9_4.bcv == "41004009"
        assert mrk_4_9_4.idtext == ("410040090051", "ὦτα")
        # default values
        assert not mrk_4_9_4.aligned
        assert mrk_4_9_4.text_unique == ""

    def test_bare_id(self) -> None:
        """Test bare_id."""
        tok = BaseToken(id="n410040090051", text="ὦτα", altId="ὦτα-1")
        assert tok.bare_id == "410040090051"
        # also the non-class function
        assert bare_id("n410040090051") == "410040090051"
        assert bare_id("410040090051") == "410040090051"

    def test_isempty(self) -> None:
        """Test isempty()."""
        assert BaseToken(id="n410040090051", text="ὦτα").isempty is False
        assert BaseToken(id="n410040090051", text="").isempty is True


class TestAsbool:
    """Test asbool()."""

    def test_values(self) -> None:
        """Test values."""
        assert asbool(True) == "y"
        assert asbool(False) == "n"
