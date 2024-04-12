"""Test code in src (init)."""

import pytest

import bible_alignments as src


class TestSourceidEnum:
    """Test SourceidEnum()."""

    def test_SourceidEnum(self) -> None:
        """Test initialization."""
        assert src.SourceidEnum("SBLGNT").value == "SBLGNT"
        # error on unrecognized sources
        with pytest.raises(ValueError):
            assert src.SourceidEnum("foo").value == "foo"

    def test_get_canon(self) -> None:
        """Test get_canon()."""
        assert src.SourceidEnum.get_canon("BGNT") == "nt"
        assert src.SourceidEnum.get_canon("NA28") == "nt"
        assert src.SourceidEnum.get_canon("SBLGNT") == "nt"
        assert src.SourceidEnum.get_canon("WLC") == "ot"
        assert src.SourceidEnum.get_canon("WLCM") == "ot"
        assert src.SourceidEnum.get_canon("foo") == "X"


# could also add tests of Configuration here, but those happen lower
# down
