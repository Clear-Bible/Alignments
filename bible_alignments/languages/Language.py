"""Dataclass for managing data about a language.

Loads data from the Strategies Languages Initiative list. This
supports checking for recognized languages (via ISO-639-3 codes), and
keeps this information in one place.

Note some values are not defined in the source data, and are
represented by '' in the loaded.

>>> from bible_alignments.languages import Language
>>> lm = LanguageManager()
# information on Turkmen
>>> lm["tuk"]
Language(BCP47='tk', Language='Turkmen', ISO='tuk', Resource_Level=1, RL_Rationale='National language, few Christans, unknown L2, 6 OLs in country. Secondary to Russian. Numerical data supports RL 1', Inclusive_code='', script='')
# Language attribute is the common English name
>>> lm["tuk"].Language
'Turkmen'
# no information on the script used
>>> lm["tuk"].script
''
# code for Mandarin is 'cmn'
>>> 'man' in lm
False

>>> lm.languages_for_script("Oriya")
# just one
[Language(BCP47='or', Language='Odia', ISO='ory', Resource_Level=2, RL_Rationale='Regional LWC in India, regonized status, secondary to Hindi, supplementary texts likely valuable', Inclusive_code='', script='Oriya')]
>>> lm.languages_for_script("foo")
# none
[]

"""

from collections import UserDict
from csv import DictReader
from enum import Enum
from pathlib import Path

from pydantic import BaseModel, ValidationError, conint, constr


class SCRIPT(Enum):
    """Enumerate the scripts.

    Codes and other information at
    https://www.scriptsource.org/cms/scripts/page.php .

    """

    Adlm = "Adlam"
    Arab = "Arabic"
    Aran = "Aran"
    Beng = "Bengali"
    Cyrl = "Cyrillic"
    Deva = "Devanagari"
    Ethi = "Ethiopic"
    Geor = "Georgian"
    Gujr = "Gujarati"
    Guru = "Gurmukhi"
    Hans = "Han"
    Java = "Javanese"
    Jpan = "Japanese"
    Khmr = "Khmer"
    Knda = "Kannada"
    Kore = "Korean"
    Laoo = "Lao"
    Latn = "Latin"
    Mlym = "Malayalam"
    Mtei = "Meitei Mayek"
    Mymr = "Myanmar"
    Orya = "Oriya"
    Sinh = "Sinhala"
    Taml = "Tamil"
    Telu = "Telugu"
    Thaa = "Thaana"
    Thai = "Thai"
    Tibt = "Tibetan"


# these attributes match the headers from the source data: might be
# better to rename when loading
class Language(BaseModel):
    """Manage data about a strategic language."""

    # two-three character language code
    BCP47: constr(min_length=2, max_length=3)
    # language name in English
    Language: str
    # 3-character language code
    ISO: constr(min_length=3, max_length=3)
    # 0-4. 0 is not a valid value, but represents missing data
    Resource_Level: conint(ge=0, le=4)
    # Rational for resource level status
    RL_Rationale: str
    # ??
    Inclusive_code: str
    # script name (decoded to a name)
    script: str


class LanguageManager(UserDict):
    """Read and manage language data."""

    data_root = Path(__file__).parent.parent.parent / "data"
    languages_root = data_root / "languages/strategic-languages.v10.tsv"

    def __init__(self) -> None:
        """Initialize instance."""
        super().__init__(self)
        # read languages_root
        with self.languages_root.open("r") as infile:
            reader = DictReader(infile, delimiter="\t", restval="")
            for row in reader:
                row["Resource_Level"] = int(row["Resource_Level"])
                row["script"] = SCRIPT[row["script"]].value if row["script"] else ""
                try:
                    self.data[row["ISO"]] = Language(**row)
                except ValidationError as e:
                    print(f"Failed on {row}")
                    print(e.json())

    def languages_for_script(self, script: str) -> list[Language]:
        """Return the languages that use script."""
        return [lang for lang in self.data.values() if lang.script == script]
