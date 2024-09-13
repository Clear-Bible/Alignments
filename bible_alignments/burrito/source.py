"""Manage the sources for alignment data.

This supports reading and writing source records. It is normally
called from burrito.manager.Manager().

>>> from bible_alignments import SOURCES
>>> from bible_alignments.burrito import SourceReader
>>> src = SourceReader(SOURCES / "SBLGNT.tsv")
# number of tokens
>>> len(src)
137741
# token vocabulary
>>> len(src.vocabulary())
19355
# lemma vocabulary
>>> len(src.vocabulary(tokenattr="lemma"))
5468
# dict: token ID -> Source() instance
>>> src["n41004003001"]
src["n41004003001"]
<Source: n41004003001>
>>> src["n41004003001"].display()
n41004003001: Ἀκούετε		 (Listen, ἀκούω, verb)
>>> src["n41004003001"].idtext
('n41004003001', 'Ἀκούετε')
>>> src["n41004003001"].asdict()
{'identifier': 'n41004003001',
 'altId': 'Ἀκούετε-1',
 'text': 'Ἀκούετε',
 'strongs': 'G0191',
 'gloss': 'Listen',
 'gloss2': 'listen',
 'lemma': 'ἀκούω',
 'pos': 'verb',
 'morph': 'V-PAM-2P'}

"""

from collections import UserDict
from dataclasses import dataclass
from pathlib import Path
import re
from typing import Any, Iterable
import unicodedata
from warnings import warn

from unicodecsv import DictReader, DictWriter

from biblelib.word import bcvwpid

# should eventually come from Clearlib
from bible_alignments import normalize_strongs
from .BaseToken import BaseToken


# these attribute names match the source data for simplicity
# TODO: make attributes optional
@dataclass(order=True, repr=False)
class Source(BaseToken):
    """Manage data for a source/manuscript token.

    This is designed around the GrapeCity content. It supports output
    in several formats.

    """

    # Strongs number
    # Serialized as strongs
    strong: str = ""
    # English gloss
    gloss: str = ""
    # sometimes a Chinese/alternate language gloss?
    gloss2: str = ""
    # source language lemma
    lemma: str = ""
    # part of speech
    pos: str = ""
    # coded morphological information: need to document the format
    morph: str = ""
    _output_fields: tuple = (
        ("id", "id"),
        ("altId", "altId"),
        ("text", "text"),
        ("strong", "strongs"),
        ("gloss", "gloss"),
        ("gloss2", "gloss2"),
        ("lemma", "lemma"),
        ("pos", "pos"),
        ("morph", "morph"),
    )
    _input_fields: tuple = tuple(dict(_output_fields).keys())
    # # TODO: enumerate and validate part of speech values
    # # TODO: standardize morph representation
    # dataclass rules means __hash__ isn't inherited otherwise
    __hash__ = BaseToken.__hash__

    def __post_init__(self) -> None:
        """Compute values after initialization."""

        def normalize(string: str) -> str:
            """Return a NFKC normalization of string."""
            return unicodedata.normalize("NFKC", string)

        # use BibleLib to standardize the identifier: no
        # corpus_prefix. but includes partID
        stdid = bcvwpid.BCVWPID(self.id)
        self.id = stdid.get_id()

        # this belongs in BibleLib
        is_nt = 66 >= int(stdid.to_bid) >= 40
        # ensure Greek is normalized for NT books
        if is_nt:
            self.altId = normalize(self.altId)
            self.text = normalize(self.text)
            self.lemma = normalize(self.lemma)
        # normalize Strongs: skip 'H' in Macula Hebrew data
        if self.strong and self.strong != "H":
            if re.match(r"[AGH]", self.strong):
                prefix = self.strong[0]
            else:
                if is_nt:
                    prefix = "G"
                else:
                    # but what about Aramaic? Assign for selected BCV?
                    prefix = "G"
                self.strong = prefix + self.strong
            try:
                self.strong = normalize_strongs(self.strong, prefix=prefix)
            except ValueError:
                warn(f"Failed to normalize Strong's '{self.strong}' in {self.id}")
        # ensure valid values: wrong for Hebrew
        # if not self.text:
        #     raise ValueError(f"Empty text for {self.id}")
        # too strict: need to allow accents
        # if not str.isalpha(self.text):
        #     raise ValueError(f"Non-alphabetic text {repr(self.text)} for {self.id}")

    def is_content(self) -> bool:
        """Return True if part of speech indicates content.

        This means 'noun', 'verb', 'adj', 'adv'.
        """
        return self.pos in {"noun", "verb", "adj", "adv"}

    def _is_pos(self, pos: str) -> bool:
        """Return True if part of speech matches pos."""
        return self.pos == pos

    def is_noun(self) -> bool:
        """Return true if this term is a noun."""
        return self._is_pos("noun")

    @staticmethod
    def fromjsondict(jdict: dict[str, Any]) -> "Source":
        """Return a Source instance for a dictionary read from JSON.

        This also does any normalization of the text: minimally,
        remove an LR markers.

        This is only used for upgrading GrapeCity data to Burrito
        format.

        """
        newdict = jdict.copy()
        # convert id attr to a str
        newdict["id"] = str(newdict["id"])
        # Some GC data is missing the leading zero for book numbers
        if len(newdict["id"]) == 11:
            # add missing leading zero: fragile hack!
            newdict["id"] = newdict["id"].zfill(12)
        # filter our LRR markers
        newdict["altId"] = newdict["altId"].replace(chr(8206), "")
        newdict["text"] = newdict["text"].replace(chr(8206), "")
        return Source(**newdict)

    @property
    def _display(self) -> str:
        """Return a displayable string for key data."""
        return f"{self.id}: {self.text}\t\t ({self.gloss}, {self.lemma}, {self.pos})"

    def display(self) -> None:
        """Print a readable display of the key data."""
        print(self._display)

    def asdict(self, omittext: bool = False, essential: bool = False) -> dict[str, str]:
        """Marshall data to a dict for output.

        This adds a canon_prefix, and omits the part_index for NT
        tokens.

        With omittext = True (default is False), replace text with a
        placeholder: use this for copyrighted texts that cannot be
        redisstributed.

        With essential = True (default is False), add an 'exclude' key
        which is True if not is_content().

        """
        fdict = dict(self._output_fields)
        outdict: dict[str, str] = {fdict[k]: getattr(self, k) for k in fdict}
        normid = bcvwpid.BCVWPID(outdict["id"])
        part_index: bool = not normid.canon_prefix == "n"
        outdict["id"] = normid.get_id(prefix=True, part_index=part_index)
        if omittext:
            outdict["altId"] = "--"
            outdict["text"] = "--"
        if essential:
            outdict["exclude"] = not self.is_content()
        return outdict


class SourceReader(UserDict):
    """Read Source TSV data into a dict, with identifiers as keys.

    Record data is normalized in some ways as it is read:
    - Convert old-style token identifiers
    - Normalize Unicode text to NKFC
    - Normalize Strong's numbers

    Verse-level indices in altId are also revised: some data had errors.
    """

    inmap = {v: k for k, v in Source._output_fields}

    def __init__(self, tsvpath: Path, idheader: str = "id") -> None:
        """Initialize a Reader instance."""
        super().__init__()
        self.tsvpath = tsvpath
        with self.tsvpath.open("rb") as f:
            reader = DictReader(f, delimiter="\t")
            for row in reader:
                assert idheader in row, f"Missing ID header '{idheader}'"
                if idheader != "id":
                    # standardize row data to use "id" as key
                    idrow = {("id" if k == idheader else k): v for k, v in row.items()}
                else:
                    idrow = row
                identifier = idrow["id"]
                deserialized = {self.inmap[k]: v for k, v in idrow.items() if k in self.inmap}
                if identifier in self:
                    warn(f"{identifier} is duplicated in {self.tsvpath}")
                self.data[identifier] = Source(**deserialized)

    def vocabulary(self, tokenattr: str = "text", lower: bool = False) -> list[str]:
        """Return the sorted set of attribute values for tokens.

        The attribute used is 'text' by default: 'lemma' is another useful value.

        With lower = True (default is False), lower-case values.
        """
        if lower:
            vocab = {getattr(stok, tokenattr).lower() for stok in self.values()}
        else:
            vocab = {getattr(stok, tokenattr) for stok in self.values()}
        return sorted(vocab)

    # This assumes the standard set of output fields. That might
    # include fields with no content.
    def write_tsv(self, outpath: Path, essential: bool = False) -> None:
        """Write Sources as TSV."""
        fields = list(dict(Source._output_fields).values())
        if essential:
            fields += ["exclude"]
        with outpath.open("wb") as f:
            writer = DictWriter(f, fieldnames=fields, delimiter="\t")
            writer.writeheader()
            for sourceinst in self.values():
                srcdict: dict = sourceinst.asdict(essential=essential)
                # normalize to not include canon prefix or part ID
                srcdict["id"] = bcvwpid.BCVWPID(srcdict["id"]).get_id(prefix=True, part_index=False)
                writer.writerow(srcdict)

    def term_tokens(self, term: str, tokenattr: str = "text", lowercase: bool = False) -> list[Source]:
        """Return a list of tokens containing term.

        The attribute used is 'text' by default: 'lemma' is another useful value.

        With lowercase = True (default is False), lower-case term and token values.
        """
        casedterm = term.lower() if lowercase else term
        return [
            token
            for token in self.values()
            if (tokattr := getattr(token, tokenattr))
            if (casedtokenattr := tokattr.lower() if lowercase else tokattr)
            if casedtokenattr == casedterm
        ]

    def _count_by_type(self, items: Iterable) -> int:
        """Return a count of unique items."""
        return len({items})

    def counts(self) -> None:
        """Print various counts for the tokens in self."""
        for toktype in ["text", "lemma"]:
            toktypestr = f"{toktype.capitalize()}"
            instances = [getattr(tok, toktype) for tok in self.values()]
            counts = {"instance": len(instances), "type": len(set(instances))}
            for counttype in ["instance", "type"]:
                counttypestr = f"{toktypestr}.{counttype.capitalize()}"
                print(f"{counttypestr}\t{counts[counttype]}")
                contentinstances = [getattr(tok, toktype) for tok in self.values() if tok.is_content()]
                contentcounts = {"instance": len(contentinstances), "type": len(set(contentinstances))}
                print(f"{counttypestr}.IsContent\t{contentcounts[counttype]}")
                for pos in ["adj", "adv", "noun", "verb"]:
                    posstr = f"{counttypestr}.{pos.capitalize()}"
                    posinstances = [getattr(tok, toktype) for tok in self.values() if tok._is_pos(pos)]
                    poscounts = {"instance": len(posinstances), "type": len(set(posinstances))}
                    print(f"{posstr}\t{poscounts[counttype]}")
