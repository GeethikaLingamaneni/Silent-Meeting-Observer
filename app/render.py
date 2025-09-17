import pandas as pd
import streamlit as st
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def create_pdf(text: str):
    """Convert plain text into a simple PDF in memory."""
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    textobject = c.beginText(40, 750)
    for line in text.split("\n"):
        textobject.textLine(line)
    c.drawText(textobject)
    c.save()
    buffer.seek(0)
    return buffer


def render_markdown(meeting, items):
    md = f"# Meeting Summary: {meeting.get('title', 'Untitled Meeting')}\n\n"

    # === 1. Action Items (Owner – Task – Timeline) ===
    actions = [i for i in items if i["type"] == "Action"]
    md += "## 📝 Action Items (Owner – Task – Timeline)\n"
    if actions:
        df = pd.DataFrame([
            {
                "Owner": a.get("speaker", "Unknown"),
                "Action Item": a["text"],
                "Timeline": a.get("due", "TBD"),
            }
            for a in actions
        ])
        st.table(df)

        # CSV download for Action Items
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="⬇️ Download Action Items (CSV)",
            data=csv,
            file_name="action_items.csv",
            mime="text/csv"
        )
    else:
        md += "_No action items recorded_\n"
    md += "\n"

    # === 2. Risks ===
    risks = [i for i in items if i["type"] == "Risk"]
    md += "## ⚠️ Risks\n"
    if risks:
        for r in risks:
            md += f"- {r['text']} *(Severity: {r.get('severity','Low')})*\n"
    else:
        md += "_No risks identified_\n"
    md += "\n"

    # === 3. Follow-ups ===
    followups = meeting.get("followups", [])
    md += "## 🔄 Follow-ups\n"
    if followups:
        for f in followups:
            md += f"- {f}\n"
    else:
        md += "_No follow-ups from previous meetings_\n"
    md += "\n"

    # === 4. Next Meeting ===
    next_meeting = meeting.get("next_meeting", None)
    md += "## 📅 Next Meeting\n"
    if next_meeting:
        md += f"- Scheduled: {next_meeting}\n"
    else:
        md += "_Next meeting not scheduled_\n"
    md += "\n"

    # --- Full Summary Downloads ---
    # TXT
    st.download_button(
        label="⬇️ Download Full Summary (TXT)",
        data=md,
        file_name="meeting_summary.txt",
        mime="text/plain"
    )

    # PDF
    pdf_buffer = create_pdf(md)
    st.download_button(
        label="⬇️ Download Full Summary (PDF)",
        data=pdf_buffer,
        file_name="meeting_summary.pdf",
        mime="application/pdf"
    )

    return md
