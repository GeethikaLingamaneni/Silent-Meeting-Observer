# app/classifier.py

def batch_classify(utterances):
    """
    Rule-based classifier for meeting transcript utterances.
    Splits into Action Items, Risks, Follow-ups, Next Meeting, Additional Notes.
    """

    results = {
        "Action Items": [],
        "Risks": [],
        "Follow-ups": [],
        "Next Meeting": [],
        "Additional Notes": []
    }

    for u in utterances:
        if isinstance(u, dict):
            text = u.get("text", "").strip()
        else:
            text = str(u).strip()

        if not text:
            continue

        lower = text.lower()

        # --- Action Items ---
        if any(kw in lower for kw in ["will do", "i'll", "we need to", "action item", "assign", "owner"]):
            results["Action Items"].append({"type": "Action Item", "text": text})

        # --- Risks ---
        elif any(kw in lower for kw in ["risk", "delay", "blocker", "issue", "problem", "concern"]):
            results["Risks"].append({"type": "Risk", "text": text})

        # --- Follow-ups ---
        elif any(kw in lower for kw in ["follow up", "circle back", "check later", "remind", "pending"]):
            results["Follow-ups"].append({"type": "Follow-up", "text": text})

        # --- Next Meeting ---
        elif any(kw in lower for kw in ["next meeting", "schedule", "let's meet", "catch up", "plan for next"]):
            results["Next Meeting"].append({"type": "Next Meeting", "text": text})

        # --- Additional Notes ---
        else:
            results["Additional Notes"].append({"type": "Note", "text": text})

    return results
