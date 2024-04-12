"""Test code in bible_alignments.burrito.Target

Does not test writing files.
"""

import pytest

from bible_alignments.burrito import DATAPATH, Target, TargetReader


@pytest.fixture
def mrk_4_9_6() -> Target:
    """Return a Target instance."""
    mrk_4_9_6_dict = {
        "id": "41004009006",
        "altId": "He-1",
        "text": "He",
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

    def test_pharaoh(self, mrk_4_9_6: Target) -> None:
        """Text pharaoh format conversion."""
        assert mrk_4_9_6.pharaoh_index == 5

    def test_asdict(self, mrk_4_9_6: Target) -> None:
        """Test asdict()."""
        assert mrk_4_9_6.asdict() == {
            "id": "41004009006",
            "altId": "He-1",
            "text": "He",
            "source_verse": "41004009",
            "transType": "m",
        }

    def test_asdict_omitfalse(self, mrk_4_9_6: Target) -> None:
        """Test asdict()."""
        assert mrk_4_9_6.asdict(omitfalse=False) == {
            "id": "41004009006",
            "altId": "He-1",
            "text": "He",
            "source_verse": "41004009",
            "skip_space_after": False,
            "exclude": False,
            "transType": "m",
            "isPunc": False,
            "isPrimary": False,
        }

    def test_asdict_omittext(self, mrk_4_9_6: Target) -> None:
        """Test asdict()."""
        assert mrk_4_9_6.asdict(omittext=True) == {
            "id": "41004009006",
            "altId": "--",
            "text": "--",
            "source_verse": "41004009",
            "transType": "m",
        }


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
        assert sparse_target.asdict() == {
            "id": "41004009006",
            "altId": "He-1",
            "text": "He",
            "source_verse": "41004009",
            "transType": "",
        }

    def test_asdict(self, sparse_target: Target) -> None:
        """Test asdict()."""
        assert sparse_target.asdict(omittext=True) == {
            "id": "41004009006",
            "altId": "--",
            "text": "--",
            "source_verse": "41004009",
            "transType": "",
        }


class TestTargetReader:
    """Test TargetReader()."""

    tr = TargetReader(DATAPATH / "targets/eng/nt_BSB.tsv")

    def test_init(self) -> None:
        """Test initialization."""
        # FRAGILE
        assert len(self.tr) == 201087
        assert self.tr["410040030021"].text == "Listen"

    def test_term_tokens(self) -> None:
        """Test term_tokens()."""
        assert [token.id for token in self.tr.term_tokens("Listen")] == [
            "400150100111",
            "400170050351",
            "400210330011",
            "410040030021",
            "410090070241",
            "420090350221",
            "420180060071",
            "460150510011",
            "590020050011",
        ]
        # Never occurs capitalized
        assert [token.id for token in self.tr.term_tokens("Crowd")] == []
        assert len([token.id for token in self.tr.term_tokens("crowd")]) == 115
        assert len([token.id for token in self.tr.term_tokens("crowd", lowercase=True)]) == 115
