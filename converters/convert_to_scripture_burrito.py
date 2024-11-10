import os
import json


# These are not in the standard format.
ALIGNMENT_EXCEPTIONS = [
    "WLC-NET-manual.json",
    "WLC-CSBE-manual.json",
    "WLC-YLT-manual.json",
    "WLC-SGS-manual.json",
    "NA27-SGS-manual.json",
    "NA27-HSB-manual.json",
    "NA27-CUVMP-manual.json",
]


def find_alignment_file_paths_for_conversion():
    alignment_file_paths = []
    for root, dirs, files in os.walk("data/alignments"):
        for file in files:
            if file.endswith("-manual.json") and file not in ALIGNMENT_EXCEPTIONS:
                alignment_file_paths.append(os.path.join(root, file))
    return alignment_file_paths


def convert():
    alignment_file_paths = find_alignment_file_paths_for_conversion()

    for alignment_file_path in alignment_file_paths:
        print(alignment_file_path)
        sb_alignment = create_sb_json_structure()

        with open(alignment_file_path, "r") as file:
            alignment_data = json.load(file)
            for alignment_datum in alignment_data:
                try:
                    sb_alignment_record = create_sb_alignment_record()
                    sb_alignment_record["id"] = alignment_datum["id"]

                    for source_id in alignment_datum["source_ids"]:
                        sb_alignment_record["source"].append(source_id)
                    for target_id in alignment_datum["target_ids"]:
                        sb_alignment_record["target"].append(target_id)

                    sb_alignment["records"].append(sb_alignment_record)
                except:
                    print("Error in alignment_datum")
                    print(f"\t{alignment_file_path}")
                    print(f"\t{alignment_datum}")

        new_path = create_new_file_name(alignment_file_path)
        json.dump(sb_alignment, open(new_path, "w"), indent=2)
        # print("MIKE\n\n\n\n")
        # print(sb_alignment)


def create_sb_json_structure():
    sb_alignment = {}
    sb_alignment["type"] = "translation"
    sb_alignment["meta"] = {}
    sb_alignment["meta"]["creator"] = "GrapeCity"
    sb_alignment["records"] = []
    return sb_alignment


def create_sb_alignment_record():
    sb_alignment_record = {}
    sb_alignment_record["id"] = ""
    sb_alignment_record["source"] = []
    sb_alignment_record["target"] = []
    return sb_alignment_record


def create_new_file_name(existing_path):
    old_path_parts = existing_path.split("/")
    old_name_parts = old_path_parts[4].split("-")
    new_filename = f"{old_name_parts[0]}-{old_name_parts[1]}-manual.sb.json"
    new_path = f"{old_path_parts[0]}/{old_path_parts[1]}/{old_path_parts[2]}/{old_path_parts[3]}/{new_filename}"
    return new_path


convert()
