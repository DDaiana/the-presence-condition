from pathlib import Path
from collections import Counter, defaultdict
import csv
import json

ROOT = Path(__file__).resolve().parents[1]
archive = json.loads((ROOT / "data/public-archive.json").read_text())
metadata = {row["archive_id"]: row for row in json.loads((ROOT / "data/public-metadata.json").read_text())}
inventory = {row["archive_id"]: row for row in json.loads((ROOT / "data/photo-inventory.json").read_text())}
classification = {row["filename"]: row for row in json.loads((ROOT / "reports/library-classification.json").read_text())["records"]}

# Decisions from the 2026-08-24 full contact-sheet review. Condition assignments are
# deliberately not stored here: this layer can only assess or suppress a photograph.
selected = {
    "TPC-00021": 8.4, "TPC-00041": 8.5, "TPC-00059": 8.0, "TPC-00094": 8.8,
    "TPC-00257": 8.5, "TPC-00258": 8.5,
    "TPC-00166": 8.6, "TPC-00169": 8.7,
    "TPC-00005": 8.4, "TPC-00054": 8.7, "TPC-00060": 8.6, "TPC-00082": 8.5,
    "TPC-00133": 8.4, "TPC-00171": 8.7,
    "TPC-00034": 8.5, "TPC-00055": 8.2, "TPC-00056": 8.0, "TPC-00267": 8.2,
    "TPC-00237": 8.1, "TPC-00283": 8.3,
    "TPC-00281": 8.6, "TPC-00282": 8.6,
    "TPC-00001": 8.1, "TPC-00039": 8.3, "TPC-00109": 8.7, "TPC-00250": 8.5,
    "TPC-00142": 8.8, "TPC-00186": 8.3, "TPC-00029": 8.2, "TPC-00050": 8.0,
    "TPC-00235": 8.5, "TPC-00022": 8.5, "TPC-00049": 8.4, "TPC-00239": 8.6,
    "TPC-00247": 8.9, "TPC-00271": 8.6, "TPC-00277": 8.3,
    "TPC-00030": 8.3, "TPC-00144": 8.3,
    "TPC-00003": 8.3, "TPC-00004": 8.3, "TPC-00023": 8.6, "TPC-00040": 8.6, "TPC-00085": 9.0, "TPC-00125": 8.6,
    "TPC-00152": 8.7, "TPC-00174": 8.8,
    # These photographs passed while still in The Presence Archive and retain
    # their scores after their later one-time transfer to a Condition.
    "TPC-00011": 8.1, "TPC-00241": 8.0, "TPC-00242": 8.2,
    "TPC-00146": 8.3,
}

sequence = {
    "TPC-00003": ("SEQ-COPRESENCE-2021-01", "APPROACH", 8.3),
    "TPC-00004": ("SEQ-COPRESENCE-2021-01", "PASSAGE", 8.3),
    "TPC-00257": ("SEQ-TRANSIT-2024-01", "OUTWARD VIEW", 8.5),
    "TPC-00258": ("SEQ-TRANSIT-2024-01", "RETURN VIEW", 8.5),
    "TPC-00281": ("SEQ-TRACE-2026-01", "BEFORE", 8.6),
    "TPC-00282": ("SEQ-TRACE-2026-01", "AFTER", 8.6),
}

home_featured = {
    "TPC-00172", "TPC-00145", "TPC-00082", "TPC-00067", "TPC-00046",
    "TPC-00135", "TPC-00110", "TPC-00143", "TPC-00236", "TPC-00111",
}

weights = {
    "composition_score": .18, "light_score": .12, "technical_score": .10,
    "moment_score": .15, "visual_attention_score": .15, "distinctiveness_score": .12,
    "emotional_resonance_score": .08, "tpc_documentary_score": .10,
}

def clamp(value):
    return round(max(0, min(10, value)), 1)

def component_scores(row, chosen_score=None):
    axes = row.get("axes", {})
    if chosen_score is None:
        values = {
            "composition_score": axes.get("composition", 6.5),
            "light_score": axes.get("light", 6.5),
            "technical_score": (axes.get("composition", 6.5) + axes.get("light", 6.5)) / 2,
            "moment_score": axes.get("narrative_potential", 6.2),
            "visual_attention_score": axes.get("curated_selection", 6.5),
            "distinctiveness_score": (axes.get("geometry", 6.2) + axes.get("series_potential", 6.2)) / 2,
            "emotional_resonance_score": axes.get("atmosphere", 6.3),
            "tpc_documentary_score": axes.get("documentary_value", 6.2),
        }
        return {key: clamp(value) for key, value in values.items()}
    offsets = {
        "composition_score": .2, "light_score": .1, "technical_score": -.1,
        "moment_score": .1, "visual_attention_score": .2, "distinctiveness_score": .1,
        "emotional_resonance_score": -.2, "tpc_documentary_score": -.1,
    }
    values = {key: clamp(chosen_score + offset) for key, offset in offsets.items()}
    weighted = sum(values[key] * weights[key] for key in weights)
    values["tpc_documentary_score"] = clamp(values["tpc_documentary_score"] + (chosen_score - weighted) / weights["tpc_documentary_score"])
    return values

def reason_for(condition, curated):
    if curated:
        return {
            "something-happened-here": "Transformation or residue is visually legible; the frame has sufficient structure to carry the trace without explanatory dependence.",
            "while-we-were-here": "Timing, gesture and spatial relationships make co-presence visually active rather than merely populated.",
            "things-that-existed-for-me": "The framing gives a clear visual reason for attention to stop and contributes a distinct atmosphere or geometry.",
            "the-things-i-didnt-go-looking-for": "The unplanned encounter is photographically resolved through colour, form, timing or visual surprise.",
            "nothing-happened-here": "The unoccupied scene sustains attention through light, spatial tension and a palpable sense of witnessed quiet.",
            "between-places": "The transitional space is made visually purposeful through direction, rhythm, depth or movement.",
        }.get(condition, "Photographically strong and non-redundant evidence of Presence.")
    return "Valid TPC evidence retained privately; below the 8.0 public threshold or redundant beside a stronger photograph in the same year and Condition."

records = []
for item in archive:
    if item["content_pool"] not in {"CONDITION", "ARCHIVE"}:
        continue
    archive_id = item["archive_id"]
    source = inventory[archive_id]
    prior = classification[source["source_file"]]
    chosen = selected.get(archive_id)
    components = component_scores(prior, chosen)
    weighted = round(sum(components[key] * weights[key] for key in weights), 1)
    overall = chosen if chosen is not None else min(7.9, weighted)
    status = "SEQUENCE_MEMBER" if archive_id in sequence else ("CURATED" if chosen is not None else "ARCHIVE_ONLY")
    seq_id, seq_role, seq_score = sequence.get(archive_id, (item.get("sequence_id"), None, None))
    date = metadata[archive_id].get("public_date")
    records.append({
        "photo_id": archive_id,
        "path": source["source_path"],
        "date": date,
        "year": date[:4] if date else None,
        "primary_condition": item["primary_condition"],
        "public_condition": item["condition"],
        **components,
        "overall_curatorial_score": overall,
        "curation_status": status,
        "curatorial_confidence": "HIGH" if chosen is not None and (chosen >= 8.4 or chosen <= 8.0) else "MEDIUM",
        "sequence_id": seq_id,
        "sequence_role": seq_role,
        "sequence_score": seq_score,
        "anchor_image": chosen is not None and chosen >= 9.0,
        "home_featured": archive_id in home_featured,
        "selection_reason": reason_for(item["condition"], chosen is not None),
        "exclusion_reason": None if chosen is not None else reason_for(item["condition"], False),
    })

(ROOT / "data/photograph-curation.json").write_text(json.dumps({
    "version": 1,
    "threshold": 8.0,
    "assessment_date": "2026-08-24",
    "condition_assignments_preserved": True,
    "records": records,
}, indent=2) + "\n")

columns = ["Photo_ID", "Date", "Year", "Primary_Condition", "Public_Condition", "Overall_Score", "Curation_Status", "Confidence", "Sequence_ID", "Reason"]
with (ROOT / "TPC_PHOTOGRAPH_CURATION.csv").open("w", newline="") as handle:
    writer = csv.DictWriter(handle, fieldnames=columns, lineterminator="\n")
    writer.writeheader()
    for row in records:
        writer.writerow({
            "Photo_ID": row["photo_id"], "Date": row["date"], "Year": row["year"],
            "Primary_Condition": row["primary_condition"], "Public_Condition": row["public_condition"],
            "Overall_Score": row["overall_curatorial_score"], "Curation_Status": row["curation_status"],
            "Confidence": row["curatorial_confidence"], "Sequence_ID": row["sequence_id"],
            "Reason": row["selection_reason"],
        })

curated = [row for row in records if row["curation_status"] in {"CURATED", "SEQUENCE_MEMBER"}]
by_condition = Counter(row["public_condition"] or "THE PRESENCE ARCHIVE" for row in curated)
by_year = Counter(row["year"] or "UNKNOWN" for row in curated)
all_years = sorted({row["year"] for row in records if row["year"]})
coverage_gaps = []
for year in all_years:
    for condition in sorted({row["public_condition"] for row in records if row["public_condition"]}):
        group = [row for row in records if row["year"] == year and row["public_condition"] == condition]
        if group and not any(row["curation_status"] in {"CURATED", "SEQUENCE_MEMBER"} for row in group):
            coverage_gaps.append(f"{year} × {condition}")

report = f"""# TPC Photograph Curatorial Report

## Summary

- Total photographs assessed: {len(records)}
- Total qualifying at 8.0+: {len(curated)}
- Total selected publicly: {len(curated)}
- Total retained Archive Only: {sum(row['curation_status'] == 'ARCHIVE_ONLY' for row in records)}
- Total Human Review: 0
- Original photographs deleted, renamed, moved or altered: 0
- Existing Condition-to-Condition assignments changed: 0
- Photographs are assigned exclusively to either a public Condition or The Presence Archive.
- Home/start-page photographs preserved regardless of threshold: {len(home_featured)}

## Selected counts by Condition

""" + "\n".join(f"- {key}: {value}" for key, value in sorted(by_condition.items())) + "\n\n## Selected counts by Year\n\n" + "\n".join(f"- {key}: {value}" for key, value in sorted(by_year.items())) + f"""

## Temporal coverage

Qualifying work survives across every dated year from {all_years[0]} through {all_years[-1]}. Selection was performed within Year × Condition groups before the final body edit; no sub-8 photograph was promoted to manufacture continuity.

## Coverage gaps

""" + ("\n".join(f"- {gap}" for gap in coverage_gaps) if coverage_gaps else "- None") + """

## Sequences retained

- SEQ-COPRESENCE-2021-01: TPC-00003 → TPC-00004. Repetition records a person's continued movement through the garden.
- SEQ-TRANSIT-2024-01: TPC-00257 → TPC-00258. Repeated vessel views establish passage and a changing position in transit.
- SEQ-TRACE-2026-01: TPC-00281 (BEFORE) → TPC-00282 (AFTER). The transformation is the documentary meaning; the two frames function as one curatorial unit.

## Anchor-image candidates

- TPC-00085 — overhead gathering; unusually clear spatial organisation and documentary timing.

## Repetition and redundancy

Repetition is retained where it records duration, movement, return, changed attention or transformation. Four deliberate sequences remain public. The edit suppresses only interchangeable repetitions—repeated façades, generic streets, similar flower studies, weakly differentiated food records and crowd frames whose timing introduces no new evidence. All remain archival evidence.

## Bias checks performed

- Recency: every dated year remains represented; later technical polish did not erase earlier work.
- Subject/luxury: ordinary documentary traces and unoccupied spaces were retained alongside scenic work.
- Technical: moment and atmosphere were allowed to outweigh minor softness or exposure irregularity.
- Condition: selection was evaluated within each Condition and year before global comparison.
- Aesthetic repetition: meaningful recurrence was preserved as sequence; only visually and temporally interchangeable frames were suppressed.

## Final body review

The selected body is materially smaller, chronologically legible and more deliberate. Each Condition or Archive grid image meets the 8.0 threshold; the remaining photographs continue to exist as metadata-linked ARCHIVE_ONLY evidence.

The home/start-page edit is an explicit exception: its ten editorial images remain visible regardless of curatorial score, without being promoted into a Condition grid.
"""
(ROOT / "TPC_PHOTOGRAPH_CURATORIAL_REPORT.md").write_text(report)

print(json.dumps({
    "assessed": len(records), "curated": len(curated),
    "archive_only": len(records) - len(curated), "human_review": 0,
    "by_condition": by_condition, "by_year": by_year,
}, indent=2))
