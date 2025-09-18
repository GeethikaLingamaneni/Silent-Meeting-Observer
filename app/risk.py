# app/risk.py

def score_risk(item: dict) -> dict:
    """Score risks with severity levels."""
    if item.get("type") != "Risk":
        return item

    text = item.get("text", "").lower()
    severity, score = "Low", 1

    if any(k in text for k in ["delay", "blocker", "critical", "deadline"]):
        severity, score = "High", 3
    elif any(k in text for k in ["risk", "issue", "problem"]):
        severity, score = "Medium", 2

    item["severity"] = severity
    item["score"] = score
    return item
