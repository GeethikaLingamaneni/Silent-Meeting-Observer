from typing import Dict
import re
from datetime import datetime, date

HEDGE_WORDS = ["might", "may", "not sure", "probably", "try", "potential", "risk", "slip", "blocked", "waiting", "pending"]
BLOCKER_WORDS = ["blocked", "dependency", "waiting", "pending", "approval", "env down", "outage"]

def _due_in_days(due_date_iso: str) -> int:
    try:
        d = date.fromisoformat(due_date_iso)
        return (d - date.today()).days
    except Exception:
        return 9999

def score_risk(item: Dict, owner_high_pri_open: int = 0) -> Dict:
    """
    Heuristic probability:
    p = 0.25*w + 0.25*t + 0.2*h + 0.15*d + 0.15*b
    where:
      w: workload (open high-priority tasks) scaled to [0,1] with cap at 5
      t: time pressure (<=3d:1, <=7d:0.6, <=14d:0.3, else:0.1)
      h: hedge/uncertainty in text (0/1)
      d: explicit dependency mentioned (0/1)
      b: blocker words present (0/1)
    """
    if item.get("type") != "Risk":
        return item

    text = item.get("text","").lower()
    w = min(owner_high_pri_open / 5.0, 1.0)

    due_iso = item.get("due_date")
    days = _due_in_days(due_iso) if due_iso else 9999
    if days <= 3:
        t = 1.0
    elif days <= 7:
        t = 0.6
    elif days <= 14:
        t = 0.3
    else:
        t = 0.1

    h = 1.0 if any(word in text for word in HEDGE_WORDS) else 0.0
    d = 1.0 if "dependency" in text else 0.0
    b = 1.0 if any(word in text for word in BLOCKER_WORDS) else 0.0

    p = 0.25*w + 0.25*t + 0.2*h + 0.15*d + 0.15*b
    sev = "High" if p >= 0.7 else "Medium" if p >= 0.4 else "Low"

    item["probability"] = round(p, 2)
    item["severity"] = sev
    if b or d:
        item["mitigation"] = "Unblock dependencies; secure approvals; parallelize preparatory work."
    else:
        item["mitigation"] = "Clarify scope and timeline; rebalance workload; set interim check-ins."
    return item
