import pandas as pd
import streamlit as st

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

    return md
