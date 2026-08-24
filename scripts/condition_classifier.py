"""TPC Conditions describe Presence-world relationships, never object classes."""
from dataclasses import dataclass,field
from typing import List,Optional
import re

CONDITIONS=("ABSENCE","TRACE","CONSUMPTION","CO-PRESENCE","SOLITARY PRESENCE","CROSSING","ATTENTION","CONTRADICTION","ARRANGEMENT","FOUND","OCCURRENCE / WITNESS","RETURN","UNKNOWN")

@dataclass
class Context:
    note:Optional[str]=None
    caption:Optional[str]=None
    subject:Optional[str]=None
    subtype:Optional[str]=None
    neighbouring_notes:List[str]=field(default_factory=list)
    sequence_id:Optional[str]=None

def classify_condition(c:Context):
    # Subject is deliberately excluded from this evidence string. A burger,
    # bench, person or building cannot determine its TPC relationship.
    text=" ".join(x for x in [c.note,c.caption,*c.neighbouring_notes] if x).lower()
    scores={k:0 for k in CONDITIONS}
    evidence=[]
    rules={
      "RETURN":[r"\b(return|again|same place|came back|revisit)"],
      "CONSUMPTION":[r"\b(eaten|ate|drank|finished meal|consumed|empty plate)"],
      "TRACE":[r"\b(left behind|remains|footprints|afterwards|disturbed|abandoned|trace)"],
      "ABSENCE":[r"\b(empty|deserted|vacant|nobody|unoccupied)"],
      "CO-PRESENCE":[r"\b(together|gathering|crowd|we were|with others)"],
      "SOLITARY PRESENCE":[r"\b(alone|waiting alone|one person|solitary)"],
      "CROSSING":[r"\b(passing|crossing|in transit|on the way|moving through)"],
      "CONTRADICTION":[r"\b(both|half.dead|old and new|occupied and empty|contradiction)"],
      "ARRANGEMENT":[r"\b(arranged|alignment|composition of|relationship between|pattern)"],
      "FOUND":[r"\b(found|lost object|discarded|unknown owner)"],
      "OCCURRENCE / WITNESS":[r"\b(happened|suddenly|unfolded|witnessed|took flight)"],
      "ATTENTION":[r"\b(noticed|caught my attention|stopped me|looked unusual)"],
    }
    for condition,patterns in rules.items():
        for pattern in patterns:
            if re.search(pattern,text):scores[condition]+=2;evidence.append(f"supported text: {pattern}")
    # A specific bodily action outranks the generic word "empty". This is
    # relationship context, not object recognition: "empty plate" alone is
    # ambiguous, while "the meal had been eaten" records consumption.
    if re.search(r"\b(eaten|ate|drank|consumed|finished meal)\b",text):
        scores["CONSUMPTION"]+=2
    ranked=sorted(((v,k) for k,v in scores.items() if k!="UNKNOWN"),reverse=True)
    if not ranked or ranked[0][0]==0:
        return {"primary_condition":"UNKNOWN","secondary_conditions":[],"confidence":.35,"reason":"Presence is certain, but available metadata and sequence context do not support a responsible relational inference.","human_review_required":True}
    top=ranked[0][0];ties=[k for v,k in ranked if v==top]
    if len(ties)>1:
        return {"primary_condition":"UNKNOWN","secondary_conditions":ties[:2],"confidence":.45,"reason":"Several Presence relationships are equally plausible; subject matter was not used to break the tie.","human_review_required":True}
    secondary=[k for v,k in ranked[1:] if v>0][:2]
    return {"primary_condition":ranked[0][1],"secondary_conditions":secondary,"confidence":.82,"reason":"Condition is supported by caption/note or neighbouring sequence evidence, independently of the visible subject.","human_review_required":False}
