import pandas as pd
import streamlit as st

def render_markdown(meeting, items):
    md = f"# Meeting Summary: {meeting.get('title', 'Untitled Meeting')}\n\n"

    # === Decisions ===
    decisions = [i for i in items if i["type"] == "Decision"]
    if decisions:
        md += "## ✅ Decisions\n"
        for d in decisions:
            md += f"- {d['text']} *(by {d.get('speaker','Unknown')})*\n"
        md += "\n"

    # === Action Items (Owner – Task – Timeline) ===
    actions = [i for i in items if i["type"] == "Action"]
    if actions:
        md += "## 📝 Action Items\n"
        df = pd.DataFrame([
            {
                "Owner": a.get("speaker", "Unknown"),
                "Action Item": a["text"],
                "Timeline": a.get("due", "TBD"),
            }
            for a in actions
        ])
        st.table(df)

    # === Additional Points ===
    extras = [i for i in items if i["type"] in ["Info", "Risk"]]
    if extras:
        md += "## ➕ Additional Points\n"
        for e in extras:
            md += f"- {e['text']}\n"
        md += "\n"

    return md
