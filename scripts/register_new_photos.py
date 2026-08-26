from pathlib import Path
import json


ROOT = Path(__file__).resolve().parents[1]
INVENTORY = ROOT / "data/photo-inventory.json"
CLASSIFICATION = ROOT / "reports/library-classification.json"


inventory = json.loads(INVENTORY.read_text())
document = json.loads(CLASSIFICATION.read_text())
records = document["records"]
known = {row.get("original_filename", row.get("filename")) for row in records}
added = []

for photo in inventory:
    filename = photo["source_file"]
    if filename in known:
        continue
    record = {
        "primary_condition": "UNKNOWN",
        "secondary_conditions": [],
        "confidence": 0.35,
        "reason": "New photograph registered without altering the established curation; visual review is required.",
        "human_review_required": True,
        "subject": "Other",
        "subject_subtype": "visual subject requires human confirmation",
        "subject_confidence": 0.2,
        "subject_review_required": True,
        "sequence_id": None,
        "sequence_position": None,
        "sequence_neighbours": [],
        "classification": "REVIEW",
        "tags": ["documentary", "everyday-life", "observational"],
        "possible_series": [],
        "technical_notes": [],
        "axes": {
            "composition": 0, "light": 0, "colour": 0, "atmosphere": 0,
            "documentary_value": 0, "sense_of_place": 0, "geometry": 0,
            "texture": 0, "narrative_potential": 0,
            "sequencing_potential": 0, "series_potential": 0,
            "curated_selection": 0,
        },
        "original_preserved": True,
        "filename": filename,
        "original_filename": filename,
        "previous_classification": None,
        "metrics": {
            "width": photo.get("width"), "height": photo.get("height"),
            "mean": None, "contrast": None, "saturation": None,
            "edge": None, "black": None, "white": None, "rgb": None,
        },
        "layer_order_applied": ["CONDITION", "PRESERVATION", "PUBLIC_DISPLAY"],
    }
    records.append(record)
    added.append({"archive_id": photo["archive_id"], "filename": filename})

document["records"] = records
CLASSIFICATION.write_text(json.dumps(document, indent=2) + "\n")
print(json.dumps({"new_photographs_registered": len(added), "records": added}, indent=2))
