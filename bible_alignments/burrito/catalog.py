"""Read an internal catalog of available alignments.

Alignment data files are named by combining the source edition ID, the
target edition ID, and an (optional) additional identifier. For
GrapeCity alignments, the additional identifier is "manual". This code
assumes there is also a TOML file adjacent to the alignments that
provides additional metadata.

>>> from bible_alignments.burrito import Catalog
>>> ctlg = catalog.Catalog()
>>> ctlg.languages
['eng', 'hin', 'man', 'mya']
>>> ctlg.get_alignmentset_ids("man")
['SBLGNT-SGS-manual', 'SBLGNT-CUVMP-manual', 'SBLGNT-XYB-manual']
>>> ctlg["man"]["SBLGNT-SGS-manual"]
<AlignmentSet: man, SBLGNT-SGS-manual>

# AlignmentSet manages paths for a group of alignment files
>>> alset = Catalog().get_alignmentset(language="eng", identifier="SBLGNT-BSB-manual")

>>> na27sgs = ctlg["man"]["SBLGNT-SGS-manual"]
>>> na27sgs.sourcepath
PosixPath('/Users/sboisen/git/Clear-Bible/internal-Alignments/data/sources/SBLGNT.tsv')
>>> na27sgs.targetpath
PosixPath('/Users/sboisen/git/Clear-Bible/internal-Alignments/data/targets/nt_SGS.tsv')
>>> na27sgs.alignmentpath
PosixPath('/Users/sboisen/git/Clear-Bible/internal-Alignments/data/alignments/man/SGS/SBLGNT-SGS-manual.json')
>>> na27sgs.tomlpath
PosixPath('/Users/sboisen/git/Clear-Bible/internal-Alignments/data/alignments/man/SGS/SBLGNT-SGS-manual.toml')


TODO:
- add check for missing source/target files

"""

from collections import defaultdict, UserDict
from dataclasses import dataclass
from pathlib import Path
import re


# from bible_alignments.burrito import DATAPATH as DPATH
# repeated here from __init__ to avoid circular imports
DATAPATH = Path(__file__).parent.parent.parent / "data"


@dataclass
class AlignmentSet:
    """Manage a set of files for an alignment."""

    # this should become an enumerated set
    sourceid: str
    targetid: str
    targetlanguage: str
    datapath: Path = DATAPATH
    alternateid: str = ""

    def __post_init__(self) -> None:
        """Post-initialization checks."""
        for idattr in ["sourceid", "targetid"]:
            idstr = getattr(self, idattr)
            # only allow ASCII letters, digits, and underscores
            if not re.fullmatch(r"\w+", idstr, flags=re.ASCII):
                raise ValueError(f"Invalid {idattr}: {idstr}")
        if self.alternateid and not re.fullmatch(r"\w+", self.alternateid, flags=re.ASCII):
            raise ValueError(f"Invalid alternateid: {self.alternateid}")

    def __repr__(self) -> str:
        """Return a printed representation."""
        return f"<AlignmentSet: {self.targetlanguage}, {self.identifier}>"

    def __hash__(self) -> int:
        """Return a hash key for Source."""
        return hash(self.sourceid + self.targetid + self.alternateid)

    def check_files(self) -> bool:
        """Check if files exists."""
        if not self.sourcepath.exists():
            raise ValueError(f"Missing source file: {self.sourcepath}")
        if not self.targetpath.exists():
            raise ValueError(f"Missing target file: {self.targetpath}")
        if not self.alignmentpath.exists():
            raise ValueError(f"Missing alignment file: {self.alignmentpath}")
        if not self.tomlpath.exists():
            raise ValueError(f"Missing TOML file: {self.tomlpath}")
        return True

    @property
    def identifier(self) -> str:
        """Return a string identifying the set.

        Delimiter is fixed as a hyphen (which is therefore not allowed within identifiers).
        """
        basestr = f"{self.sourceid}-{self.targetid}"
        if self.alternateid:
            basestr += f"-{self.alternateid}"
        return basestr

    @property
    def sourcepath(self) -> Path:
        """Return the path of the source file, relative to datapath."""
        return self.datapath / f"sources/{self.sourceid}.tsv"

    @property
    def targetpath(self) -> Path:
        """Return the path of the target file, relative to datapath."""
        # need to distinguish OT and NT portions of the target file
        # too fragile: this should happen better, and upstream
        return self.datapath / f"targets/{self.targetlanguage}/{self.canon}_{self.targetid}.tsv"

    @property
    def langtargetdirpath(self) -> Path:
        """Return the path of the language and target folder, relative to datapath."""
        return self.datapath / f"alignments/{self.targetlanguage}/{self.targetid}"

    @property
    def alignmentpath(self) -> Path:
        """Return the path of the alignment file, relative to datapath."""
        return self.langtargetdirpath / f"{self.identifier}.json"

    @property
    def tomlpath(self) -> Path:
        """Return the path of the TOML file, relative to datapath."""
        return self.langtargetdirpath / f"{self.identifier}.toml"

    @property
    def canon(self) -> str:
        """Return a string for the source canon: 'nt', 'ot', or 'X'."""
        if self.sourceid in ["NA27", "NA28", "SBLGNT", "BGNT"]:
            return "nt"
        elif self.sourceid in ["WLC", "WLCM"]:
            return "ot"
        else:
            return "X"

    @property
    def displaystr(self) -> str:
        """Return a string displaying configuration information."""
        return f"""
        - root: {self.datapath}
        - source: {"/".join(self.sourcepath.parts[-2:])}
        - target: {"/".join(self.targetpath.parts[-3:])}
        - alignments: {"/".join(self.alignmentpath.parts[-4:])}
        """


class Catalog(UserDict):
    """Manage data across all the alignments.

    This collects languages and versions from alignments, along with
    associated TOML metadata.  It also identifies the associated
    source and target files. It does _not_ validate the contents of
    the TOML files.

    self.data maps language codes to a dict mapping identifiers like
    'SBLGNT-BSB-manual' to AlignmentSet instances.

    """

    alignments: Path = DATAPATH / "alignments"

    def __init__(self) -> None:
        """Initialize an instance."""
        super().__init__(self)
        self.languages: list[str] = sorted([lang.name for lang in self.alignments.glob("*")])
        # HARDWIRED: needs a better approach
        self.sourceids: list[str] = ["NA28", "BGNT", "SBLGNT", "WLC", "WLCM"]
        self.targetids: defaultdict[str, list] = defaultdict(list)
        # naming conventions are hardwired here
        for lang in self.languages:
            for targetidpath in self.alignments.glob(f"{lang}/*"):
                tid = targetidpath.name
                if not tid.startswith("."):
                    self.targetids[lang].append(tid)
                    for asetpath in self.alignments.glob(f"{lang}/{tid}/*.json"):
                        alset: AlignmentSet = self._make_alignmentset(asetpath.name, lang)
                        if lang not in self.data:
                            self.data[lang] = {}
                        self.data[lang][alset.identifier] = alset

    def _make_alignmentset(self, filename: str, language: str) -> AlignmentSet:
        """Return an AlignmentSet that matches filename and language.

        Filename is from a langtargetdir path in self.alignments. Assumes
        filenames match the pattern
        <sourceid>-<targetid>[-<alternateid>].(json|toml) .

        """
        matched = re.fullmatch(r"(?P<sourceid>(\w)+)-(?P<targetid>(\w)+)(-(?P<alternateid>(\w)+)|).json", filename)
        assert matched, f"Cannot match filename {repr(filename)}"
        asdict: dict[str, str] = matched.groupdict()
        asdict.update(targetlanguage=language)
        return AlignmentSet(**asdict)

    def get_languages(self) -> list[str]:
        """Return the language codes for which AlignmentSets are available."""
        return self.languages

    def get_alignmentset_ids(self, language: str) -> list[str]:
        """Return the identifiers for AlignmentSets for language."""
        return [asetid for asetid in self[language]]

    def get_alignmentset(self, language: str, identifier: str) -> AlignmentSet:
        """Return the AlignmentSets for language and identifier."""
        assert language in self.data, f"No data for {language}"
        assert identifier in self.data[language], f"No {language} data for {identifier}"
        aset: AlignmentSet = self.data[language][identifier]
        return aset

        # self.tomlfiles = {
        #     # TODO: tomlfile.stem is sufficient to identify an
        #     # alignment. Maybe leave these three elements separate
        #     # therefore?
        #     f"{lang}+{version}+{tomlfile.stem}": tomlfile
        #     for lang, version in self.targetids
        #     for tomlfile in sorted(self.alignments.glob(f"{lang}/{version}/*.toml"))
        # }
        # self.tomldicts = {}
        # for alignedver, tomlfile in self.tomlfiles.items():
        #     if alignedver in self.tomldicts:
        #         raise ValueError(f"Duplicate alignment: {alignedver}")
        #     with tomlfile.open("rb") as f:
        #         try:
        #             self.tomldicts[alignedver] = tomli.load(f)
        #         except tomli.TOMLDecodeError as e:
        #             warn(f"Skipping {alignedver}: {e}")
        # self.commonkeys = {k for v in self.tomldicts.values() for k in v}
