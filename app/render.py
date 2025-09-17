import io
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def render_markdown(data, scored):
    """
    Convert scored classification results into a Markdown summary.
    """
    md = "## Meeting Summary\n\n"

    # === Action Items ===
    if "Action Items" in scored and scored["Action Items"]:
        md += "### ✍️ Action Items (Owner – Task – Timeline)\n"
        for item in scored["Action Items"]:
            owner = item.get("owner", "TBD")
            task = item.get("task", item.get("text", ""))
            timeline = item.get("timeline", "TBD")
            md += f"- **{owner}** — {task} _(Timeline: {timeline})_\n"
        md += "\n"

    # === Risks ===
    if "Risks" in scored and scored["Risks"]:
        md += "### ⚠️ Risks\n"
        for item in scored["Risks"]:
            text = item.get("text", "")
            severity = item.get("severity", "Low")
            score = item.get("score", 0)
            md += f"- {text} _(Severity: {severity}, Score: {score})_\n"
        md += "\n"

    # === Follow-ups ===
    if "Follow-ups" in scored and scored["Follow-ups"]:
        md += "### 🔄 Follow-ups\n"
        for item in scored["Follow-ups"]:
            md += f"- {item.get('text', '')}\n"
        md += "\n"
    else:
        md += "### 🔄 Follow-ups\n_No follow-ups_\n\n"

    # === Next Meeting ===
    if "Next Meeting" in scored and scored["Next Meeting"]:
        md += "### 📅 Next Meeting\n"
        for item in scored["Next Meeting"]:
            md += f"- {item.get('text', '')}\n"
        md += "\n"
    else:
        md += "### 📅 Next Meeting\n_Not scheduled_\n\n"

    # === Brief Summary ===
    md += "### 📝 Brief Summary\n"
    md += f"- Action Items: {len(scored.get('Action Items', []))}\n"
    md += f"- Risks: {len(scored.get('Risks', []))}\n"
    md += f"- Follow-ups: {len(scored.get('Follow-ups', []))}\n"
    md += f"- Next Meeting: {len(scored.get('Next Meeting', []))}\n"

    return md


def render_pdf(data, scored):
    """
    Render the meeting summary into a downloadable PDF.
    """
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    text = c.beginText(40, height - 50)
    text.setFont("Helvetica", 11)
    text.textLine("Meeting Summary")
    text.textLine("=" * 50)
    text.textLine("")

    # Action Items
    if "Action Items" in scored and scored["Action Items"]:
        text.textLine("Action Items:")
        for item in scored["Action Items"]:
            owner = item.get("owner", "TBD")
            task = item.get("task", item.get("text", ""))
            timeline = item.get("timeline", "TBD")
            text.textLine(f"- {owner}: {task} (Timeline: {timeline})")
        text.textLine("")

    # Risks
    if "Risks" in scored and scored["Risks"]:
        text.textLine("Risks:")
        for item in scored["Risks"]:
            txt = item.get("text", "")
            severity = item.get("severity", "Low")
            score = item.get("score", 0)
            text.textLine(f"- {txt} (Severity: {severity}, Score: {score})")
        text.textLine("")

    # Follow-ups
    text.textLine("Follow-ups:")
    if "Follow-ups" in scored and scored["Follow-ups"]:
        for item in scored["Follow-ups"]:
            text.textLine(f"- {item.get('text', '')}")
    else:
        text.textLine("No follow-ups.")
    text.textLine("")

    # Next Meeting
    text.textLine("Next Meeting:")
    if "Next Meeting" in scored and scored["Next Meeting"]:
        for item in scored["Next Meeting"]:
            text.textLine(f"- {item.get('text', '')}")
    else:
        text.textLine("Not scheduled.")
    text.textLine("")

    # Brief Summary
    text.textLine("Brief Summary:")
    text.textLine(f"- Action Items: {len(scored.get('Action Items', []))}")
    text.textLine(f"- Risks: {len(scored.get('Risks', []))}")
    text.textLine(f"- Follow-ups: {len(scored.get('Follow-ups', []))}")
    text.textLine(f"- Next Meeting: {len(scored.get('Next Meeting', []))}")

    c.drawText(text)
    c.showPage()
    c.save()

    buffer.seek(0)
    return buffer
