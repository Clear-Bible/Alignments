"""Process alignment data formatted by Grape City.

These alignments were then handed down to Global Bible Initiative (GBI), and then Clear Bible. Note that some of the target texts were typed in by hand, so may have minor differences from authoritative editions. 

The source alignment data is in JSON, with a list of objects
representing verse data. Each verse object has three keys:

- manuscript: a single key "words" whose value is a list of source
  text word/morph objects, with properties like "id", "text", "lemma",
  etc.
- translation: a single key "words" whose value is a list of target
  text word/morph objects, with properties like "id", "text",
  "isPunc", etc.
- links: a list of lists of lists, each terminal list containing one or more indexes into the manuscript and translation words (zero-based). So an element of links like [[0], [0, 1]] means the first word of the source text is aligned with the first two words of the target text.

"""


from dataclasses import dataclass
import json
from pathlib import Path

#
ROOT = Path(__file__).parent.parent
# these don't belong here
OTJSON = ROOT / "data/eng/ylt/ylt.ot.alignment.json"
NTJSON = ROOT / "data/eng/ylt/ylt.nt.alignment.json"


@dataclass
class Manuscript:
    """Manage manuscript data."""

    id: str
    altId: str
    text: str
    strong: str
    gloss: str
    gloss2: str
    lemma: str
    pos: str
    morph: str

    @staticmethod
    def fromjsondict(jdict: dict[str, str]) -> "Manuscript":
        """Return a Manuscript instance for a dictionary read from JSON."""
        # convert id attr to a str
        jdict["id"] = str(jdict["id"])
        return Manuscript(**jdict)
