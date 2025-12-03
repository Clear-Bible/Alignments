#!/usr/bin/env python3
"""
Usage:

curl -OL https://github.com/Clear-Bible/macula-hebrew/raw/refs/heads/main/WLC/tsv/macula-hebrew.tsv?download=

python bible_alignments/scripts/map_lemmas.py \
    data/sources/WLCM+required.tsv \
    macula-hebrew.tsv

rm macula-hebrew.tsv
"""

import csv
import sys
from typing import Dict, List


def read_tsv(filename: str) -> List[Dict[str, str]]:
    """Read TSV file and return list of dictionaries."""
    with open(filename, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        return list(reader)


def write_tsv(filename: str, data: List[Dict[str, str]], fieldnames: List[str]) -> None:
    """Write list of dictionaries to TSV file."""
    with open(filename, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        writer.writerows(data)


def create_lemma_mapping(tsv2_data: List[Dict[str, str]]) -> Dict[str, str]:
    """Create mapping from xml:id to lemma from TSV2."""
    return {
        row["xml:id"]: row["lemma"]
        for row in tsv2_data
        if "xml:id" in row and "lemma" in row
    }


def update_lemmas(
    tsv1_data: List[Dict[str, str]], lemma_mapping: Dict[str, str]
) -> List[Dict[str, str]]:
    """Update lemma values in TSV1 data using mapping from TSV2."""
    updated_data = []
    for row in tsv1_data:
        if row["id"] in lemma_mapping:
            row["lemma"] = lemma_mapping[row["id"]]
        updated_data.append(row)
    return updated_data


def main():
    if len(sys.argv) != 3:
        print("Usage: python map_lemmas.py <tsv1_file> <tsv2_file>")
        sys.exit(1)

    tsv1_file = sys.argv[1]
    tsv2_file = sys.argv[2]

    try:
        # Read both TSV files
        tsv1_data = read_tsv(tsv1_file)
        tsv2_data = read_tsv(tsv2_file)

        # Create mapping from TSV2
        lemma_mapping = create_lemma_mapping(tsv2_data)

        # Update TSV1 data with lemmas from TSV2
        updated_tsv1_data = update_lemmas(tsv1_data, lemma_mapping)

        # Write updated data back to TSV1 file
        write_tsv(tsv1_file, updated_tsv1_data, list(tsv1_data[0].keys()))

        print(f"Successfully updated lemmas in {tsv1_file}")

    except FileNotFoundError as e:
        print(f"Error: Could not find file - {e}")
        sys.exit(1)
    except csv.Error as e:
        print(f"Error processing TSV file - {e}")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
