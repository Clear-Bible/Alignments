"""Manage a set of alignment data.

This requires setting a number of parameters.

>>> from bible_alignments.burrito import AlignmentSet, DATAPATH
# your local copy of alignments-eng/data
>>> ENGLANGDATAPATH = DATAPATH.parent.parent / "alignments-eng/data"
>>> asetleb = AlignmentSet(sourceid="SBLGNT", targetid="LEB",
                           targetlanguage="eng", langdatapath=ENGLANGDATAPATH,
                           alternateid="manual")
>>> asetleb.identifier
'SBLGNT-LEB-manual'
>>> asetleb.canon
'nt'
>>> asetleb.sourcedatapath
PosixPath('/Users/sboisen/git/Clear-Bible/internal-Alignments/data/sources')
>>> asetleb.targetpath
PosixPath('/Users/sboisen/git/Clear-Bible/alignments-eng/data/targets/LEB/nt_LEB.tsv')
>>> asetleb.alignmentpath
PosixPath('/Users/sboisen/git/Clear-Bible/alignments-eng/data/alignments/LEB/SBLGNT-LEB-manual.json')
>>> asetleb.tomlpath
PosixPath('/Users/sboisen/git/Clear-Bible/alignments-eng/data/alignments/LEB/SBLGNT-LEB-manual.toml')
>>> asetleb.check_files()
True

"""

from dataclasses import dataclass
from pathlib import Path
import re
from warnings import warn

from bible_alignments import DATAPATH, SourceidEnum


@dataclass
class AlignmentSet:
    """Manage a set of files for an alignment."""

    # this should become an enumerated set
    sourceid: str
    targetid: str
    # an ISO 639-3 code (not a full name)
    targetlanguage: str
    sourcedatapath: Path = DATAPATH / "sources"
    # language-specific data path, like alignments-hin/data
    langdatapath: Path = Path()
    # most common default, but override if necessary
    alternateid: str = "manual"
    # these are computed in post-init
    sourcepath: Path = Path()
    targetpath: Path = Path()
    alignmentpath: Path = Path()
    tomlpath: Path = Path()

    def __post_init__(self) -> None:
        """Post-initialization checks."""
        for idattr in ["sourceid", "targetid"]:
            idstr = getattr(self, idattr)
            # only allow ASCII letters, digits, and underscores
            if not re.fullmatch(r"\w+", idstr, flags=re.ASCII):
                raise ValueError(f"Invalid {idattr}: {idstr}")
        if self.alternateid and not re.fullmatch(r"\w+", self.alternateid, flags=re.ASCII):
            raise ValueError(f"Invalid alternateid: {self.alternateid}")
        self.sourcepath = self.sourcedatapath / f"{self.sourceid}.tsv"
        self.targetpath = self.langdatapath / f"targets/{self.targetid}/{self.canon}_{self.targetid}.tsv"
        self.alignmentpath = self.langdatapath / f"alignments/{self.targetid}/{self.identifier}.json"
        self.tomlpath = self.langdatapath / f"alignments/{self.targetid}/{self.identifier}.toml"

    def __repr__(self) -> str:
        """Return a printed representation."""
        return f"<AlignmentSet: {self.targetlanguage}, {self.identifier}>"

    def __hash__(self) -> int:
        """Return a hash key for Source."""
        return hash(self.sourceid + self.targetid + self.alternateid)

    # def from_repo(self, repodatapath: Path) -> None:
    #     """Reset target and alignment paths for repopath.

    #     repopath should be the root of a language-specific alignment
    #     repository (like alignments-arb). This assumes conventional
    #     directory structures.

    #     """
    #     if not repodatapath.exists():
    #         raise ValueError(f"Missing repository path: {repodatapath}")
    #     # this path construction logic is fragile
    #     tpathtail = self.targetpath.relative_to(self.datapath / "targets" / self.targetlanguage)
    #     self.targetpath = (repodatapath / "targets").joinpath(tpathtail)
    #     apathtail = self.alignmentpath.relative_to(self.datapath / "alignments" / self.targetlanguage)
    #     self.alignmentpath = (repodatapath / "alignments").joinpath(apathtail)

    @property
    def identifier(self) -> str:
        """Return a string identifying the set.

        Delimiter is fixed as a hyphen (which is therefore not allowed within identifiers).
        """
        basestr = f"{self.sourceid}-{self.targetid}"
        if self.alternateid:
            basestr += f"-{self.alternateid}"
        return basestr

    # this may now be misleading since data could come from multiple paths
    # @property
    # def langtargetdirpath(self) -> Path:
    #     """Return the path of the language and target folder, relative to datapath."""
    #     return self.datapath / f"alignments/{self.targetlanguage}/{self.targetid}"

    @property
    def canon(self) -> str:
        """Return a string for the source canon: 'nt', 'ot', or 'X'."""
        return SourceidEnum.get_canon(self.sourceid)

    @property
    def displaystr(self) -> str:
        """Return a string displaying configuration information."""
        return f"""
        - sourcepath: {self.sourcepath}
        - targetpath: {self.targetpath}
        - alignmentpath: {self.alignmentpath}
        - tomlpath: {self.tomlpath}
        """

    def check_files(self) -> bool:
        """Check if files exists."""
        pathattrs = ["sourcepath", "targetpath", "alignmentpath", "tomlpath"]
        for pathattr in pathattrs:
            pathval = getattr(self, pathattr)
            if not pathval.exists():
                raise ValueError(f"Missing {pathattr} file: {pathval}")
        return True
