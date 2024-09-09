"""Manage data for alignment types.

These types may be extended.
"""

from dataclasses import dataclass
from typing import Union


@dataclass
class _AlignmentType:
    """Base class for managing types and roles for alignment records.

    Different types define different roles. While the set of types is
    intentionally left open to extension, data using these types have
    a defined set of roles.

    """

    type: str
    roles: tuple[str, ...] = tuple([])

    def __repr__(self) -> str:
        """Return a printed representation."""
        return f"<{self.__class__.__name__}: roles={self.roles}>"


@dataclass
class RelatedType(_AlignmentType):
    """The related type is a generic way to relate units."""

    type: str = "related"


@dataclass
class DirectedType(_AlignmentType):
    """Describes a directed but otherwise generic type."""

    type: str = "directed"
    roles: tuple[str, str] = tuple(
        ["from", "to"],
    )


@dataclass
class TranslationType(_AlignmentType):
    """Represents a source text and its translation as target."""

    type: str = "translation"
    roles: tuple[str, str] = tuple(
        ["source", "target"],
    )


@dataclass
class AnaphoraType(_AlignmentType):
    """Represents an anaphoric relation."""

    type: str = "anaphora"
    roles: tuple[str, str] = tuple(
        ["antecedent", "anaphor"],
    )


# Other use cases? quotation, citation, echo, allusion, text reuse, summarization, versioning

AlignmentTypes = Union[RelatedType, DirectedType, TranslationType, AnaphoraType]
