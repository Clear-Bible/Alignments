# Alignment Formats

Multiple formats are currently used in the community for alignment
data. While a single shared standard would be desirable for sharing
data, and we hope one will be developed, in the meantime we will
support data in a variety of formats. 

The currently-recognized formats are listed below. If you have alignment
data in a different format, please let us know so we can support it if
possible. 


## Grape City Format

This format combines three files:

* Source: the Hebrew/Greek source text in TSV format.
    * If the source was a Grape City manual alignment, this includes
      word/morph identifiers, altId, text, strongs number, gloss,
      gloss2, lemma, pos, and morph code. If the text is copyrighted,
      altId and text are omitted. 
* Target: the translated Bible version in TSV format. 
    * If the target came from a Grape City manual alignment, this
      includes altId, text, transType, isPunc, isPrimary. If the text
      is copyrighted, altId and text are omitted. 
* Alignment: how the source and target texts are aligned. This
  supports many-to-many alignment across verse boundaries, with
  metadata for each alignment group.

### Common Attributes

* `identifier`: a word or token in a standardized reference system
    * The default reference system is BBCCCVVVWWWP, representing book,
      chapter, verse, word, and word. Alternate identification systems
      should be specified with a `referencesystem` attribute.
    * The same reference system should be used for source and target
      texts, to ensure consistency in the alignment data.


### Source Text Example

This is based on the NA27, so `altId` and `text` values are omitted.

```
identifier		altId	text	strongs	gloss				gloss2			lemma	pos		morph
400010010011	--		--		G0976	a record			A record		βίβλος	noun	n- -nsf-
400010010021	--		--		G1078	of [the] genealogy	of genealogy	γένεσις	noun	n- -gsf-
400010010031	--		--		G2424	of Jesus			of Jesus		Ἰησοῦς	Name	nr -gsm-
400010010041	--		--		G5547	Christ				Christ			Χριστός	Name	nr -gsm-
400010010051	--		--		G5207	son					son				υἱός	noun	n- -gsm-
400010010061	--		--		G1138	of David			of David Δαυίδ	Name	nr -gsm-
...
```

* `identifier`: a word or token in a standardized reference system
    * The default reference system is BBCCCVVVWWWP, representing book,
      chapter, verse, word, and word.
* `altId`: ? Omitted for copyrighted texts.
* `text`: surface text from the source. Omitted for copyrighted texts.
* `strongs`: Strongs concordance identifier for this lemma. These typically match
  the regular expression "^[A,G-H]\d\d\d\d([a-c])?$"
* `gloss`: English gloss for this lemma. Includes some context
  information.
* `gloss2`: another gloss for this lemma; typically Chinese.
* `lemma`: the dictionary form of the word.
* `pos`: Part Of Speech, one of the following values:
    * adj: adjective
    * adv: adverb
    * art: article (OT)
	* det: determiner (NT)
    * cj: conjunction (OT)
    * conj: conjunction (NT)
    * ij: interjection (OT)
    * intj: interjection (NT)
    * Name: proper name
    * noun: noun
    * num: number
    * om: omitted?
    * prep: preposition
    * pron: pronoun
    * ptcl: particle
    * rel: relative pronoun? (OT)
    * verb: verb
    * x: ?
* `morph`: encoded morphological information. Examples follow for
  several parts of speech to illustrate the patterns.
    * "a- -npf-" is an adjective (`adj`) in the nominative case,
      plural, feminine.
    * "d- -----" is an adverb (uninflected).
	* "ra -asm-" is a determiner (`det`), accusative, singular, masculine.
	* "nr -nsm-" is a name (`Name`), nominative, singular, masculine.
    * "an -apf-" is a number (`num`) in the accusative case, plural,
      feminine.
    * "n- -nsf-" is a noun in the nominative case, singular,
      feminine.
    * "rp 2gs--" is a pronoun (`pron`), second person, genitive
      singular. "rp -dsm-" is dative, singular, masculine. 
	* "v- 3-s--aai" is a verb, third person singular, active aorist
      indicative.  "v- -nsm-aap" is a nominative singular masculine,
      aorist active participle. An articular infinitive is marked as
      "v- -----ppn": present, passive, infinitive.
    * For uninflected forms, the pattern is "X- -----" where X is the
      first letter of the part of speec ("c" for conjunction, "p" for
      prep, etc.)
	  


### Target Text Example

This is based on Young's Literal Translationd.

```
identifier	altId		text	transType	isPunc	isPrimary
40001001001	A-1			A		m			False	False
40001001002	roll-1		roll	k			False	True
40001001003	of-1		of		m			False	False
40001001004	the-1		the					False	False
40001001005	birth-1		birth	k			False	True
40001001006	of-2		of		m			False	False
40001001007	Jesus-1		Jesus	k			False	True
40001001008	Christ-1	Christ	k			False	True
40001001009	,-1			,					False	False
40001001010	son-1		son		k			False	True
40001001011	of-2		of		m			False	False
40001001012	David-1		David	k			False	True
...
```

* `identifier`: book, chapter, verse, word encoded as
  BBCCCVVVWWW. Unlike the Greek and Hebrew source texts, the Grape
  City alignments at least aren't segemented and therefore  don't have
  word parts. Other alignment targets may, in which case the format
  would also include Part.
* `altId`: ? Omitted for copyrighted texts.
* `text`: surface text from the target. Omitted for copyrighted texts.
* `transType`: classifies how the translation word(s) linked to the Greek & Hebrew should be understood in relation to the source Greek & Hebrew words.
    * a: Assisted word (translation word added to assist in conveying
      the meaning & has no corresponding word in the Greek & Hebrew). 
    * d: Dynamic translation (no one-to-one correspondence between the translation & the Greek & Hebrew)
    * k: Key word (content-bearing translation word that corresponds to the Greek & Hebrew)
    * m: Morphology (translation word reflects Greek or Hebrew
      morphology and is not a separate word in the Greek or Hebrew)
    * s: Substitution (pronoun substituted with a full noun reference or a full noun substituted with a pronoun)
	* u: perhaps Union? Only occurs once for Greek in Rev 7:4 for "144"
	

### Alignment Example

```
[
{"40001001.1": {"NA27": ["400010010011"], "YLT": ["40001001002", "40001001001"], "meta": {"process": "manual"}}},
{"40001001.2": {"NA27": ["400010010021"], "YLT": ["40001001005", "40001001003"], "meta": {"process": "manual"}}},
{"40001001.3": {"NA27": ["400010010031"], "YLT": ["40001001007", "40001001006"], "meta": {"process": "manual"}}},
{"40001001.4": {"NA27": ["400010010041"], "YLT": ["40001001008"], "meta": {"process": "manual"}}},
{"40001001.5": {"NA27": ["400010010051"], "YLT": ["40001001010"], "meta": {"process": "manual"}}},
{"40001001.6": {"NA27": ["400010010061"], "YLT": ["40001001012", "40001001011"], "meta": {"process": "manual"}}},
{"40001001.7": {"NA27": ["400010010071"], "YLT": ["40001001014"], "meta": {"process": "manual"}}},
{"40001001.8": {"NA27": ["400010010081"], "YLT": ["40001001016", "40001001015"], "meta": {"process": "manual"}}},
{"40001002.1": {"NA27": ["400010020011"], "YLT": ["40001002001"], "meta": {"process": "manual"}}},
...
```

* Each row represents an *alignment group*, while the whole file is
  formatted as JSON so it can be read programmatically. 
* The key (e.g. "40001001.1") combines a verse identifier with a
  sequential counter for alignment groups: this allows extending this
  data with additional information in separate files, provided they
  use the same alignment group identifiers.
* The value is an object that identifies the source text and which
  source words are part of the alignment group (by identifier), and
  likewise for the target text. (In the example above, "NA27" is the
  source and "YLT" is the target.)
* The value object also includes a "meta" key whose value is a set of
  key-value pairs with metadata for the alignment. Often this will be
  the same for all alignment groups (as in the example above
  reflecting a manual alignment process), but this could be used to
  capture e.g., difference confidence scores for individual alignment
  groups. 

## `vref` Format

## Pharaoh Format Alignment

"Pharaoh format" is common in the machine translation community. This
represents a set of alignments for a sentence by a list of word
pair indices, separated by a dash, where many-to-one alignments are
represented by repeating the word index. Word numbers for this purpose
are zero-based (in the source data they're one-based). For the alignment example
above, but encoded in a JSON file, this would look like:

```
[
{"40001001": "0-0 0-1 1-2 1-4 2-5 2-6 3-7 4-9 5-10 5-11 6-13 7-14 7-15"},
{"40001002": "0-0 1-1 3-2 4-5 5-4 6-6 8-7 9-10 10-9 11-11 13-12 14-13 16-15 17-14"},
{"40001003": "0-1 1-0 2-2 4-3 5-4 7-5 8-6 10-7 11-10 12-9 13-11 15-12 16-15 17-14 18-16 20-17"},
...
```



## Other Formats

Other formats include useful information for alignment
purposes but are not fully-specified alignments:

* (Reverse) interlinear format: this indicates a source lemma for a
  target word, or vice versa. However, when words are repeated in a
  sentence or verse, such formats do not specify which instance is
  aligned with which, so the alignments are ambiguous.[^1]


[^1]: Hueristics might help to convert such data to a complete
    alignment. How well this works is likely to depend on the
    languages involved.
