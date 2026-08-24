"""Preservation-first classification for The Presence Condition.

Ingestion is permissive; public curation is selective; rejection is exceptional.
Technical characteristics are recorded separately and never operate as subject bans.
"""
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional

CLASSES=("FEATURE","SUPPORTING","ARCHIVE","REVIEW","REJECT")

@dataclass
class Evidence:
    decode_ok: bool=True
    confidence: float=.75
    axes: Dict[str,float]=field(default_factory=dict)
    tags: List[str]=field(default_factory=list)
    possible_series: List[str]=field(default_factory=list)
    technical_notes: List[str]=field(default_factory=list)
    exact_duplicate_of: Optional[str]=None
    superior_duplicate_confirmed: bool=False
    near_black_ratio: float=0
    near_white_ratio: float=0
    accidental_blank_confidence: float=0
    severe_motion_blur: bool=False
    unintelligible: bool=False
    severe_obstruction: bool=False
    accidental_obstruction_confidence: float=0
    screenshot_confidence: float=0
    unintended_activation_confidence: float=0
    manual_override: Optional[str]=None

def classify(e:Evidence):
    if e.manual_override:
        if e.manual_override not in CLASSES:raise ValueError("Invalid manual override")
        return result(e,e.manual_override,1,"Manual curation override.")
    if not e.decode_ok:return result(e,"REJECT",.99,"File cannot be decoded; original remains recoverable.")
    if e.exact_duplicate_of and e.superior_duplicate_confirmed:
        return result(e,"REJECT",.97,f"Exact duplicate of {e.exact_duplicate_of}; exclusion is reversible.")
    blank=max(e.near_black_ratio,e.near_white_ratio)
    if blank>.985 and e.accidental_blank_confidence>.9:
        return result(e,"REJECT",.96,"Near-blank accidental frame with strong evidence of unintended capture.")
    if e.severe_motion_blur and e.unintelligible and e.confidence>.9:
        return result(e,"REJECT",.94,"Entire frame is unintelligible from strongly evidenced accidental motion blur.")
    if e.severe_obstruction and e.accidental_obstruction_confidence>.9:
        return result(e,"REJECT",.94,"Almost-total accidental obstruction; no readable photographic content remains.")
    if e.screenshot_confidence>.95:return result(e,"REJECT",.96,"Strongly evidenced accidental UI/screenshot asset, not a portfolio photograph.")
    if e.unintended_activation_confidence>.95:return result(e,"REJECT",.96,"Strongly evidenced unintended camera activation.")
    if e.confidence<.55:return result(e,"REVIEW",max(.5,e.confidence),"Artistic intent is ambiguous; preservation and human review are safer than exclusion.")
    values=list(e.axes.values()) or [5]
    strongest=max(values); series=e.axes.get("series_potential",0); curated=e.axes.get("curated_selection",strongest)
    if strongest>=8.5 and curated>=8 and e.confidence>=.72:
        return result(e,"FEATURE",e.confidence,"One or more photographic dimensions strongly support prominent display.")
    if strongest>=6.5 or series>=6.5 or sum(v>=6 for v in values)>=3:
        return result(e,"SUPPORTING",e.confidence,"Photographically valid with individual or series value; preserve for sequencing and display consideration.")
    return result(e,"ARCHIVE",e.confidence,"Photographically valid record retained for future interpretation, projects and re-curation.")

def result(e,classification,confidence,reason):
    return {"classification":classification,"confidence":round(float(confidence),2),"reason":reason,
      "tags":sorted(set(e.tags)),"possible_series":sorted(set(e.possible_series)),
      "technical_notes":list(e.technical_notes),"axes":dict(e.axes),"original_preserved":True}

