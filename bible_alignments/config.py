"""Initialize common values.

This also defines a dataclass for managing the set of values
associated with a given version and source, e.g. ESV and WLC.

>>> from bible_alignments import config
>>> cfg = config.Configuration(sourceid="WLC", targetid="ESV", targetlanguage="eng", processid="manual")

# get the path to the alignments data (in your local repository)
>>> cfg.alignmentspath
PosixPath('/Users/sboisen/git/Clear-Bible/Alignments/data/alignments/eng/ESV/NA27-ESV-manual.json')

# get the path to the source data
>>> cfg.sourcepath
PosixPath('/Users/sboisen/git/Clear-Bible/Alignments/data/sources/NA27-ESV.tsv')

# get the path to the target data
>>> cfg.targetpath
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


# this has to be initialized with keyword arguments: not sure why
class Configuration(BaseModel):
    """Manage configuration data for a specific source and target.

    This encapsulates the set of naming conventions, and checks for
    the existence of expected files.

    """

    # an enumerated value from SourceidEnum like 'WLC'
    sourceid: SourceidEnum
    # like 'ESV'
    targetid: str
    # like 'eng': 2-4 characters, not a full name
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
        return f"{self.sourceid}-{self.targetid}-{self.processid}"

    @property
    def sourcepath(self) -> Path:
        """Return Path to source file."""
        return SOURCES / f"{self.sourceid}-{self.targetid}.tsv"

    @property
    def targetpath(self) -> Path:
        """Return Path to target file."""
        return TARGETS / f"{self.sourceid}-{self.targetid}.tsv"

    @property
    def alignmentsdirpath(self) -> Path:
        """Return Path to alignments directory."""
        return ALIGNMENTS / self.targetlanguage / self.targetid

    @property
    def alignmentspath(self) -> Path:
        """Return Path to alignments file."""
        return self.alignmentsdirpath / f"{self.sourceid}-{self.targetid}-{self.processid}.json"

    @property
    def configpath(self) -> Path:
        """Return Path to alignments file."""
        return self.alignmentsdirpath / f"{self.sourceid}-{self.targetid}-{self.processid}.toml"

    # optional/experimental
    @property
    def namespath(self) -> Path:
        """Return Path to names file."""
        return NAMES / f"{self.sourceid}-{self.targetid}.tsv"

    def display(self) -> None:
        """Display readable values."""
        print(repr(self))
        for attr in ["sourcepath", "targetpath", "configpath", "alignmentspath"]:
            print(f"{attr:<15} = {getattr(self, attr)}")
