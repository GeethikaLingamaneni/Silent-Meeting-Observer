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
        # if it's a dict, get the 'text' field
        if isinstance(u, dict):
            text = u.get("text", "").strip()
        else:
            text = str(u).strip()

        if not text:
            continue

        low = text.lower()

        # --- Action Items ---
        if any(kw in low for kw in [
            "will do", "need to", "i'll", "assign", "take care", "owner",
            "action item", "task", "responsible for", "to do", "due"
        ]):
            results["Action Items"].append(text)
            continue

        # --- Risks ---
        if any(kw in low for kw in [
            "risk", "delay", "issue", "problem", "blocker", "concern",
            "dependency", "slip", "slippage"
        ]):
            results["Risks"].append(text)
            continue

        # --- Follow-ups ---
        if any(kw in low for kw in [
            "follow up", "circle back", "check again", "remind",
            "update later", "pending confirmation"
        ]):
            results["Follow-ups"].append(text)
            continue

        # --- Next Meeting ---
        if any(kw in low for kw in [
            "next meeting", "schedule", "catch up", "next week",
            "discuss further", "plan for next"
        ]):
            results["Next Meeting"].append(text)
            continue

        # --- Additional Notes ---
        results["Additional Notes"].append(text)

    return results
