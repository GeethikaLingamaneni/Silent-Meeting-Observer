# app/render.py

import io
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import pandas as pd

def ensure_dataframe(data):
    if isinstance(data, pd.DataFrame):
        return data
    elif isinstance(data, list):
        return pd.DataFrame(data)
    elif isinstance(data, dict):
        return pd.DataFrame([data])
    else:
        return pd.DataFrame()

def ensure_dict(scored):
    if isinstance(scored, dict):
        return scored
    elif isinstance(scored, list):
        return {"Risks": scored}
    else:
        return {}

def render_markdown(data, scored=None):
    data = ensure_dataframe(data)
    scored = ensure_dict(scored)

    md = "## Meeting Summary\n\n"

    # --- Action Items
    if scored.get("Action Items"):
        md += "### 📝 Action Items\n"
        for item in scored["Action Items"]:
            md += f"- {item['text']}\n"
        md += "\n"

    # --- Risks
    if scored.get("Risks"):
        md += "### ⚠️ Risks\n"
        for r in scored["Risks"]:
            sev = r.get("severity", "N/A")
            score = r.get("score", 0)
            md += f"- {r['text']} _(Severity: {sev}, Score: {score})_\n"
        md += "\n"

    # --- Follow-ups
    md += "### 🔄 Follow-ups\n"
    if scored.get("Follow-ups"):
        for f in scored["Follow-ups"]:
            md += f"- {f['text']}\n"
    else:
        md += "_No follow-ups_\n"
    md += "\n"

    # --- Next Meeting
    md += "### 📅 Next Meeting\n"
    if scored.get("Next Meeting"):
        for nm in scored["Next Meeting"]:
            md += f"- {nm['text']}\n"
    else:
        md += "_Not scheduled_\n"
    md += "\n"

    # --- Additional Notes
    if scored.get("Additional Notes"):
        md += "### 🗒 Additional Notes\n"
        for note in scored["Additional Notes"]:
            md += f"- {note['text']}\n"
        md += "\n"

    # --- Brief Summary
    md += "### 📝 Brief Summary\n"
    md += f"- Action Items: {len(scored.get('Action Items', []))}\n"
    md += f"- Risks: {len(scored.get('Risks', []))}\n"
    md += f"- Follow-ups: {len(scored.get('Follow-ups', []))}\n"
    md += f"- Next Meeting: {len(scored.get('Next Meeting', []))}\n"
    md += f"- Notes: {len(scored.get('Additional Notes', []))}\n"

    return md

def render_pdf(data, scored=None):
    data = ensure_dataframe(data)
    scored = ensure_dict(scored)

    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    text = c.beginText(40, height - 40)
    text.setFont("Helvetica", 10)

    text.textLine("Meeting Summary")
    text.textLine("")

    if scored.get("Action Items"):
        text.textLine("Action Items:")
        for item in scored["Action Items"]:
            text.textLine(f"- {item['text']}")
        text.textLine("")

    if scored.get("Risks"):
        text.textLine("Risks:")
        for r in scored["Risks"]:
            sev = r.get("severity", "N/A")
            score = r.get("score", 0)
            text.textLine(f"- {r['text']} (Severity: {sev}, Score: {score})")
        text.textLine("")

    text.textLine("Follow-ups:")
    if scored.get("Follow-ups"):
        for f in scored["Follow-ups"]:
            text.textLine(f"- {f['text']}")
    else:
        text.textLine("No follow-ups")
    text.textLine("")

    text.textLine("Next Meeting:")
    if scored.get("Next Meeting"):
        for nm in scored["Next Meeting"]:
            text.textLine(f"- {nm['text']}")
    else:
        text.textLine("Not scheduled")
    text.textLine("")

    if scored.get("Additional Notes"):
        text.textLine("Additional Notes:")
        for note in scored["Additional Notes"]:
            text.textLine(f"- {note['text']}")
        text.textLine("")

    # Brief Summary
    text.textLine("Brief Summary:")
    text.textLine(f"- Action Items: {len(scored.get('Action Items', []))}")
    text.textLine(f"- Risks: {len(scored.get('Risks', []))}")
    text.textLine(f"- Follow-ups: {len(scored.get('Follow-ups', []))}")
    text.textLine(f"- Next Meeting: {len(scored.get('Next Meeting', []))}")
    text.textLine(f"- Notes: {len(scored.get('Additional Notes', []))}")

    c.drawText(text)
    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer
