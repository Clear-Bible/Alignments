"""Utilities for working with Strong's numbers.

Obligatory disclaimer: Strong's numbers are a mess, and we shouldn't
rely on them. Nevertheless, some data comes with them, so we should
maintain them, and (when forced) use them.

"""

import re


def normalize_strongs(strongs: str | int, prefix: str = "", strict: bool = False) -> str:
    """Return a normalized Strongs id."""
    _strongsre: re.Pattern = re.compile(r"[AGH]?\d{1,4}[a-d]?")
    # any other alpha suffix is eliminated
    _badsuffixre: re.Pattern = re.compile(r"[e-z]$")
    specials: dict[str, str] = {
        "1537+4053": "G4053b",
        "5228+1537+4053": "G4053c",
        "1417+3461": "G3461b",
    }
    # some weird cases from WLCM with vertical bars, like
    # "1886j|2050b". Use the number after the bar, though that
    # sometimes seems wrong.
    if isinstance(strongs, str) and "|" in strongs:
        strongs = strongs.split("|")[-1]
    # special case for uW KeyTerms data: some like G29620. It appears
    # the last digit is always zero. This assumes there's always an initial prefix
    if isinstance(strongs, str) and strongs.startswith("G") and len(strongs) == 6:
        if strongs.endswith("0"):
            strongs = strongs[:-1]
        # six char for codes like G4053b
        # else:
        #     raise ValueError(f"6-char Strong's code: {strongs}")
    # some Macula Hebrew has trailing j, z
    if isinstance(strongs, str) and _badsuffixre.search(strongs):
        strongs = strongs[:-1]
    # some special cases for SBLGNT data
    if strongs in specials:
        normed = specials[str(strongs)]
    # Macula Hebrew has some empty values: allow these if not strict
    elif strict and (strongs == "H"):
        raise ValueError("Strong's code must not be empty")
    elif isinstance(strongs, int):
        normed = f"{prefix}{strongs:0>4}"
    elif _strongsre.fullmatch(strongs):
        # check for initial prefix: save if available
        if re.match(r"[AGH]", strongs):
            firstchar = strongs[0]
            if prefix:
                if firstchar != prefix:
                    print(f"Overwriting prefix parameter {prefix} for {strongs}")
            else:
                prefix = firstchar
        base = re.sub(r"\D", "", strongs)
        # final letter
        if re.search("[a-d]$", strongs):
            suffix = strongs[-1]
        else:
            suffix = ""
        # might need other tests here
        # this drops any suffix
        assert prefix, f"prefix must be specified: {strongs}"
        normed = f"{prefix}{base:0>4}{suffix}"
    else:
        raise ValueError(f"Invalid Strong's code: {strongs}")
    return normed
