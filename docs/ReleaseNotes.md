# Release Notes

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
