# Metrics for Alignments

We use the following abbreviations for summarizing evaluation metrics:

* A: the total number of alignments
* TP (true positives): the number of proposed alignments that match
  the gold standard
* FP (false positives): the number of proposed alignments that do not
  match the gold standard
* FN (false negatives): the number of gold standard alignments for
  which no alignment is proposed

## Alignment Error Rate (AER)

Computed as TP / (TP + FP)

Intuition: what percentage of many proposed alignments are incorrect? 

AER = 1 - precision. 

Fraser and Marcu (2007) argue that AER (defined by then and Och and
Ney 2003 as combining both "sure" and "possible" alignments) has
a fundamental flaw: unlike F-measure, "unbalanced precision and recall
are penalized", and therefore "it is possible to maximize AER by favoring
precision over recall". z

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
