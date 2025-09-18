# app/render.py
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def render_markdown(data, scored: list) -> str:
    """Render markdown summary in simplified format."""
    md = "# Meeting Summary\n\n"

    # Action Items
    action_items = [s for s in scored if s["type"] == "Action Item"]
    md += "## Action Items\n"
    if action_items:
        for a in action_items:
            owner = a.get("owner", "TBD")
            task = a.get("text", "")
            timeline = a.get("timeline", "TBD")
            md += f"- {owner}: {task}: {timeline}\n"
    else:
        md += "No action items found.\n"
    md += "\n"

    # Risks
    risks = [s for s in scored if s["type"] == "Risk"]
    md += "## Risks\n"
    if risks:
        for r in risks:
            md += f"- {r['text']} (Severity: {r.get('severity','Low')})\n"
    else:
        md += "No risks identified.\n"
    md += "\n"

    # Follow-ups
    followups = [s for s in scored if s["type"] == "Follow-up"]
    md += "## Follow-ups\n"
    if followups:
        for f in followups:
            md += f"- {f['text']}\n"
    else:
        md += "No follow-ups.\n"
    md += "\n"

    # Notes
    notes = [s for s in scored if s["type"] == "Note"]
    md += "## Notes\n"
    if notes:
        for n in notes:
            md += f"- {n['text']}\n"
    else:
        md += "No notes.\n"
    md += "\n"

    return md


def render_pdf(data, scored: list):
    """Generate a PDF version of the simplified summary."""
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    text = c.beginText(50, 750)
    text.setFont("Helvetica", 11)

    text.textLine("Meeting Summary")
    text.textLine("=" * 40)
    text.textLine("")

    # Action Items
    action_items = [s for s in scored if s["type"] == "Action Item"]
    text.textLine("Action Items:")
    if action_items:
        for a in action_items:
            owner = a.get("owner", "TBD")
            task = a.get("text", "")
            timeline = a.get("timeline", "TBD")
            text.textLine(f"- {owner}: {task}: {timeline}")
    else:
        text.textLine("No action items found.")
    text.textLine("")

    # Risks
    risks = [s for s in scored if s["type"] == "Risk"]
    text.textLine("Risks:")
    if risks:
        for r in risks:
            text.textLine(f"- {r['text']} (Severity: {r.get('severity','Low')})")
    else:
        text.textLine("No risks identified.")
    text.textLine("")

    # Follow-ups
    followups = [s for s in scored if s["type"] == "Follow-up"]
    text.textLine("Follow-ups:")
    if followups:
        for f in followups:
            text.textLine(f"- {f['text']}")
    else:
        text.textLine("No follow-ups.")
    text.textLine("")

    # Notes
    notes = [s for s in scored if s["type"] == "Note"]
    text.textLine("Notes:")
    if notes:
        for n in notes:
            text.textLine(f"- {n['text']}")
    else:
        text.textLine("No notes.")
    text.textLine("")

    c.drawText(text)
    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer
