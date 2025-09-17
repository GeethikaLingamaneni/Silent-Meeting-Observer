from dataclasses import dataclass
from typing import List, Optional, Dict
import re
import dateparser
from dateutil.relativedelta import relativedelta
from datetime import datetime
import dateparser



ASSIGNMENT_PATTERNS = [
    r"\b(i|we|you|he|she|they)\s+will\b",
    r"\b(i|we|you|he|she|they)\s+can\b",
    r"\bassign(ed)?\s+(to\s+)?(?P<owner>@?\w+)\b",
    r"\b(?P<owner>@?\w+)\s+to\s+(handle|own|do|finish|complete|prepare)\b",
]
DECISION_PATTERNS = [
    r"\bwe (decided?|will|shall)\b",
    r"\bdecision\b",
    r"\bagree(d)? to\b",
]
RISK_PATTERNS = [
    r"\bmight\b", r"\bmay\b", r"\brisk\b", r"\bblocked\b",
    r"\bslip\b", r"\bdelay\b", r"\bnot sure\b", r"\bdependency\b",
    r"\bwaiting\b", r"\bpending\b"
]
DUE_DATE_PATTERNS = [
    r"\bby\s+(?P<when>(next\s+)?(mon|tue|wed|thu|fri|sat|sun|monday|tuesday|wednesday|thursday|friday|saturday|sunday))\b",
    r"\bby\s+(?P<when>tomorrow|today|eod|end of day)\b",
    r"\bby\s+(?P<when>\d{4}-\d{2}-\d{2})\b",
    r"\bby\s+(?P<when>(this|next)\s+week)\b",
    r"\bby\s+(?P<when>\w+\s+\d{1,2}(,\s*\d{4})?)\b",  # e.g., Sep 20, 2025
]

@dataclass
class Utterance:
    ts: str
    speaker: str
    text: str

def _find_owner(text: str, fallback: Optional[str]) -> Optional[str]:
    for pat in ASSIGNMENT_PATTERNS:
        m = re.search(pat, text, flags=re.IGNORECASE)
        if m:
            if "owner" in m.groupdict() and m.group("owner"):
                return m.group("owner").lstrip("@")
            # if pattern indicates self-assignment (I will…), owner = speaker (handled by caller)
            return fallback
    return None

def _find_due_date(text: str, ref: Optional[datetime] = None) -> Optional[str]:
    for pat in DUE_DATE_PATTERNS:
        m = re.search(pat, text, flags=re.IGNORECASE)
        if m:
            when = m.group("when")
            ref_dt = ref or datetime.now()
            parsed = None
            if when:
                # Map shorthand
                if when.lower() in {"eod", "end of day"}:
                    parsed = ref_dt.replace(hour=17, minute=0, second=0, microsecond=0)
                else:
                    parsed = dateparser.parse(when, settings={"RELATIVE_BASE": ref_dt})
            if parsed:
                return parsed.date().isoformat()
    return None

def classify_utterance(u: Utterance, attendees: Optional[List[str]] = None) -> Dict:
    text = u.text.strip()
    low = text.lower()

    # Decide type
    t = "Info"
    if any(re.search(p, low) for p in DECISION_PATTERNS):
        t = "Decision"
    if any(re.search(p, low) for p in ASSIGNMENT_PATTERNS):
        t = "Action"
    if any(re.search(p, low) for p in RISK_PATTERNS):
        # Risks take precedence if language contains uncertainty/blockers
        t = "Risk"

    # Owner & due date
    owner = None
    if t in {"Action", "Risk"}:
        owner = _find_owner(text, fallback=u.speaker)
        # If owner not explicitly mentioned but someone is @tagged
        if not owner:
            m = re.search(r"@(?P<name>[A-Za-z0-9_-]+)", text)
            if m:
                owner = m.group("name")
        # Validate owner against attendees if provided
        if attendees and owner and owner not in attendees:
            # best effort normalization (case-insensitive match)
            match = next((a for a in attendees if a.lower() == owner.lower()), None)
            if match:
                owner = match

    due_date = _find_due_date(text)
    topic = None  # could be inferred with keyword clustering later

    return {
        "type": t,
        "title": text,
        "speaker": u.speaker,
        "ts": u.ts,
        "text": text,
        "owner": owner if t in {"Action", "Risk"} else None,
        "due_date": due_date,
        "topic": topic,
    }

def batch_classify(utterances: List[Dict], attendees: Optional[List[str]] = None) -> List[Dict]:
    out = []
    for row in utterances:
        u = Utterance(ts=row.get("ts",""), speaker=row.get("speaker","Unknown"), text=row.get("text",""))
        out.append(classify_utterance(u, attendees=attendees))
    return out
