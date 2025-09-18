"""
classifier.py
Classifies each line (utterance) from a meeting transcript into:
- Action Item
- Risk
- Follow-up
- Note
"""

def classify_utterance(utterance: str) -> dict:
    """
    Classify a single utterance into Action Item, Risk, Follow-up, or Note.
    """
    if not isinstance(utterance, str):
        return {"type": "Note", "text": ""}

    u = utterance.strip().lower()

    # --- Action Items ---
    if any(keyword in u for keyword in [
        "will do", "i can", "assign", "take care", "task", "action item", "owner"
    ]):
        return {
            "type": "Action Item",
            "text": utterance,
            "owner": "TBD",         # later: NLP can detect real names
            "timeline": "TBD"
        }

    # --- Risks ---
    elif any(keyword in u for keyword in [
        "risk", "issue", "delay", "blocker", "problem", "concern"
    ]):
        return {
            "type": "Risk",
            "text": utterance,
            "severity": "Medium"    # default, will be re-scored in risk.py
        }

    # --- Follow-ups ---
    elif any(keyword in u for keyword in [
        "follow up", "check back", "circle back", "update later", "pending"
    ]):
        return {
            "type": "Follow-up",
            "text": utterance
        }

    # --- Notes (default) ---
    else:
        return {
            "type": "Note",
            "text": utterance
        }


def batch_classify(utterances: list) -> list:
    """
    Classify a list of utterances and return structured results.
    """
    results = []
    for u in utterances:
        if not isinstance(u, str):
            continue
        classified = classify_utterance(u)
        results.append(classified)
    return results
