from pathlib import Path
import csv
import json
import os


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = Path(
    "/Users/daiana-melaniadobre/Library/Mobile Documents/com~apple~CloudDocs/"
    "001_Jimmy's business/System Feythic Live/01_ACTIVE/TPC-20260515-21/"
    "content/visual/artist-photography-portfolio"
)
SOURCE = Path(os.environ.get("TPC_PHOTO_SOURCE", DEFAULT_SOURCE))
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".heic", ".heif", ".webp", ".tif", ".tiff"}


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2) + "\n")


# Contact sheets and reports are working curation assets, not source photographs.
source_names = {
    path.name
    for path in SOURCE.iterdir()
    if path.is_file()
    and path.suffix.lower() in IMAGE_EXTENSIONS
    and not path.name.upper().startswith("TPC_")
}

inventory_path = ROOT / "data/photo-inventory.json"
inventory = json.loads(inventory_path.read_text())
removed = [row for row in inventory if row["source_file"] not in source_names]
removed_ids = {row["archive_id"] for row in removed}
removed_files = {row["source_file"] for row in removed}
inventory = [row for row in inventory if row["archive_id"] not in removed_ids]
write_json(inventory_path, inventory)

assignments_path = ROOT / "data/condition-assignments.json"
assignments = json.loads(assignments_path.read_text())
for slug in assignments:
    assignments[slug] = [archive_id for archive_id in assignments[slug] if archive_id not in removed_ids]
write_json(assignments_path, assignments)

classification_path = ROOT / "reports/library-classification.json"
classification = json.loads(classification_path.read_text())
classification["records"] = [
    row for row in classification["records"]
    if row.get("original_filename", row.get("filename")) not in removed_files
]
write_json(classification_path, classification)

curation_path = ROOT / "data/photograph-curation.json"
curation = json.loads(curation_path.read_text())
curation["records"] = [row for row in curation["records"] if row["photo_id"] not in removed_ids]
write_json(curation_path, curation)

registry_path = ROOT / "data/archive-registry.json"
registry = json.loads(registry_path.read_text())
registry = {digest: archive_id for digest, archive_id in registry.items() if archive_id not in removed_ids}
write_json(registry_path, registry)

for archive_id in removed_ids:
    derivative = ROOT / "public/archive" / f"{archive_id}.jpg"
    if derivative.exists():
        derivative.unlink()

excluded_assets = sum(
    1 for path in SOURCE.iterdir()
    if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS and path.name.upper().startswith("TPC_")
)

print(json.dumps({
    "source_photographs": len(source_names),
    "remaining_inventory": len(inventory),
    "removed_records": len(removed),
    "removed_ids": sorted(removed_ids),
    "working_assets_excluded": excluded_assets,
}, indent=2))
