"""Internal-only code for working with alignment data."""

from enum import Enum
from pathlib import Path

from pydantic import BaseModel, constr

from .strongs import normalize_strongs


ROOT = Path(__file__).parent.parent
DATAPATH = ROOT / "data"
SRCPATH = ROOT / "src"

ALIGNMENTS = DATAPATH / "alignments"
SOURCES = DATAPATH / "sources"
TARGETS = DATAPATH / "targets"
NAMES = DATAPATH / "names"

# for output
ALIGNMENTSROOT = ROOT.parent / "Alignments"
REFERENCESPATH = ALIGNMENTSROOT / "data/sources/references"

CANONIDS = {
    "nt",
    "ot",
    # meaning the entire 66 book corpus
    "protestant",
}


class SourceidEnum(str, Enum):
    """Valid source identifiers."""

    BGNT = "BGNT"
    NA27 = "NA27"
    NA28 = "NA28"
    SBLGNT = "SBLGNT"
    WLC = "WLC"
    WLCM = "WLCM"

    @property
    def canon(self) -> str:
        """Return 'ot' or 'nt' for the canon."""
        if self.value in ["WLC", "WLCM"]:
            return "ot"
        elif self.value in ["BGNT", "NA27", "NA28", "SBLGNT"]:
            return "nt"
        else:
            raise ValueError(f"Unknown error in SourceidEnum.canon for {self.value}")

    # need to add DC, probably others down the road
    @staticmethod
    def get_canon(sourceid: str) -> str:
        """Return a canon string for recognized sources, else 'X'."""
        try:
            srcenum = SourceidEnum(sourceid)
            return srcenum.canon
        except ValueError:
            # unrecognized source
            return "X"


__all__ = [
    "ROOT",
    "DATAPATH",
    "SRCPATH",
    "ALIGNMENTS",
    "SOURCES",
    "TARGETS",
    "NAMES",
    "SourceidEnum",
    # strongs
    "normalize_strongs",
]


# this has to be initialized with keyword arguments: because Pydantic?
class Configuration(BaseModel):
    """Manage configuration data for a specific source and target.

    This encapsulates the set of naming conventions, and checks for
    the existence of expected files.

    When loaded through a pip-installed library, only a small amount
    of LEB alignment data is provided. To use a local data for a
    configurationg, set the root property to the path to the root of
    the local Alignments repository.

    """

    # the root directory for input and output
    # default is okay within this module, but has to be specified for
    # clients using this as a library
    root: Path = Path(__file__).parent.parent
    # an enumerated value from SourceidEnum like 'WLC'
    sourceid: SourceidEnum
    # like 'ESV'
    targetid: str
    # like 'eng': 2-4 characters, not a full name
    # TODO: use Annotated instead,
    # https://docs.pydantic.dev/latest/api/types/#pydantic.types.constr--__tabbed_1_2
    targetlanguage: constr(min_length=2, max_length=4)
    # like 'manual': an open-ended slug
    processid: str

    # def __post_init__(self) -> None:
    #     """Compute values after initialization."""
    #     # could add language validation against Language.LanguageManager()
    #     pass

    @property
    def identifier(self) -> str:
        """Return a string identifying the configuration."""
        # in some (legacy?) contexts sourceid is an Enum? not sure what's up here, workaround
        sourceid: str = self.sourceid.value if isinstance(self.sourceid, Enum) else self.sourceid
        return f"{sourceid}-{self.targetid}-{self.processid}"

    @property
    def sourcepath(self) -> Path:
        """Return Path to source file."""
        return self.root / "data/sources" / f"{self.sourceid.value}-{self.targetid}.tsv"

    @property
    def targetpath(self) -> Path:
        """Return Path to target file."""
        return self.root / "data/targets" / f"{self.sourceid.value}-{self.targetid}.tsv"

    @property
    def alignmentsdirpath(self) -> Path:
        """Return Path to alignments directory."""
        return Path(self.root / "data/alignments" / self.targetlanguage / self.targetid)

    @property
    def alignmentspath(self) -> Path:
        """Return Path to alignments output file."""
        # return self.alignmentsdirpath / f"{self.sourceid.value}-{self.targetid}-{self.processid}.json"
        return self.alignmentsdirpath / f"{self.identifier}.json"

    @property
    def alignmentswordspath(self) -> Path:
        """Return Path to alignments file that includes words."""
        return self.alignmentsdirpath / f"{self.identifier}+words.json"

    @property
    def configpath(self) -> Path:
        """Return Path to alignments configuration file."""
        return self.alignmentsdirpath / f"{self.identifier}.toml"

    # optional/experimental
    @property
    def namespath(self) -> Path:
        """Return Path to names file."""
        return self.root / "data/names" / f"{self.sourceid.value}-{self.targetid}.tsv"

    # to add
    # - plain pharaoh
    # - JSONified pharaoh

    def display(self) -> None:
        """Display readable values."""
        print(repr(self))
        for attr in ["sourcepath", "targetpath", "configpath", "alignmentspath"]:
            print(f"{attr:<15} = {getattr(self, attr)}")

    def reroot(self, root: Path) -> None:
        """Reset the root and derivative attributes.

        Installing this via pip sets root to an unhelpful value.

        """
