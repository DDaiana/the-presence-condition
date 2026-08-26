# The Presence Condition

The production repository for The Presence Condition (TPC): a quiet photographic archive documenting evidence of human presence.

> **Copyright:** Photographs, writing, archive structure and website code are protected. No reuse licence is granted by default. Read [COPYRIGHT.md](COPYRIGHT.md) before copying or redistributing any material.

## Local development

Requires Node.js 22.13+ and pnpm.

```sh
pnpm install
pnpm dev
pnpm build
```

## Archive ingestion

The approved incremental process is documented in [docs/PHOTOGRAPH_PROCESSING_WORKFLOW.md](docs/PHOTOGRAPH_PROCESSING_WORKFLOW.md). Follow it for every future photo intake so the current Condition edit remains unchanged.

Original photographs remain outside this repository. Point the scanner at the authoritative local directory, then build privacy-safe web derivatives:

```sh
TPC_PHOTO_SOURCE="/absolute/path/to/photography-portfolio" pnpm archive:scan
pnpm archive:classify
pnpm archive:build
pnpm archive:validate
```

The scan generates `data/photo-inventory.json` and the persistent hash-to-ID registry. It never moves, renames or modifies originals. Generated derivatives are resized JPEGs; GPS is not made public. Classification is preservation-first: decodable photographs default to retained review, `REJECT` is a reversible recommendation, and edits in `data/curation.json` override automated suggestions. Public galleries curate separately from `FEATURE` and `SUPPORTING`.

## Publication model

Archive membership, Condition assignment and public publication are separate. New photographs default to manual review and no Condition. No public description, location or Condition is invented.

## Submissions

The interface is present, but deliberately disabled until a secure backend is selected. A future adapter must use private object storage, moderation states (`submitted`, `pending_review`, `approved`/`rejected`, `published`) and environment-held credentials. Uploads must never enter the public repository automatically.

## Deployment

The production source lives in `DDaiana/the-presence-condition`. Every push to `main` builds the static site and deploys it through GitHub Pages. The Vinext/OpenAI Sites build remains supported as a secondary private deployment path. See `docs/DEPLOYMENT.md`.
