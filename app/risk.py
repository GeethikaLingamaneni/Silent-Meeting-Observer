# app/risk.py

def score_risk(item):
    """
    Assign severity scores to risks.
    Input: dict {"type": "Risk", "text": "..."}
    Output: dict with added severity + score.
    """

    # Handle strings just in case
    if isinstance(item, str):
        item = {"type": "Risk", "text": item}

    if item.get("type") != "Risk":
        return item

    text = item.get("text", "").lower()
    score = 0
    severity = "Low"

    if "delay" in text or "slip" in text:
        score += 2
        severity = "High"
    if "issue" in text or "problem" in text:
        score += 1
        severity = "Medium"
    if "risk" in text:
        score += 1

    item["severity"] = severity
    item["score"] = score
    return item
