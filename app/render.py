# app/render.py
import io
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def render_markdown(data, scored):
    """Renders meeting summary into Markdown sections"""

    md = "# Meeting Summary\n\n"

    # --- Action Items ---
    if scored.get("Action Items"):
        md += "### 📝 Action Items (Owner – Task – Timeline)\n"
        for item in scored["Action Items"]:
            md += f"- {item['text']}\n"
        md += "\n"

    # --- Risks ---
    if scored.get("Risks"):
        md += "### ⚠️ Risks\n"
        for r in scored["Risks"]:
            sev = r.get("severity", "N/A")
            score = r.get("score", 0)
            md += f"- {r['text']} _(Severity: {sev}, Score: {score})_\n"
        md += "\n"

    # --- Follow-ups ---
    if scored.get("Follow-ups"):
        md += "### 🔄 Follow-ups\n"
        for f in scored["Follow-ups"]:
            md += f"- {f['text']}\n"
        md += "\n"
    else:
        md += "### 🔄 Follow-ups\n_No follow-ups_\n\n"

    # --- Next Meeting ---
    if scored.get("Next Meeting"):
        md += "### 📅 Next Meeting\n"
        for nm in scored["Next Meeting"]:
            md += f"- {nm['text']}\n"
        md += "\n"
    else:
        md += "### 📅 Next Meeting\n_Not scheduled_\n\n"

    # --- Brief Summary ---
    num_actions = len(scored.get("Action Items", []))
    num_risks = len(scored.get("Risks", []))
    num_followups = len(scored.get("Follow-ups", []))
    num_next = len(scored.get("Next Meeting", []))
    num_notes = len(scored.get("Additional Notes", []))

    md += "### 📝 Brief Summary\n"
    md += f"- Action Items: {num_actions}\n"
    md += f"- Risks: {num_risks}\n"
    md += f"- Follow-ups: {num_followups}\n"
    md += f"- Next Meeting: {num_next}\n"
    md += f"- Notes: {num_notes}\n"

    return md


def render_pdf(data, scored):
    """Renders meeting summary into a downloadable PDF"""

    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    y = height - 50
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "Meeting Summary")
    y -= 30

    sections = render_markdown(data, scored).split("\n")
    c.setFont("Helvetica", 10)

    for line in sections:
        if y < 50:  # new page
            c.showPage()
            y = height - 50
            c.setFont("Helvetica", 10)

        c.drawString(50, y, line)
        y -= 15

    c.save()
    buffer.seek(0)
    return buffer
