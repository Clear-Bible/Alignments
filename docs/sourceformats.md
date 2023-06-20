# Source Text Formats

## `refline` Format

This format puts the text of each verse on a single line, in canonical
order, without explicit references. The file should be accompanied by
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

[^1]: So named because these files were produced by GrapeCity
    Software, a predecessor organization to Clear Bible.
