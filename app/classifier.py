def batch_classify(utterances):
    """
    Classify meeting transcript lines into categories:
    - Action Items
    - Risks
    - Follow-ups
    - Next Meeting
    - Additional Notes
    """

    results = {
        "Action Items": [],
        "Risks": [],
        "Follow-ups": [],
        "Next Meeting": [],
        "Additional Notes": []
    }

    for u in utterances:
        text = u.strip().lower()

        if not text:
            continue

        # --- Action Items ---
        if any(kw in text for kw in [
            "will do", "need to", "i'll", "assign", "take care", "owner",
            "action item", "task", "responsible for", "to do", "due"
        ]):
            results["Action Items"].append(u)
            continue

        # --- Risks ---
        if any(kw in text for kw in [
            "risk", "delay", "issue", "problem", "blocker", "concern",
            "dependency", "slip", "slippage"
        ]):
            results["Risks"].append(u)
            continue

        # --- Follow-ups ---
        if any(kw in text for kw in [
            "follow up", "circle back", "check again", "remind",
            "update later", "pending confirmation"
        ]):
            results["Follow-ups"].append(u)
            continue

        # --- Next Meeting ---
        if any(kw in text for kw in [
            "next meeting", "schedule", "catch up", "next week",
            "discuss further", "plan for next"
        ]):
            results["Next Meeting"].append(u)
            continue

        # --- Additional Notes ---
        results["Additional Notes"].append(u)

    return results
