# TPC Photograph Processing Workflow

This document records the approved workflow established through the completed TPC website and photography-curation work. It is the operational source of truth for processing future photographs without disturbing the current edit.

## Approved public model

The current photograph placement is authoritative and must be preserved unless a new explicit curatorial decision changes it.

- Six public Condition categories remain active:
  - `SOMETHING HAPPENED HERE`
  - `WHILE WE WERE HERE`
  - `THINGS THAT EXISTED FOR ME`
  - `THE THINGS I DIDN'T GO LOOKING FOR`
  - `NOTHING HAPPENED HERE`
  - `BETWEEN PLACES`
- A photograph has exactly one public gallery owner: one Condition or The Presence Archive.
- Condition galleries contain only photographs approved in the curated selection (`CURATED` or `SEQUENCE_MEMBER`).
- Every other retained photograph appears in The Presence Archive, regardless of its internal taxonomy or preservation class.
- An Archive-owned photograph keeps its assigned public Condition on its detail page when one exists. Gallery ownership and displayed attribution are separate fields.
- Home/start-page photographs are an explicit editorial exception and remain visible regardless of their curatorial score.
- Originals are never renamed, moved, deleted, recompressed, cropped, or altered by this workflow.

## Permanent three-layer order

Every photograph is processed in this order:

1. **Condition relationship** — what kind of Presence the photograph records. Classification is relational, not subject-based.
2. **Preservation class** — `FEATURE`, `SUPPORTING`, `ARCHIVE`, `REVIEW`, or exceptionally `REJECT`. Ingestion is permissive and rejection is rare.
3. **Public curation** — `CURATED`, `SEQUENCE_MEMBER`, `ARCHIVE_ONLY`, or `HUMAN_REVIEW`. Only an explicit public-curation decision affects Condition-gallery inclusion.

Do not infer a Condition from the depicted object alone. Food, people, buildings, roads, animals, interiors, and objects are subject metadata; the Condition records the relationship between Presence and the encounter. Use `UNKNOWN` when the relationship cannot be responsibly inferred.

## Source of truth

The authoritative originals directory is `photography-portfolio`. Set it explicitly for every ingestion session:

```sh
export TPC_PHOTO_SOURCE="/absolute/path/to/photography-portfolio"
```

Files beginning with `TPC_` are working reports/contact sheets and are excluded from photo ingestion. The hash registry preserves stable TPC IDs. Do not manually reuse an ID.

## Safe incremental processing of new photographs

Run these commands from the repository root and in this order.

### 1. Inspect repository state

```sh
git status --short
```

Preserve unrelated and untracked user files. Do not clean or reset the worktree.

### 2. Reconcile deletions before rescanning

```sh
pnpm archive:reconcile
```

This compares the existing inventory with the source folder, removes records and web derivatives for originals deliberately deleted from the source, and removes their Condition assignments. It does not modify originals.

This step must run **before** `archive:scan`; scanning first would replace the prior inventory and erase the comparison needed to identify deletions.

### 3. Scan originals and allocate stable IDs

```sh
pnpm archive:scan
```

The scanner inventories current originals, preserves IDs through hashes, detects exact duplicates, records non-sensitive metadata, and assigns new IDs only to genuinely new files.

### 4. Register only newly discovered photographs

```sh
pnpm archive:register-new
```

This leaves every existing classification untouched. New photographs enter as:

- internal Condition: `UNKNOWN`
- preservation class: `REVIEW`
- public destination: The Presence Archive
- human review required: yes

Do **not** run `pnpm archive:classify` for routine incremental ingestion. That command is the historical full-library reclassification pass and is retained only for an explicitly authorised full re-curation.

### 5. Build privacy-safe derivatives

```sh
pnpm archive:build
```

Web JPEGs are resized and stripped of metadata. Originals remain unchanged.

### 6. Generate gallery data

```sh
pnpm archive:gallery
```

At this point new photographs appear in The Presence Archive. They cannot enter a Condition merely because an internal label, preservation class, or high technical score exists.

### 7. Validate and build

```sh
pnpm archive:validate
pnpm build
```

Validation must confirm:

- no Archive/Condition gallery overlap;
- no photograph assigned to multiple Condition routes;
- every source record has a web derivative;
- no sub-8 photograph appears in a Condition gallery;
- home editorial photographs remain routable;
- all six Condition categories retain their approved entries.

## Curating a new photograph into a Condition

Promotion is a deliberate visual-editorial task, not an ingestion side effect.

1. Inspect the full image, metadata, and neighbouring timestamps.
2. Identify subject metadata separately from TPC meaning.
3. Assign exactly one internal Primary Condition; optionally add up to two Secondary Conditions.
4. Assess photographic proficiency using composition, light, technical control, timing, visual attention, distinctiveness, atmosphere, and TPC documentary force.
5. Require an overall curatorial score of at least `8.0` for a Condition gallery.
6. Compare the image with the existing category for redundancy, rhythm, year coverage, and sequence value.
7. Add its TPC ID to exactly one list in `data/condition-assignments.json`.
8. Record the curatorial decision in `data/photograph-curation.json` (or the maintained generation source), using `CURATED` or `SEQUENCE_MEMBER`.
9. Regenerate gallery data, validate, and build.

If the photograph is not selected, keep it in The Presence Archive. Do not weaken the archive record merely because it is not portfolio-facing.

## Condition guidance

- **SOMETHING HAPPENED HERE** — transformation, consumption, residue, or visible consequence of interaction.
- **WHILE WE WERE HERE** — gatherings, travel, activities, gestures, crossing lives, or co-presence.
- **THINGS THAT EXISTED FOR ME** — a visually compelling thing, place, façade, arrangement, landscape, object, or attentive encounter.
- **THE THINGS I DIDN'T GO LOOKING FOR** — a more selective unplanned encounter, found object, animal, coincidence, or visual surprise.
- **NOTHING HAPPENED HERE** — strictly unoccupied scenes: no people, human figures, shadows, reflections, vehicles-as-active-presence, or direct human traces.
- **BETWEEN PLACES** — transit, routes, roads, stations, vehicles, thresholds, movement, or spaces whose in-between state becomes the destination.

When evidence is ambiguous, do not force a category. Keep the photograph in the Archive pending human review.

## Sequence and repetition rule

Repetition is part of TPC when it records duration, transformation, return, movement, changed attention, or before/after meaning. Preserve meaningful pairs or sequences as one curatorial unit. Suppress only interchangeable repetitions from public Condition galleries; retain all originals and Archive evidence.

## Deletion and restoration rule

- No automated process may delete an original.
- A source deletion initiated by the photographer may be mirrored by `archive:reconcile`, which removes only repository metadata and generated web derivatives.
- `REJECT` means recommended exclusion, never destruction.
- Restore an accidentally removed source file before reconciliation whenever possible.

## Commit and deployment checklist

Before publishing:

```sh
git diff --check
pnpm archive:validate
pnpm build
git status --short
```

Review the exact counts by destination and Condition. Commit only intended files; leave unrelated drafts untouched. Push to `main`, then confirm the GitHub Pages workflow completes successfully.

## Current approved baseline

At the time this workflow was registered:

- Source photographs: 266
- Curated Condition photographs: 49
- Presence Archive photographs: 217
- Archive photographs retaining an assigned Condition on their detail page: 193
- Genuinely unassigned Archive photographs: 24
- Home/start-page editorial photographs: 10
- Archive/Condition gallery overlap: 0

These figures are a baseline, not quotas. Future totals may change only through the workflow above.
