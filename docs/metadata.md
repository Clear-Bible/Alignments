# Alignment Metadata

Each alignment pair *must* include a `.toml` file that captures
essential and optional metadata about the pair. [^1]

Metadata is in the form of key-value pairs. The list below specifies a
number of standard keys, in the interest of descriptive consistency
(not prescription of what *must* be provided). 

* Essential attributes are in **`bold`**. In the interests of including
  data at all stages of development, these are essential, not
  "required", but some scripts may issue a warning (but still continue
  without error) if they're missing.
* Recommended attributes are in plain text. You should provide them if
  you can.
* Optional attributes are in *`italics`*. Names are provided for
  standardization, but they are not required. 
  
Any other attributes can be included without error, though they may
not get incorporated into downstream data aggregations.

All attribute values are strings unless otherwise noted.

## Common Attributes

These may have values for both source and target texts.

* **`identifier`**: a standardized identifier for the source
  or target Bible version.
    * Best practice: use version identifiers from a standard source,
      like [Digital Bible Library][dbl] or [eBible.org][ebible].
	* Best practice: for versions which have had multiple editions,
      include a date distinguishing the version (e.g. "NASB1977" vs
      "NASB1995"). 
    * Common identifiers for the Greek New Testament include:
      `SBLGNT`, `NA1904`, `UGNT`.
	  Common identifiers for the Hebrew Bible include: `WLC`, `UHB`.
* **`copyright`**: a copyright statement for the source or
  target Bible version, as provided by the publisher. This should
  indicate the copyright year(s) and the publisher, e.g. "Copyright ©
  2012 Logos Bible Software". 
    * Bibles licensed under Creative Commons typically still have a
      copyright statement that indicates who has the authority to
      declare this license.
    * Works in the public domain should _not_ have a copyright
      statement, since no one has the right to declare other licenses
      for them.
* *`license`*: a license statement for the source or target
  Bible version. For texts protected from use by copyright, no license
  statement is needed. 
    * Best practice is an abbreviation indicating a standard license,
      e.g. "CC-BY-4.0" indicating the license described at
      https://creativecommons.org/licenses/by/4.0/ .
    * The absence of a license statement indicates that the copyright
      holder must be contacted for permission to use the text. In such
      cases, the text should not be included in the alignment data:
      please contact Clear if copyright-protected text has been
      inadvertently included.
    * If the version is copyrighted (the typical case), a separate
      `copyright` statement should also be provided. This is not
      required if the license is "Public domain".
    * If the publisher intends the version to be used but only under
      special conditions, use "Custom" as the value, and indicate the
      conditions in a separate `licensenotes` field.
* *`licensenotes`*: for additional notes on the
  license. Typically used for non-standard situations, like a
  version with the note to "Contact the publisher for permission."
* `name.<code>`: a localized name for the source or target
  version. `code` should be a three-letter ISO-639-3 code like `eng`.
    * Example: for SBLGNT, the value for `source.name.eng` would be
      "SBL Greek New Testament".
	* Best practice: at least include a value for `name.eng`.
    * Best practice: for target translations, capture the vernacular
      name. 
* `url`: a web link to the actual source or target version
  text used for alignment.
    * Best practice is to link to the actual text used. If that's not
      available, however, a link to another edition of the text is
      still valuable. 

### Metadata

In some cases, there may be metadata alongside the source or target
text with a different copyright or license than the surface text
itself. For example, several GrapeCity-format alignments includes
lemmas, part of speech, morphology codes, etc. In such cases, use
separate `metadata.<attr>` attributes to capture information about
copyright, license, etc.

Example: the alignment data for `NA27-ESV` includes metadata provided
by Clear Bible, Inc. So in addition to license and copyright
attributes for the `NA27` text (which is not provided due to
copyright), the `[source]` section of the TOML file should include:

```
[source.metadata]
copyright = "Copyright (c) 2023 by Clear Bible, Inc."
license = "CC-BY 4.0"
```

and likewise for `[target.metadata]`. 

If different metadata with different copyrights and/or licensed are
mixed together, add further qualifiers that identify the type of
metadata. For example, if a source includes both lemmas and glosses
with different copyrights:

```
[source.metadata.lemmas]
copyright = "Copyright holder for lemma data."

[source.metadata.morphology]
copyright = "Copyright holder for morphology data."
```

(The metadata attributes could also have distinct identifiers,
licenses, names, etc.)

## Alignment

* `alignment.format`: the format for the alignment data. Note
  this is not the same as the file format, since several different
  alignment formats could use the same file format. See [Alignment
  Formats](formats.md) for more information.
    * Best practice: use a standard identifier. If none exists, 
* **`alignment.identifier`**: a standardized identifier for
  the alignment data. 
    * Best practice: combine `source.identifier`, `target.identifier`,
      and any other identifiers as necessary for disambiguation.
    * Example: an automated alignment of ...
    * Example: a manually corrected alignment of an automated alignment ...
* **`alignment.copyright`**: a copyright statement for the alignment
  data, if not in the public domain. See standards above.
* **`alignment.license`**: a license statement for the alignment
  data. See standards above.
* **`alignment.process`**: a standardized identifier for the
  alignment process. 
    * Use `manual` for manual alignments.
* _`alignment.scope`_: how much of the text is aligned?
  Common values includes "OT", "NT",  "all", "content words", or another
  descriptive string.
* _`alignment.provider`_: what organization did the alignment?


## Alignment Process

* _`alignment.derivedfrom`_: if this alignment is a
  correction of *another alignment*, what was the source?
  Common values includes "automatic" and, "manual".
    * If "manual", indicate the initial alignment that was corrected
      using `alignment.derivedfrom`. 
* _`alignment.process`_: how was the alignment performedd?
  Common values includes "automatic" and, "manual".
    * If "manual", indicate the initial alignment that was corrected
      using `alignment.derivedfrom`. 


## Correction Process



[^1]: Formatted according to [TOML: Tom's Obvious Minimal Language](https://toml.io/en/)

[dbl]: https://thedigitalbiblelibrary.org/
[ebible]: https://ebible.org/
