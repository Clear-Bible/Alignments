"""Base class for Source and Target."""

from dataclasses import dataclass

from biblelib.word import bcvwpid


@dataclass(order=True)
class BaseToken:
    """Common structure for Source and Target tokens."""

    # Identifies the word/morph in BBCCCVVVWWWP format
    # note, no word part: so this doesn't support sub-word tokens
    id: str
    # surface form: omit this for copyrighted sources
    text: str
    # ?
    altId: str = ""
    # fields for display: filled downstream
    aligned: bool = False
    # variant text if this text occurs multiple times in a verse
    text_unique: str = ""

    def __repr__(self) -> str:
        """Return a printed representation."""
        return f"<{self.__class__.__name__}: {self.id}>"

    #
    def __hash__(self) -> int:
        """Return a hash key."""
        return hash(self.id)

    @property
    def bcv(self) -> str:
        """Return the BCV-format verse reference for a token instance."""
        return str(bcvwpid.to_bcv(self.id))

    # variant so it can be passed as a Callable to methods
    def to_bcv(self) -> str:
        """Return the BCV-format verse reference for a token instance."""
        return str(self.bcv)

    @property
    def idtext(self) -> tuple[str, str]:
        """Return a tuple of id and text.

        This can help with diagnosing data issues.
        """
        return (
            self.id,
            self.text,
        )

    @property
    def pharaoh_index(self) -> int:
        """Return a zero-based word index.

        This supports generating data in 'pharaoh format'.

        """
        # parse the identifier to get the word index
        parsedid = bcvwpid.BCVWPID(self.id)
        return int(parsedid.word_ID) - 1
