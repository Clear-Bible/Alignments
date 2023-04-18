"""Initialize common values."""

from pathlib import Path

ROOT = Path(__file__).parent.parent
DATAPATH = ROOT / "data"

ALIGNMENTS = DATAPATH / "alignments"
SOURCES = DATAPATH / "sources"
TARGETS = DATAPATH / "targets"
NAMES = DATAPATH / "names"
