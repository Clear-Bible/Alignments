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

## Source Text

* **`source.identifier`** (string): a standardized identifier for the source Bible
  version. 
    * Best practice: use version identifiers from a standard source,
      like [Digital Bible Library][dbl] or [eBible.org][ebible].
    * Common identifiers for the Greek New Testament include:
      `SBLGNT`, `NA1904`, `UGNT`.
	  Common identifiers for the Hebrew Bible include: `WLC`, `UHB`.
* _`source.version`_ (string): an identifier of specific version of the
  text. This might be a date or a version number.
* `source.name.<code>` (string): a localized name for the source
  version. `code` should be a three-letter ISO-639-3 code like `eng`.
    * Example: for SBLGNT, the value for `source.name.eng` would be
      "SBL Greek New Testament". 
* `source.url` (string): a web link to the actual source version text used for
  alignment. 
    * Best practice is to link to the actual text used. If that's not
      available, however, a link to another edition of the text is
      still valuable. 
* _`source.url.validated`_ (boolean): `true` if the URL is the actual
  text used for the alignment, or `false` if it can't be confirmed to
  be the same text. (It's not unusual for there to be minor variations
  between different editions of "the same" version.)


## Target Text

* **`target.identifier`** (string): a standardized identifier for the target Bible
  version. 
    * Best practice: use version identifiers from a standard target,
      like [Digital Bible Library][dbl] or [eBible.org][ebible].
* **`target.license`** (string): a license statement for the target Bible version. 
    * If the version is copyrighted, include the copyright statement
      as provided by the publisher,
      e.g. "Copyright © 2012 Logos Bible Software".
    * Otherwise use a standardized license statemen, like:
      * "Public domain"
      * "CC-BY-4.0"
* *`target.licensenotes`* (string): for additional notes on the
  license. Typically used for non-standard situations, like a
  copyrighted version with the note to "Contact the publisher for permission."
* **`target.name.eng`** (string): an English name for the target Bible version. 
* **`target.url`** (string): a web link to the actual target version text used for
  alignment. 
    * Best practice is to link to the actual text used. If that's not
      available, however, a link to another edition of the text, or
      the provider's or publisher's website is still valuable. 

## Alignment

* `alignment.format` (string): the format for the alignment data. Note
  this is not the same as the file format, since several different
  alignment formats could use the same file format. See [Alignment
  Formats](formats.md) for more information.
    * Best practice: use a standard identifier. If none exists, 
* **`alignment.identifier`** (string): a standardized identifier for
  the alignment data. 
    * Best practice: combine `source.identifier`, `target.identifier`,
      and any other identifiers as necessary for disambiguation.
    * Example: an automated alignment of ...
    * Example: a manually corrected alignment of an automated alignment ...
* **`alignment.license`** (string): a license statement for the alignment data. 
* **`alignment.process`** (string): a standardized identifier for the
  alignment process. 
    * Use `manual` for manual alignments.
* _`alignment.scope`_ (string): how much of the text is aligned?
  Common values includes "OT", "NT",  "all", "content words", or another
  descriptive string.
* _`alignment.team`_ (string): what organization did the alignment?


## Alignment Process

* _`alignment.derivedfrom`_ (string): if this alignment is a
  correction of *another alignment*, what was the source?
  Common values includes "automatic" and, "manual".
    * If "manual", indicate the initial alignment that was corrected
      using `alignment.derivedfrom`. 
* _`alignment.process`_ (string): how was the alignment performedd?
  Common values includes "automatic" and, "manual".
    * If "manual", indicate the initial alignment that was corrected
      using `alignment.derivedfrom`. 


## Correction Process



[^1]: Formatted according to [TOML: Tom's Obvious Minimal Language](https://toml.io/en/)

[dbl]: https://thedigitalbiblelibrary.org/
[ebible]: https://ebible.org/
