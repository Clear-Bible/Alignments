# Alignment Formats

Multiple formats are currently used in the community for alignment
data. While a single shared standard would be desirable for sharing
data, and we hope one will be developed, in the meantime we will
support data in a variety of formats. 

Here's a list of currently recognized formats. If you have alignment
data in a different format, please let us know so we can support it if
possible. 

* Alignment group format

## Alignment Group Format

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

* `identifier`: book, chapter, verse, word, word part encoded as
  BBCCCVVVWWWP.
* `altId`: ? Omitted for copyrighted texts.
* `text`: surface text from the source. Omitted for copyrighted texts.
* `strongs`: Strongs concordance identifier for this lemma.
* `gloss`: English gloss for this lemma. Includes some context
  information.
* `gloss2`: ?
* `lemma`: the dictionary form of the word.
* `pos`: Part Of Speech, one of the following values:
    * prep: preposition
    * verb: verb
    * ij: interjection
    * noun: noun
    * om: object marker
    * pron: pronoun
    * ptcl: participle
    * art: article
    * num: number
    * rel: relative pronoun
    * x: suffix
    * cj: conjunction
    * Name: proper name
    * adj: adjective
    * adv: adverb
* `morph`: encoded morphological information.
    * Example: "n- -nsf-" is a noun in the nominative case, singular, feminine.


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

### Alignment Example

```
[
{"40001001.1": {"sources": ["400010010011"], "targets": ["40001001002", "40001001001"], "meta": {"process": "manual"}}},
{"40001001.2": {"sources": ["400010010021"], "targets": ["40001001005", "40001001003"], "meta": {"process": "manual"}}},
{"40001001.3": {"sources": ["400010010031"], "targets": ["40001001007", "40001001006"], "meta": {"process": "manual"}}},
{"40001001.4": {"sources": ["400010010041"], "targets": ["40001001008"], "meta": {"process": "manual"}}},
{"40001001.5": {"sources": ["400010010051"], "targets": ["40001001010"], "meta": {"process": "manual"}}},
{"40001001.6": {"sources": ["400010010061"], "targets": ["40001001012", "40001001011"], "meta": {"process": "manual"}}},
{"40001001.7": {"sources": ["400010010071"], "targets": ["40001001014"], "meta": {"process": "manual"}}},
{"40001001.8": {"sources": ["400010010081"], "targets": ["40001001016", "40001001015"], "meta": {"process": "manual"}}},
{"40001002.1": {"sources": ["400010020011"], "targets": ["40001002001"], "meta": {"process": "manual"}}},
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
