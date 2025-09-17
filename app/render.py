import streamlit as st
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import pandas as pd
import io

def ensure_dataframe(data):
    """Convert input into a DataFrame if it's a list/dict."""
    if isinstance(data, pd.DataFrame):
        return data
    elif isinstance(data, list):
        return pd.DataFrame(data)
    elif isinstance(data, dict):
        return pd.DataFrame([data])
    else:
        return pd.DataFrame()

def render_markdown(data, scored=None):
    data = ensure_dataframe(data)  # ✅ make sure it's a DataFrame
    md = "## Meeting Summary\n\n"

    # --- 1. Action Items
    if not data.empty and "Action Item" in data.columns:
        md += "### 📝 Action Items (Owner – Task – Timeline)\n"
        for _, row in data.iterrows():
            owner = row.get("Owner", "Unknown")
            task = row.get("Action Item", "No task")
            timeline = row.get("Timeline", "TBD")
            md += f"- **{owner}**: {task} _(Timeline: {timeline})_\n"
        md += "\n"

    # --- 2. Risks
    if scored and "Risks" in scored:
        md += "### ⚠️ Risks\n"
        for r in scored["Risks"]:
            md += f"- {r}\n"
        md += "\n"

    # --- 3. Follow-ups
    followups = scored.get("Follow-ups", []) if scored else []
    md += "### 🔄 Follow-ups\n"
    if followups:
        for f in followups:
            md += f"- {f}\n"
    else:
        md += "_No follow-ups from previous meetings_\n"
    md += "\n"

    # --- 4. Next Meeting
    next_meeting = scored.get("Next Meeting") if scored else None
    md += "### 📅 Next Meeting\n"
    if next_meeting:
        md += f"- {next_meeting}\n"
    else:
        md += "_Next meeting not scheduled_\n"
    md += "\n"

    # --- 5. Brief Summary (at the bottom)
    num_actions = len(data) if not data.empty else 0
    num_risks = len(scored["Risks"]) if scored and "Risks" in scored else 0
    has_followups = bool(followups)
    has_next_meeting = bool(next_meeting)

    md += "### 📝 Brief Summary\n"
    md += f"- **Action Items**: {num_actions}\n"
    md += f"- **Risks**: {num_risks}\n"
    md += f"- **Follow-ups**: {'Yes' if has_followups else 'No'}\n"
    md += f"- **Next Meeting**: {'Scheduled' if has_next_meeting else 'Not scheduled'}\n\n"

    return md

def render_pdf(data, scored=None):
    data = ensure_dataframe(data)  # ✅ make sure it's a DataFrame
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    text = c.beginText(40, height - 40)
    text.setFont("Helvetica", 10)

    text.textLine("Meeting Summary")
    text.textLine("")

    if not data.empty and "Action Item" in data.columns:
        text.textLine("Action Items (Owner – Task – Timeline):")
        for _, row in data.iterrows():
            owner = row.get("Owner", "Unknown")
            task = row.get("Action Item", "No task")
            timeline = row.get("Timeline", "TBD")
            text.textLine(f"- {owner}: {task} (Timeline: {timeline})")
        text.textLine("")

    if scored and "Risks" in scored:
        text.textLine("Risks:")
        for r in scored["Risks"]:
            text.textLine(f"- {r}")
        text.textLine("")

    followups = scored.get("Follow-ups", []) if scored else []
    text.textLine("Follow-ups:")
    if followups:
        for f in followups:
            text.textLine(f"- {f}")
    else:
        text.textLine("No follow-ups from previous meetings")
    text.textLine("")

    next_meeting = scored.get("Next Meeting") if scored else None
    text.textLine("Next Meeting:")
    if next_meeting:
        text.textLine(f"- {next_meeting}")
    else:
        text.textLine("Next meeting not scheduled")
    text.textLine("")

    # Brief Summary
    num_actions = len(data) if not data.empty else 0
    num_risks = len(scored["Risks"]) if scored and "Risks" in scored else 0
    has_followups = bool(followups)
    has_next_meeting = bool(next_meeting)

    text.textLine("Brief Summary:")
    text.textLine(f"- Action Items: {num_actions}")
    text.textLine(f"- Risks: {num_risks}")
    text.textLine(f"- Follow-ups: {'Yes' if has_followups else 'No'}")
    text.textLine(f"- Next Meeting: {'Scheduled' if has_next_meeting else 'Not scheduled'}")

    c.drawText(text)
    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer
