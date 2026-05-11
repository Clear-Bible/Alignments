# AGENTS.md

## Overview

This repository contains word-level alignments between Greek/Hebrew source texts and Bible translations. Alignment data is in Scripture Burrito format (JSON + TOML metadata).

Python tooling to read and work with this data is in the [`biblealignlib`](https://pypi.org/project/biblealignlib/) library, available from PyPI.

```bash
pip install biblealignlib
```

## Using the Data

```python
from pathlib import Path
from biblealignlib.burrito import AlignmentSet, Manager

data = Path("/path/to/data")  # root of this repo's data/ dir, or an extracted archive
alset = AlignmentSet(
    sourceid="SBLGNT",
    targetid="BSB",
    targetlanguage="eng",
    langdatapath=data / "eng",       # language-specific subfolder
    sourcedatapath=data / "sources", # shared Greek/Hebrew TSVs
)
mgr = Manager(alset)
mgr["41004003"]  # VerseData for Mark 4:3
```

`AlignmentSet.identifier` is `"{sourceid}-{targetid}-{alternateid}"` (e.g. `SBLGNT-BSB-manual`).

## Data Model

- **`AlignmentGroup`** — Full set of alignment records for a source+target pair. Contains `Document` (source/target text identifiers), `Metadata`, and `list[AlignmentRecord]`.
- **`AlignmentRecord`** — One alignment group: maps source selectors (token IDs) to target selectors via `AlignmentReference` objects, keyed by role (`"source"`, `"target"`).
- **`Source`** / **`SourceReader`** — Token from the Greek/Hebrew source text. Fields: `id`, `altId`, `text`, `strong`, `gloss`, `gloss2`, `lemma`, `pos`, `morph`. `SourceReader` is a dict from token ID → `Source`.
- **`Target`** / **`TargetReader`** — Token from the translated text. Fields: `id`, `altId`, `text`, `source_verse`, `transType`, `isPunc`, `isPrimary`.
- **`BadRecord`** — Tracks records dropped due to missing/empty source or target selectors.

## Token Identifier Scheme

BCVWP format: 12 characters `BBCCCVVVWWWP` (book, chapter, verse, word, part).
- Source tokens drop the part index internally (stored as 11 chars), but may include it in files.
- In output/JSON, source tokens have a Macula prefix: `'n'` for NT (books 40–66), `'o'` for OT (books 01–39). The prefix is stripped when reading and re-added on output via `macula_prefixer()` / `macula_unprefixer()`.
- BCV is the first 8 chars (`BBCCCVVV`); this is used as the key in `Manager`.

## Data Directory Layout

```
data/
  sources/          # Source TSV files: SBLGNT.tsv, WLC.tsv, WLCM.tsv, BGNT.tsv
  {lang}/
    targets/{version}/{canon}_{version}.tsv   # e.g. nt_BSB.tsv, ot_BSB.tsv
    alignments/{version}/{sourceid}-{version}-{alternateid}.json
                                              # e.g. SBLGNT-BSB-manual.json
                    /{sourceid}-{version}-{alternateid}.toml  # metadata
  vref/             # Verse reference files
  legacy/           # Pre-Burrito format data
  catalog.tsv       # Generated catalog of all alignments
```

Language codes follow ISO 639-3 (e.g., `eng`, `hin`, `rus`, `fra`, `arb`).

## Key Design Notes

- Source texts:
    - OT: `WLC`, `WLCM` (WLC as provided by
      https://github.com/Clear-Bible/macula-hebrew/ )
    - NT: `SBLGNT`, `BGNT`, `NA27`, `NA28`
    - The best supported source texts are `WLCM` and `SBLGNT`.
- `alternateid` defaults to `"manual"` — distinguishes alignment variants for the same source+target pair
- `Manager` cleans bad records by default (`keepbadrecords=False`); inspect `mgr.badrecords` for details
- The deprecated `bible_alignments/` package in this repo has the same API; prefer `biblealignlib`
