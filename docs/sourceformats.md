# Source Text Formats

## `vref` Format[^1]

This format puts the text of each verse on a single line, in canonical
order, without explicit references. Typically the file will be accompanied by
a file in the `references` directory such that processing both files
in parallel, line-by-line, would provide the correct reference for
each verse.

If there is no text for a verse in the standard reference sequence
(typically because of text critical decisions), a blank line should be
left to maintain the correct synchronization. Only the verses that
occur in *both* source and target are included.

Punctuation is typically separated from other characters by
whitespace. Other tokenization may be applied, in which case it should
be specified in the configuration file. 

## GrapeCity[^2] Format

This provides an overview of the GrapeCity source format. See
[Alignment Formats](formats/#grape-city-format) for more details.
  
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

The TSV format may contain various columns/fields, but *must* have at
least two:

* `identifier`: a unique identifier for each token in the text,
  preferably in BCVWP format, that corresponds to the identifiers used
  in the alignments file.
* `text`: the surface text for each token

Other columns are possible. These column names are optional but for specific
purposes, and if used, should have the intended content:

* `altId`: typically the lemma followed by a hyphen and a one-up
  integer indexing how many times this lemma occurs in the verse.
* `strongs`: the Strongs number for the lemma.
* `after`: indicates one or more non-whitespace characters (like
  punctuation) that should follow this token without intervening
  whitespace. Typically used when punctuation is not treated as a
  separate token. 
* `gloss`: an English gloss for the lemma
* `gloss2`: another gloss for the lemma, typically Chinese
* `lemma`: the dictionary form of the word
* `pos`: part of speech abbreviation.
* `morph`: coded information about the morphology of the token

Other columns are allowed, but should be documented, and will require
custom readers.

[^1]: This name comes from Paratext.
[^2]: So named because these files were produced by GrapeCity
    Software, a predecessor organization to Clear Bible.
