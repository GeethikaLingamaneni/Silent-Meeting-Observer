import streamlit as st
import pandas as pd

def render_markdown(meeting, items):
    md = f"# Meeting Summary: {meeting.get('title', 'Untitled Meeting')}\n\n"

    # ✅ Decisions
    decisions = [i for i in items if i["type"] == "Decision"]
    if decisions:
        md += "## ✅ Decisions\n"
        for d in decisions:
            md += f"- {d['text']} *(Decider: {d.get('speaker','Unknown')})*\n"
        md += "\n"

    # 📝 Action Items
    actions = [i for i in items if i["type"] == "Action"]
    if actions:
        md += "## 📝 Action Items\n"
        for a in actions:
            md += f"- {a['speaker']}: {a['text']} *(Due: {a.get('due','TBD')})*\n"
        md += "\n"

        # --- Bonus: Action Item Tracker as table ---
        md += "### 📋 Action Item Tracker\n"
        df = pd.DataFrame([
            {
                "Owner": a.get("speaker", "Unknown"),
                "Task": a["text"],
                "Due": a.get("due", "TBD"),
                "Status": a.get("status", "Open"),
            }
            for a in actions
        ])
        st.table(df)

    # ⚠️ Risks
    risks = [i for i in items if i["type"] == "Risk"]
    if risks:
        md += "## ⚠️ Risks\n"
        for r in risks:
            md += f"- {r['text']} *(Severity: {r.get('severity','Low')})*\n"
        md += "\n"

    # ℹ️ Notes
    infos = [i for i in items if i["type"] == "Info"]
    if infos:
        md += "## ℹ️ Notes\n"
        for info in infos:
            md += f"- {info['text']}\n"
        md += "\n"

    return md
