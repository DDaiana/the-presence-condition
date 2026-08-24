# Preservation-first photography system

The system assists the photographer; it does not replace artistic judgement.

## Three ordered layers

1. **Presence relationship / Condition.** Ask what had to happen between the photographer's Presence and the world for the photograph to exist. Assign exactly one Primary Condition, up to two Secondary Conditions, separate subject metadata and sequence context. If the relationship cannot be responsibly inferred, use `UNKNOWN` and request human review. Never classify Condition from the object alone.
2. **Preservation class is permissive.** Every photograph then receives `FEATURE`, `SUPPORTING`, `ARCHIVE`, `REVIEW` or `REJECT`, plus confidence, reason, tags, possible series and technical notes. A decodable photograph is retained unless there is strong evidence of corruption, an unintended blank/pocket/UI frame, an unintelligible accidental obstruction, or an exact redundant duplicate with a confirmed superior copy. `REJECT` is a reversible exclusion recommendation, never deletion.
3. **Public display is selective.** Website, exhibition and photobook sequences are edited from `FEATURE` and `SUPPORTING`. `ARCHIVE` and `REVIEW` remain preserved for future work.

Technical imperfection is a characteristic, not an automatic defect. Blur, grain, clipping, darkness, colour cast, skew, distortion, brands, people, traffic, tourist locations, ordinary objects and unconventional composition cannot independently produce `REJECT`.

## Classification meanings

- `FEATURE`: strong candidate for prominent display.
- `SUPPORTING`: useful individually or through a sequence, series, colour relationship, subject relationship or visual essay.
- `ARCHIVE`: photographically valid and retained, but not presently selected for display.
- `REVIEW`: intent or evidence is genuinely ambiguous; retain and ask a human.
- `REJECT`: only a strongly evidenced, reversible exclusion recommendation for an unusable/corrupt/accidental asset or confirmed exact redundant duplicate.

Manual decisions in `data/curation.json` take precedence over suggestions. A record can be restored simply by changing its override to `FEATURE`, `SUPPORTING`, `ARCHIVE` or `REVIEW` and rescanning.

## Why the earlier system over-rejected

The retired curation pass defaulted every undecided photograph to `CONCEPTUAL_REJECT` and asked whether each frame carried explicit TPC meaning and exhibition-level distinctiveness. That collapsed archive ingestion, conceptual interpretation and final portfolio selection into a single gate. It produced 219 conceptual rejects even though the files were valid artist-made photographs.

The corrected classifier evaluates independent photographic axes and lets one strong dimension or meaningful series role preserve a photograph. Low conceptual clarity, ordinary subject matter and technical notes do not lower eligibility.

## Public portfolio sequencing

The homepage and public archive remain authored outputs. Their edit should optimise rhythm, cohesion, pace, orientation, colour and subject relationships—not simply rank a generic technical score. A technically imperfect supporting frame may be public when it makes the sequence stronger.
