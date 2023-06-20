# Target Text Formats

## `refline` Format

This format puts the text of each verse on a single line, in canonical
order, without explicit references. The verses included and their
order should match that of the source file (that is, the two files
should be _synchronized_) for successful alignment.

If there is no text for a verse in the synchronized sequence
(typically because of text critical decisions), a blank line should be
left to maintain the correct synchronization. If the text for multiple
verses is combined, put the text on the first line and leave blank
lines for the remaining verses, to maintain correct synchronization.

Punctuation is typically separated from other characters by
whitespace. Other tokenization may be applied, in which case it should
be specified in the configuration file.

## GrapeCity[^1] Format

[^1]: So named because these files were produced by GrapeCity
    Software, a predecessor organization to Clear Bible.
