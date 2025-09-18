def render_markdown(data, scored):
    """
    Render a meeting summary in markdown format with
    Action Items, Risks, Follow-ups, and Notes.
    """

    md = "## Meeting Summary\n\n"

    # --- Action Items ---
    action_items = [s for s in scored if s.get("type") == "Action Item"]
    md += "### 📝 Action Items (Owner – Task – Timeline)\n"
    if action_items:
        for a in action_items:
            owner = a.get("owner", "TBD")
            task = a.get("text", "")
            timeline = a.get("timeline", "TBD")
            md += f"- **{owner}** → {task} _(Timeline: {timeline})_\n"
    else:
        md += "_No action items found._\n"
    md += "\n"

    # --- Risks ---
    risks = [s for s in scored if s.get("type") == "Risk"]
    md += "### ⚠️ Risks\n"
    if risks:
        for r in risks:
            text = r.get("text", "")
            severity = r.get("severity", "Low")
            md += f"- {text} _(Severity: {severity})_\n"
    else:
        md += "_No risks identified._\n"
    md += "\n"

    # --- Follow-ups ---
    followups = [s for s in scored if s.get("type") == "Follow-up"]
    md += "### 🔄 Follow-ups\n"
    if followups:
        for f in followups:
            md += f"- {f.get('text', '')}\n"
    else:
        md += "_No follow-ups._\n"
    md += "\n"

    # --- Notes ---
    notes = [s for s in scored if s.get("type") == "Note"]
    md += "### 🗒️ Notes\n"
    if notes:
        for n in notes:
            md += f"- {n.get('text', '')}\n"
    else:
        md += "_No additional notes._\n"
    md += "\n"

    return md
