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
    def bare_id(self) -> str:
        """Return the ID minus any canon prefixes."""
        return self.id[1:] if self.id[0].isalpha() else self.id

    @property
    def isempty(self) -> bool:
        """True if token.text is the empty string: that's not normal."""
        return self.text == ""


def asbool(value: bool | str) -> str:
    """Return a minimal string value for output from a boolean value."""
    return "y" if bool(value) else "n"


def bare_id(identifier) -> str:
    """Strip any canon prefixes."""
    assert bcvwpid.is_bcvwpid(identifier), f"'{identifier}' does not look like a valid BCVWPID identifier."
    return identifier[1:] if identifier[0].isalpha() else identifier
