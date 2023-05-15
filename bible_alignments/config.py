"""Initialize common values.

This also defines a dataclass for managing the set of values
associated with a given version and source, e.g. ESV and WLC.

>>> from bible_alignments import config
>>> vs = config.VersionSource(version="ESV", sourceid="WLC", language="eng", processid="manual")

# get the path to the alignments data (in your local repository)
>>> vs.alignmentspath
PosixPath('/Users/sboisen/git/Clear-Bible/Alignments/data/alignments/eng/ESV/NA27-ESV-manual.json')

# get the path to the source data
>>> vs.sourcepath
PosixPath('/Users/sboisen/git/Clear-Bible/Alignments/data/sources/NA27-ESV.tsv')

# get the path to the target data
>>> vs.targetpath
PosixPath('/Users/sboisen/git/Clear-Bible/Alignments/data/targets/NA27-ESV.tsv')


"""

from enum import Enum
from pathlib import Path

from pydantic import BaseModel, constr


ROOT = Path(__file__).parent.parent
DATAPATH = ROOT / "data"

ALIGNMENTS = DATAPATH / "alignments"
SOURCES = DATAPATH / "sources"
TARGETS = DATAPATH / "targets"
NAMES = DATAPATH / "names"


class SourceidEnum(str, Enum):
    """Valid source identifiers."""

    NA27 = "NA27"
    SBLGNT = "SBLGNT"
    WLC = "WLC"


class VersionSource(BaseModel):
    """Manage configuration data for a specific version and source.

    This encapsulates the set of naming conventions, and checks for
    the existence of expected files.

    """

    # like 'ESV'
    version: str
    # an enumerated value from SourceidEnum like 'WLC'
    sourceid: SourceidEnum
    # like 'eng': 2-4 characters, not a full name
    language: constr(min_length=2, max_length=4)
    # like 'manual': an open-ended slug
    processid: str

    # def __post_init__(self) -> None:
    #     """Compute values after initialization."""
    #     # could add language validation against Language.LanguageManager()
    #     pass

    @property
    def sourcepath(self) -> Path:
        """Return Path to source file."""
        return SOURCES / f"{self.sourceid}-{self.version}.tsv"

    @property
    def targetpath(self) -> Path:
        """Return Path to target file."""
        return TARGETS / f"{self.sourceid}-{self.version}.tsv"

    @property
    def alignmentsdirpath(self) -> Path:
        """Return Path to alignments directory."""
        return ALIGNMENTS / self.language / self.version

    @property
    def alignmentspath(self) -> Path:
        """Return Path to alignments file."""
        return self.alignmentsdirpath / f"{self.sourceid}-{self.version}-{self.processid}.json"

    @property
    def configpath(self) -> Path:
        """Return Path to alignments file."""
        return self.alignmentsdirpath / f"{self.sourceid}-{self.version}-{self.processid}.toml"

    # optional/experimental
    @property
    def namespath(self) -> Path:
        """Return Path to names file."""
        return NAMES / f"{self.sourceid}-{self.version}.tsv"
