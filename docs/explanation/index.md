# Explanation

This documentation provides *understanding-oriented* discussion of
alignment data and processes.

## Understanding Corpus Files

### Common Attributes

* `identifier`: a word or token in a standardized reference system
    * The default reference system is BBCCCVVVWWWP, representing book,
      chapter, verse, word, and word. Alternate identification systems
      should be specified with a `referencesystem` attribute.
    * The same reference system should be used for source and target
      texts, to ensure consistency in the alignment data.


### Source Corpora

This is sample data for the first five words from Mark 1:1 :

| id | altId | text | strongs | gloss | gloss2 | lemma | pos | morph |
| -- | ----- | ---- | ------- | ----- | ------ | ----- | --- | ----- |
| n41001001001 | Ἀρχὴ-1 | Ἀρχὴ | G0746 | [The] beginning | beginning | ἀρχή | noun | N-NSF |
| n41001001002 | τοῦ-1 | τοῦ | G3588 | of the | the | ὁ | det | T-GSN |
| n41001001003 | εὐαγγελίου-1 | εὐαγγελίου | G2098 | gospel | gospel | εὐαγγέλιον | noun | N-GSN |
| n41001001004 | Ἰησοῦ-1 | Ἰησοῦ | G2424 | of Jesus | Jesus | Ἰησοῦς | noun | N-GSM |
| n41001001005 | χριστοῦ-1 | χριστοῦ | G5547 | Christ | Christ | Χριστός | noun | N-GSM |

The attributes:

* `identifier`: a word or token in a standardized reference system
    * The default reference system is BBCCCVVVWWWP, representing book,
      chapter, verse, word, and word part.
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
	
