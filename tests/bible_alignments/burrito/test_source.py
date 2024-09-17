"""Test code in burrito.source

Does not test SourceReader or writing files.

There are different assumptions for GrapeCity formatted data, that
gets processed by Source.fromjsondict, as opposed to instantiating
Source objects directly. In particular, fromjsondict normalizes IDs
and some Unicode characters.

"""

import pytest

from bible_alignments import SOURCES
from bible_alignments.burrito import Source, SourceReader


@pytest.fixture
def mrk_4_9_4() -> Source:
    """Return a Source instance."""
    mrk_4_9_4_dict = {
        # GC data includes a word number
        "id": "410040090051",
        "altId": "ὦτα-1",
        "text": "ὦτα",
        "strong": "3775",
        "gloss": "ears",
        "gloss2": "ears",
        "lemma": "οὖς",
        "pos": "noun",
        "morph": "n- -apn-",
    }
    return Source.fromjsondict(mrk_4_9_4_dict)


@pytest.fixture
def gen_1_1_1() -> Source:
    """Return a Source instance."""
    gen_1_1_1_dict = {
        "id": "o010010010012",
        "altId": "רֵאשִׁ֖ית-1",
        "text": "רֵאשִׁית",
        "strong": "H7225",
        "gloss": "beginning",
        "lemma": "",
        "pos": "noun",
        "morph": "",
    }
    return Source.fromjsondict(gen_1_1_1_dict)


@pytest.fixture
def serialized() -> dict[str, str]:
    """Return a Source instance for data read from file."""
    return {
        # GC data includes a word number
        "id": "410040090051",
        "altId": "ὦτα-1",
        "text": "ὦτα",
        "strongs": "775",
        "gloss": "ears",
        "gloss2": "ears",
        "lemma": "οὖς",
        "pos": "noun",
        "morph": "n- -apn-",
    }


class TestSource:
    """Test Source()."""

    def test_init_gen(self, gen_1_1_1: Source) -> None:
        """Test initialization."""
        assert gen_1_1_1.id == "010010010012"
        # altId has vowel-pointing differences from text?
        # assert gen_1_1_1.altId[:-2] == gen_1_1_1.text
        assert gen_1_1_1.text == "רֵאשִׁית"

    def test_init(self, mrk_4_9_4: Source) -> None:
        """Test initialization."""
        assert mrk_4_9_4.id == "410040090051"
        assert mrk_4_9_4.altId[:-2] == mrk_4_9_4.text

    def test_idtext(self, mrk_4_9_4: Source) -> None:
        """Text idtext property."""
        assert mrk_4_9_4.idtext == (
            "410040090051",
            "ὦτα",
        )

    # this happens intentionally for Hebrew? So dropping this check
    # and its test for now
    # def test_empty_text(self) -> None:
    #     """Test failing on empty text."""
    #     notext: dict[str, str] = {
    #         "id": "41004009005",
    #         "altId": "ὦτα-1",
    #         "text": "",
    #         "strong": "3775",
    #         "gloss": "ears",
    #         "gloss2": "ears",
    #         "lemma": "οὖς",
    #         "pos": "noun",
    #         "morph": "n- -apn-",
    #     }
    #     with pytest.raises(ValueError):
    #         Source(**notext)

    def test_badid(self) -> None:
        """Test failing on ID with too many characters."""
        bad: dict[str, str] = {
            "id": "4100400900005",
            "altId": "ὦτα-1",
            "text": "ὦτα",
            "strong": "3775",
            "gloss": "ears",
            "gloss2": "ears",
            "lemma": "οὖς",
            "pos": "noun",
            "morph": "n- -apn-",
        }
        with pytest.raises(AssertionError):
            Source(**bad)

    def test_gcid(self) -> None:
        """Test fromjsondict on GC ID without leading zero."""
        gcdict: dict[str, str] = {
            # missing leading zero
            "id": "10010010011",
            # ignore this obviously non-Hebrew data
            "altId": "ὦτα-1",
            "text": "ὦτα",
            "strong": "3775",
            "gloss": "ears",
            "gloss2": "ears",
            "lemma": "οὖς",
            "pos": "noun",
            "morph": "n- -apn-",
        }
        gen_1_1 = Source.fromjsondict(gcdict)
        assert gen_1_1.id == "010010010011"

    def test_asdict(self, mrk_4_9_4: Source) -> None:
        """Test asdict()."""
        assert mrk_4_9_4.asdict() == {
            "id": "n41004009005",
            "altId": "ὦτα-1",
            "text": "ὦτα",
            "strongs": "G3775",
            "gloss": "ears",
            "gloss2": "ears",
            "lemma": "οὖς",
            "pos": "noun",
            "morph": "n- -apn-",
        }

    def test_asdict_omittext(self, mrk_4_9_4: Source) -> None:
        """Test asdict()."""
        assert mrk_4_9_4.asdict(omittext=True) == {
            "id": "n41004009005",
            "altId": "--",
            "text": "--",
            "strongs": "G3775",
            "gloss": "ears",
            "gloss2": "ears",
            "lemma": "οὖς",
            "pos": "noun",
            "morph": "n- -apn-",
        }

    def test_asdict_essential(self, mrk_4_9_4: Source) -> None:
        """Test asdict()."""
        assert mrk_4_9_4.asdict(essential=True) == {
            "id": "n41004009005",
            "altId": "ὦτα-1",
            "text": "ὦτα",
            "strongs": "G3775",
            "gloss": "ears",
            "gloss2": "ears",
            "lemma": "οὖς",
            "pos": "noun",
            "morph": "n- -apn-",
            "exclude": False,
        }

    def test_asdict_omittext_essential(self, mrk_4_9_4: Source) -> None:
        """Test asdict()."""
        assert mrk_4_9_4.asdict(omittext=True, essential=True) == {
            "id": "n41004009005",
            "altId": "--",
            "text": "--",
            "strongs": "G3775",
            "gloss": "ears",
            "gloss2": "ears",
            "lemma": "οὖς",
            "pos": "noun",
            "morph": "n- -apn-",
            "exclude": False,
        }

    def test_deserialized(self, serialized: dict[str, str]) -> None:
        """Test asdict()."""
        deserialized: dict[str, str] = {SourceReader.inmap[k]: v for k, v in serialized.items()}
        assert Source(**deserialized).asdict() == {
            "id": "n41004009005",
            "altId": "ὦτα-1",
            "text": "ὦτα",
            # tests prefix and zero padding
            "strongs": "G0775",
            "gloss": "ears",
            "gloss2": "ears",
            "lemma": "οὖς",
            "pos": "noun",
            "morph": "n- -apn-",
        }


class TestSourceReader:
    """Test SourceReader()."""

    sr = SourceReader(SOURCES / "SBLGNT.tsv")

    def test_init(self) -> None:
        """Test initialization."""
        # FRAGILE
        assert len(self.sr) > 137700
        # no lemmas yet for SBLGNT
        # assert sr["n41004003001"].lemma == "ἀκούω"
        assert self.sr["n41004003001"].strong == "G0191"

    def test_vocabulary(self) -> None:
        """Test vocabulary()."""
        assert len(self.sr.vocabulary()) == 19355
        assert len(self.sr.vocabulary(lower=True)) == 18619
        assert len(self.sr.vocabulary(tokenattr="lemma")) == 5468

    def test_term_tokens(self) -> None:
        """Test term_tokens()."""
        # token.id here excludes corpus_prefix, but includes part_ID
        assert [token.id for token in self.sr.term_tokens("βλαστᾷ")] == ["410040270111"]
        assert [token.id for token in self.sr.term_tokens("βλαστάνω", tokenattr="lemma")] == [
            "400130260031",
            "410040270111",
            "580090040241",
            "590050180121",
        ]
        # lemma doesn't match surface text
        assert [token.id for token in self.sr.term_tokens("βλαστάνω")] == []
        assert [token.id for token in self.sr.term_tokens("Οἶδας")] == ["400150120071", "550010150011"]
        assert len([token.id for token in self.sr.term_tokens("οἶδας")]) == 15
        # more if disregarding case
        assert len([token.id for token in self.sr.term_tokens("Οἶδας", lowercase=True)]) == 17


class TestOTSourceReader:
    """Test SourceReader()."""

    sr = SourceReader(SOURCES / "WLC.tsv")

    def test_init(self) -> None:
        """Test initialization."""
        # FRAGILE: round number for slightly more generality
        assert len(self.sr) >= 475000
        # this fails: Unicode normalization??
        assert self.sr["o010010010021"].text == "בָּרָ֣א"

    def test_vocabulary(self) -> None:
        """Test vocabulary()."""
        assert len(self.sr.vocabulary()) == 83669
        assert len(self.sr.vocabulary(tokenattr="lemma")) == 9044

    # def test_term_tokens(self) -> None:
    #     """Test term_tokens()."""
    #     assert [token.id for token in self.sr.term_tokens("βλαστᾷ")] == ["n41004027011"]
    #     assert [token.id for token in self.sr.term_tokens("βλαστάνω", tokenattr="lemma")] == [
    #         "n40013026003",
    #         "n41004027011",
    #         "n58009004024",
    #         "n59005018012",
    #     ]
    #     # lemma doesn't match surface text
    #     assert [token.id for token in self.sr.term_tokens("βλαστάνω")] == []
    #     assert [token.id for token in self.sr.term_tokens("Οἶδας")] == ["n40015012007", "n55001015001"]
    #     assert len([token.id for token in self.sr.term_tokens("οἶδας")]) == 15
    #     # more if disregarding case
    #     assert len([token.id for token in self.sr.term_tokens("Οἶδας", lowercase=True)]) == 17
