# app/classifier.py

def classify_utterance(utterance: str) -> dict:
    """Classify a single utterance into Action Item, Risk, Follow-up, or Note."""
    if not isinstance(utterance, str):
        return {"type": "Note", "text": ""}

    u = utterance.strip().lower()

    # Action Items
    if any(k in u for k in ["will do", "i can", "assign", "take care", "task", "action item", "owner"]):
        return {
            "type": "Action Item",
            "text": utterance,
            "owner": "TBD",
            "timeline": "TBD"
        }

    # Risks
    elif any(k in u for k in ["risk", "issue", "delay", "blocker", "problem", "concern"]):
        return {
            "type": "Risk",
            "text": utterance,
            "severity": "Medium"
        }

    # Follow-ups
    elif any(k in u for k in ["follow up", "check back", "circle back", "update later", "pending"]):
        return {
            "type": "Follow-up",
            "text": utterance
        }

    # Notes (default)
    else:
        return {"type": "Note", "text": utterance}


def batch_classify(utterances: list) -> list:
    """Classify a list of utterances and return structured results."""
    return [classify_utterance(u) for u in utterances if isinstance(u, str)]
