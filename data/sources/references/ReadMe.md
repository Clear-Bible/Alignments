These files make explicit the verse numbers for specific versions in
vline format in the parent directory, using USFM references.

## Reference (`ref`) files

There are three files, one for each major canon division, together
representing the content of vref.txt file from
https://github.com/BibleNLP/ebible/blob/main/metadata/vref.txt , one
strong candidate for a standard list of verses. These contain a full
set of references, one per line, in USFM format. 

* `vref-ot-refline.txt`: the Old Testament canon
* `vref-nt-refline.txt`: the New Testament canon
* `vref-dc-refline.txt`: the Deuterocanonical books


## SBLGNT-ref.txt

This file contains the references from the published SBLGNT
(https://github.com/LogosBible/SBLGNT/tree/master/data/sblgnt/text). 

There are 18 verses that are present in some versions (including vref.txt) but are
absent from the SBLGNT, reflecting different text-critical decisions
by the editor. 

Blanks lines have been added for these in SBLGNT-vref.txt in the
parent directory, to synchronize that file with nt-ref.txt. 

MAT 17:21
MAT 18:11
MAT 23:14
MRK 7:16
MRK 9:44
MRK 9:46
MRK 11:26
MRK 15:28
LUK 17:36
LUK 23:17
JHN 5:4
ACT 8:37
ACT 15:34
ACT 24:7
ACT 28:29
ROM 16:25
ROM 16:26
ROM 16:27

Note that the latest version of the SBLGNT text on the Logos
repository _does_ include the "pericopae adulterae" verses from John
7:53-8:11. 

## N1904-ref.txt

This is extracted from the Macula Greek syntax trees for the Nestle
1904, with additional "missing" values to synchronize it with `org`.
