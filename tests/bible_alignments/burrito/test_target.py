"""Test code in burrito.Target

Does not test writing files.
"""

import pytest

from bible_alignments.burrito import DATAPATH, Target, TargetReader

# test published version
ENGLANGDATAPATH = DATAPATH / "eng"


@pytest.fixture
def mrk_4_9_6() -> Target:
    """Return a Target instance."""
    mrk_4_9_6_dict = {
        "id": "41004009006",
        "source_verse": "41004009",
        "skip_space_after": False,
        "altId": "He-1",
        "text": "He",
        "exclude": True,
        "transType": "m",
        "isPunc": False,
        "isPrimary": False,
    }
    return Target.fromjsondict(mrk_4_9_6_dict)


@pytest.fixture
def sparse_target() -> Target:
    """Return a Target instance with defaulted data."""
    mrk_4_9_6_dict = {
        "id": "41004009006",
        "altId": "He-1",
        "text": "He",
    }
    return Target.fromjsondict(mrk_4_9_6_dict)


class TestTarget:
    """Test Target()."""

    def test_init(self, mrk_4_9_6: Target) -> None:
        """Test initialization."""
        assert mrk_4_9_6.id == "41004009006"
        assert mrk_4_9_6.altId[:-2] == mrk_4_9_6.text

    def test_idtext(self, mrk_4_9_6: Target) -> None:
        """Text idtext property."""
        assert mrk_4_9_6.idtext == (
            "41004009006",
            "He",
        )

    def test_asdict(self, mrk_4_9_6: Target) -> None:
        """Test asdict()."""
        assert mrk_4_9_6.asdict(omitfalse=True, omittext=True) == {
            "id": "41004009006",
            "text": "--",
            "exclude": "y",
            "skip_space_after": "",
            "source_verse": "41004009",
        }
        assert mrk_4_9_6.asdict(omitfalse=True, omittext=False) == {
            "id": "41004009006",
            "text": "He",
            "exclude": "y",
            "skip_space_after": "",
            "source_verse": "41004009",
        }
        assert mrk_4_9_6.asdict(omitfalse=False, omittext=True) == {
            "id": "41004009006",
            "text": "--",
            "exclude": "y",
            "skip_space_after": "n",
            "source_verse": "41004009",
        }
        assert mrk_4_9_6.asdict(omitfalse=False, omittext=False) == {
            "id": "41004009006",
            "text": "He",
            "exclude": "y",
            "skip_space_after": "n",
            "source_verse": "41004009",
        }
        # TODO: test with variant fields


class TestSparseTarget:
    """Test Target() with sparse data."""

    def test_init(self, sparse_target: Target) -> None:
        """Test initialization."""
        assert sparse_target.id == "41004009006"
        assert sparse_target.altId[:-2] == sparse_target.text
        # defaults
        assert sparse_target.transType == ""
        assert not sparse_target.isPunc
        assert not sparse_target.isPrimary

    def test_asdict(self, sparse_target: Target) -> None:
        """Test asdict()."""
        assert sparse_target.asdict(omittext=True) == {
            "id": "41004009006",
            "text": "--",
            "exclude": "",
            "skip_space_after": "",
            "source_verse": "41004009",
        }


class TestTargetReader:
    """Test TargetReader()."""

    tr = TargetReader(ENGLANGDATAPATH / "targets/BSB/nt_BSB.tsv")

    def test_init(self) -> None:
        """Test initialization."""
        # FRAGILE: exact number changes
        assert len(self.tr) > 201000
        assert self.tr["41004003002"].text == "Listen"

    def test_term_tokens(self) -> None:
        """Test term_tokens()."""
        listentokens = [token.id for token in self.tr.term_tokens("Listen")]
        for ltoken in [
            "40015010011",
            "40017005035",
            "40021033001",
            "41004003002",
            "41009007024",
            "42009035022",
            "42018006007",
            "46015051001",
            "59002005001",
        ]:
            assert ltoken in listentokens
        # Never occurs capitalized
        assert [token.id for token in self.tr.term_tokens("Crowd")] == []
        assert len([token.id for token in self.tr.term_tokens("crowd")]) == 115
        assert len([token.id for token in self.tr.term_tokens("crowd", lowercase=True)]) == 115
