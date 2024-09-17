# Release Notes

## 0.4

Major update that restructures the `data` and `bible_alignments`
(source code) directories. 

Notable changes:
* `data` directory is now organized first by language, then by
  `alignments` and `targets`. `data/source` is structured as before
  (but cleaned out a lot of cruft and updated what’s there). This
  better matches our newer approach of separate internal repos for
  each languages alignment data (`alignments-<language code>`). 
* `bible_alignments` is re-sync’ed with our internal code with
  reorganization to make this easier in the future.

Going forward, we plan to focus on alignment data for _open_
translations, in the format specified by the [Scripture Burrito
Working Group](https://docs.burrito.bible/en/latest/) as a standard
for exchanging data. Our primary source texts are:

* The SBL Greek New Testament (SBLGNT), [Macula
  version](https://github.com/Clear-Bible/macula-greek/tree/main/SBLGNT). 
* [The Macula version of the Westminster Leningrad Codex](https://github.com/Clear-Bible/macula-hebrew/) (WLC[M])

## 0.3.5

* Support NA28 as an edition (since that's what the 'NA27' files
  really are).
* Use the identifier attribute in configuration. 

## 0.3.4

* Bumped supported Python version to anything <4, for greater generality.

## 0.3.3

* Bug fix to grapecity.py: was returning an undefined value.

## 0.3.2

* Added YLT data for NT for expository purposes.
* Fixed Open in Colab link in notebook.

## 0.3.1

* Added `dataframe()` to `grapecity.Reader` to better visualize
  alignment data for a verse.
* Added notebooks/Alignments.ipynb to show how it all works
* Other minor supporting improvements.

## 0.3.0

* Realized I wasn't including data files, which made this pretty
  pointless for pip installation. But the alignment data is pretty
  big, so I'm only including LEB alignments for now, along with
  languages, catalog, and source reference files. Now it takes much
  longer to install :-/.
    * To create a configuration rooted in a local copy of this repo,
      set the `root` property of `config.Configuration()`. 

## 0.2.17

* Fixed bug in `gcsource.Reader()` and `gctarget.Reader()` that was
  treating the header row as data.
* Updated tests for this instance.
* Fixed incorrect encoding in `test_grapecity`.

## 0.2.16

* Upgrade pydantic to 2.1.

## 0.2.15

* Fixes to `grapecity.Reader` for the new format.

## 0.2.14

- Path().parent only works when loading config.py directly: when it's
  pip-installed, it points to the venv. So made `root` a fifth
  paramemter to `Configuration()`, defaulting to the same local value
  when loaded locally, but it needs to be supplied when loaded as
  a package.

## 0.2.13

- Added `identifier` to Configuration for downstream use.
- Added URLs for several versions.
- Better error handling in catalog.py.
- Restored NET data.
- Added MSB data for Myanmar (mya).
- Minor improvements to documentation.

## 0.2.12

- Add Configuration class to manage details, and refactor around it.

## 0.2.10

- Complete renaming of module, fixing imports.

## 0.2.9

- Rename `src` to `bible_aligments` to make packaging stuff work.

## 0.2.8

- Installed module isn't importable. Change packges to include src/*.py 

## 0.2.7

- Add import of Reader from grapecity.

## 0.2.6

- Reverted to `Alignments` (not `bible-alignments`) as the repository
  name. But published to PyPI as `bible-alignments`. 

## 0.2.5

- loosened Python requirement to >=3.7

## 0.2.4

- Added grapecity.Reader().source_concordance()

## 0.2.3

- Renamed the repo to avoid PyPI collisions.
- Added minimal tests

## 0.2.2

- Updated Python version for broader applicability; some additional
  build attributes for PyPI upload.

## 0.2.0

- Initial public version, with half a dozen alignments.
