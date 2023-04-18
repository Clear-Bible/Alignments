"""Generate a catalog of alignments.

>>> from src import catalog
>>> catalog.Catalog().write()

TODO:
- add check for missing source/target files

"""

from copy import deepcopy
from csv import DictWriter
from functools import reduce
from pathlib import Path
from warnings import warn

import tomli

from src import config


class Catalog:
    """Manage data across all the alignments"""

    alignments: Path = config.ALIGNMENTS
    catalogpath: Path = config.DATAPATH / "catalog.tsv"
    # Standard metadata attributes: warn if not present
    stdattrs: dict[str, dict[str, str]] = {
        "alignment": ["format", "identifier", "license", "process", "scope", "team"],
        "source": ["identifier", "license"],
        "target": ["identifier", "license", "name", "url"],
    }
    # no warnings, but don't include in output
    omittedattrs: dict[str, dict[str, str]] = {
        "alignment": [
            # already in the key
            "identifier",
            # aliready part of the identifier
            "process",
        ],
        "source": [
            # already in the key
            "identifier"
        ],
        "target": [
            # already in the key
            "identifier"
        ],
    }

    def __init__(self) -> None:
        """Initialize an instance."""
        self.languages = sorted([l.name for l in self.alignments.glob("*")])
        self.versions = sorted([(lang, v.name) for lang in self.languages for v in self.alignments.glob(f"{lang}/*")])
        self.tomlfiles = {
            # TODO: tomlfile.stem is sufficient to identify an
            # alignment. Maybe leave these three elements separate
            # therefore?
            f"{lang}+{version}+{tomlfile.stem}": tomlfile
            for lang, version in self.versions
            for tomlfile in sorted(self.alignments.glob(f"{lang}/{version}/*.toml"))
        }
        self.tomldicts = {}
        for alignedver, tomlfile in self.tomlfiles.items():
            with tomlfile.open("rb") as f:
                self.tomldicts[alignedver] = tomli.load(f)
        self.commonkeys = {k for v in self.tomldicts.values() for k in v}

    def write(self) -> None:
        """Write the catalog."""
        langverkey = "lang+version+alignment"
        self.langverdicts = {}
        for alignedver, tomldict in self.tomldicts.items():
            # warn if standard attrs are missing
            self._validate(alignedver, tomldict)
            stddict = deepcopy(tomldict)
            # drop non-standard pairs
            for stdk in stddict.copy():
                if stdk not in self.stdattrs:
                    warn(f"Dropping {stdk} from {alignedver} data: non-standard.")
                    del stddict[stdk]
                else:
                    for stdsubk in stddict[stdk].copy():
                        if stdsubk not in self.stdattrs[stdk]:
                            warn(f"Dropping {stdk}.{stdsubk} from {alignedver}: non-standard.")
                            del stddict[stdk][stdsubk]
                        elif stdsubk in self.omittedattrs[stdk]:
                            del stddict[stdk][stdsubk]
            self.langverdicts[alignedver] = {
                f"{k}.{subk}": stddict[k][subk] if subk in stddict[k] else ""
                for k in self.stdattrs
                for subk in self.stdattrs[k]
                if subk not in self.omittedattrs[k]
            }
            # reformat name
            fixeddict = self.langverdicts[alignedver]
            if "target.name" in fixeddict and isinstance(fixeddict["target.name"], dict):
                langcode, langname = list(fixeddict["target.name"].items())[0]
                fixeddict["target.name"] = f"'{langname}'@{langcode}"
        self.fieldnames = [langverkey] + [
            f"{k}.{subk}" for k in self.stdattrs for subk in self.stdattrs[k] if subk not in self.omittedattrs[k]
        ]
        with self.catalogpath.open("w") as f:
            writer = DictWriter(f, fieldnames=self.fieldnames, delimiter="\t")
            writer.writeheader()
            for alignedver, langverdict in self.langverdicts.items():
                # langvervalue = f"{alignedver[0]}+{alignedver[1]}"
                langverdict.update({langverkey: alignedver})
                writer.writerow(langverdict)

    # TODO: add as_markdown() to output a table
    def _validate(self, langver: str, langverdict: dict[str, dict[str, str]]) -> None:
        """Warn if standard attributes are missing."""
        for stdk in self.stdattrs:
            if stdk not in langverdict:
                warn(f"{langver} is missing standard key '{stdk}'")
            for stdsubk in self.stdattrs[stdk]:
                if stdsubk not in langverdict[stdk]:
                    warn(f"{langver} is missing standard subkey {stdsubk}")
