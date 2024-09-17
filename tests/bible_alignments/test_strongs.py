"""Test code in src.util.strongs."""

import pytest

from bible_alignments import normalize_strongs


class TestNormalizeStrongs:
    """Test normalize_strongs()."""

    def test_prefix(self) -> None:
        """Test prefix."""
        # no default prefix any more
        assert normalize_strongs("0123", "G") == "G0123"
        # add non-default prefix
        assert normalize_strongs("0123", "H") == "H0123"

    def test_trailing_zero(self) -> None:
        """Test extra trailing zero.."""
        # only if also prefixed with 'G'
        assert normalize_strongs("G01230") == "G0123"

    def test_int(self) -> None:
        """Test int parameter."""
        # int parameter, with zero padding
        assert normalize_strongs(123, "G") == "G0123"
        # out of range: needs code!
        # with pytest.raises(ValueError):
        #     assert normalize_strongs("9999") == "G9999"

    def test_special(self) -> None:
        """Test special cases."""
        # special cases
        assert normalize_strongs("1537+4053") == "G4053b"

    def test_suffix(self) -> None:
        """Test prefix."""
        # with character suffix
        assert normalize_strongs("4053c", "G") == "G4053c"
        # with invalid character suffix
        with pytest.raises(AssertionError):
            assert normalize_strongs("4053z", "G") == "G4053z"

    def test_pipe(self) -> None:
        """Test cases with pipes."""
        # special cases
        assert normalize_strongs("1886j|2050b", "H") == "H2050b"
