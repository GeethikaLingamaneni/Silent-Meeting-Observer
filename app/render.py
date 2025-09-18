# app/render.py
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def render_markdown(data, scored):
    """Convert parsed meeting data into Markdown for display in Streamlit."""
    md = "## Meeting Summary\n\n"

    # --- Action Items ---
    action_items = scored.get("Action Items", [])
    if action_items:
        md += "### ✍️ Action Items (Owner – Task – Timeline)\n"
        for item in action_items:
            md += f"- **{item.get('owner','TBD')}** — {item.get('task','')} (Due: {item.get('timeline','TBD')})\n"
    else:
        md += "### ✍️ Action Items\n_No action items found._\n"

    # --- Risks ---
    risks = scored.get("Risks", [])
    if risks:
        md += "\n### ⚠️ Risks\n"
        for r in risks:
            md += f"- {r.get('text','')} _(Severity: {r.get('severity','Low')})_\n"
    else:
        md += "\n### ⚠️ Risks\n_No risks captured._\n"

    # --- Follow-ups ---
    followups = scored.get("Follow-ups", [])
    if followups:
        md += "\n### 🔄 Follow-ups\n"
        for f in followups:
            md += f"- {f.get('text','')}\n"
    else:
        md += "\n### 🔄 Follow-ups\n_No follow-ups._\n"

    # --- Notes ---
    notes = scored.get("Notes", [])
    if notes:
        md += "\n### 📝 Additional Notes\n"
        for n in notes:
            md += f"- {n}\n"
    else:
        md += "\n### 📝 Additional Notes\n_None_\n"

    return md


def render_pdf(data, scored):
    """Generate a PDF version of the meeting summary."""
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    text = c.beginText(50, height - 50)
    text.setFont("Helvetica", 12)

    text.textLine("Meeting Summary")
    text.textLine("=" * 40)
    text.textLine("")

    # Action Items
    action_items = scored.get("Action Items", [])
    text.textLine("Action Items:")
    if action_items:
        for item in action_items:
            line = f"- {item.get('owner','TBD')}: {item.get('task','')} (Due: {item.get('timeline','TBD')})"
            text.textLine(line)
    else:
        text.textLine("No action items found.")
    text.textLine("")

    # Risks
    risks = scored.get("Risks", [])
    text.textLine("Risks:")
    if risks:
        for r in risks:
            text.textLine(f"- {r.get('text','')} (Severity: {r.get('severity','Low')})")
    else:
        text.textLine("No risks captured.")
    text.textLine("")

    # Follow-ups
    followups = scored.get("Follow-ups", [])
    text.textLine("Follow-ups:")
    if followups:
        for f in followups:
            text.textLine(f"- {f.get('text','')}")
    else:
        text.textLine("No follow-ups.")
    text.textLine("")

    # Notes
    notes = scored.get("Notes", [])
    text.textLine("Additional Notes:")
    if notes:
        for n in notes:
            text.textLine(f"- {n}")
    else:
        text.textLine("None.")
    text.textLine("")

    c.drawText(text)
    c.showPage()
    c.save()
    buffer.seek(0)

    return buffer
