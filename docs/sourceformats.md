# Source Text Formats

## `vline` Format

This format puts the text of each verse on a single line, in canonical
order, without explicit references. Typically the file will be accompanied by
a file in the `references` directory such that processing both files
in parallel, line-by-line, would provide the correct reference for
each verse.

If there is no text for a verse in the standard reference sequence
(typically because of text critical decisions), a blank line should be
left to maintain the correct synchronization.

Punctuation is typically separated from other characters by
whitespace. Other tokenization may be applied, in which case it should
be specified in the configuration file.

## GrapeCity[^1] Format

### Filenames

These are typically named according to the pattern
`<source>-<target>-<process>.tsv`, where

* `source` identifies either a Greek or Hebrew source (like `NA27` or
  `WLC`)
* `target` identifies the target translation that this source is
  aligned with. Note that e.g., the file `NA27-ESV-manual.tsv` has a
  different number of lines, and therefore a different number of
  tokens, compared to `NA27-YLT-manual.tsv`, since these texts have
  minor differences in the verses they include.
* `process` identifies the process that was used in alignment: for the
  older GrapeCity files, this is always `manual` indicating the files
  were manually aligned.



[^1]: So named because these files were produced by GrapeCity
    Software, a predecessor organization to Clear Bible.
