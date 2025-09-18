"""
render.py
Renders the classified meeting transcript into Markdown.
"""

def render_markdown(data: dict, scored: list) -> str:
    """
    Convert classified data into a markdown meeting summary.
    data: dict with transcript metadata
    scored: list of classified items (Action Items, Risks, Follow-ups, Notes)
    """

    md = "# Meeting Summary\n\n"

    # --- Group by type ---
    action_items = [x for x in scored if x["type"] == "Action Item"]
    risks = [x for x in scored if x["type"] == "Risk"]
    followups = [x for x in scored if x["type"] == "Follow-up"]
    notes = [x for x in scored if x["type"] == "Note"]

    # === Action Items ===
    if action_items:
        md += "## 📝 Action Items (Owner – Task – Timeline)\n"
        for a in action_items:
            md += f"- **{a.get('owner','TBD')}** → {a['text']} _(Timeline: {a.get('timeline','TBD')})_\n"
        md += "\n"

    # === Risks ===
    if risks:
        md += "## ⚠️ Risks\n"
        for r in risks:
            md += f"- {r['text']} _(Severity: {r.get('severity','Medium')})_\n"
        md += "\n"

    # === Follow-ups ===
    if followups:
        md += "## 🔄 Follow-ups\n"
        for f in followups:
            md += f"- {f['text']}\n"
        md += "\n"

    # === Notes ===
    if notes:
        md += "## 🗒️ Notes\n"
        for n in notes:
            md += f"- {n['text']}\n"
        md += "\n"

    # === Brief Summary ===
    md += "## 📌 Brief Summary\n"
    md += f"- Action Items: {len(action_items)}\n"
    md += f"- Risks: {len(risks)}\n"
    md += f"- Follow-ups: {len(followups)}\n"
    md += f"- Notes: {len(notes)}\n"

    return md
