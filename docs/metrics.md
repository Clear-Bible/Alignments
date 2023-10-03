# Metrics for Alignments

We use the following abbreviations for summarizing evaluation metrics:

* A: the total number of alignments
* TP (true positives): the number of proposed alignments that match
  the gold standard
* FP (false positives): the number of proposed alignments that do not
  match the gold standard
* FN (false negatives): the number of gold standard alignments for
  which no alignment is proposed

## Intuitions on Metrics for Resource Enhancement

Word alignments support a variety of use cases. For the specific case
of enhancing resources for Bible translation, we assume:

* Full alignment of every word in source and target texts is not a
  requirement. Instead, content words are the most important, because
  (unlike function words) they are much more likely to support
  resource enhancement.
* Aligning forms that carry meaning is more important than token-level
  alignment, since the ultimate goal of resource enhancement is
  showing meaningful content for target text.
* Even within these constraints, recall overall may not be as
  important as precision. For example, many content words referring to
  common objects (body parts; objects in the natural world; etc.)
  don't need enhancement: every culture understands the ordinary sense
  of "hand", or "rock". Recall is most important for terms that refer
  to objects that aren't native to a specific culture.
    * This suggests it would be useful to have a score indicating
      _enhancement importance_ for biblical vocabulary.
* Precision is important: following an incorrect alignment to enhanced
  content will produce misleading information. 
  

## Alignment Error Rate (AER)

Computed as TP / (TP + FP)

Intuition: what percentage of many proposed alignments are incorrect? 

AER = 1 - precision. 

Fraser and Marcu (2007) argue that AER (defined by then and Och and
Ney 2003 as combining both "sure" and "possible" alignments) has
a fundamental flaw: unlike F-measure, "unbalanced precision and recall
are penalized", and therefore "it is possible to maximize AER by favoring
precision over recall". 

## F-Score

Computed as (2 * TP) / ((2 * TP) + FP + FN)

Intuition: harmonic mean of precision and recall, representing both in
a single metric.

## Precision

Intuition: how many of the predicted alignments are correct?

Precision = 1 - AER.

## Recall

Computed as TP / (TP + FN)

Intuition: how many of the correct alignments were found?

## MAP

## AO@1 (Average Overlap)

## RBO (Rank-Based Overlap)

## References

* Fraser, Alexander and Daniel Marcu. 2007. Measuring Word Alignment
  Quality for Statistical Machine Translation. Computational
  Linguistics, 33(3):293-303. 
* Och, Franz J. and Hermann Ney. 2003. A systematic comparison of
  various statistical alignment models. Computational Linguistics,
  29(1):19–51.
