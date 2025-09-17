import streamlit as st
import json
from typing import Dict, List
from app.classifier import batch_classify
from app.risk import score_risk
from app.render import render_markdown

st.set_page_config(page_title="Silent Meeting Observer", layout="centered")
st.title("🤖 Silent Meeting Observer")
st.caption("Classifies Decisions / Actions / Risks / Info from meeting transcripts and renders a 1-page summary.")

with st.expander("How to use"):
    st.markdown("""
1. Upload a **JSON transcript** or paste **plain text** (one line per utterance, `Speaker: text`).
2. Click **Process** to classify and score risks.
3. Copy the Markdown summary for email/Slack/Docs.
""")

# Input method
tab_json, tab_text = st.tabs(["Upload JSON", "Paste Plain Text"])

meeting: Dict = {"title": "Untitled Meeting", "attendees": [], "utterances": []}

with tab_json:
    st.subheader("Upload Transcript (JSON)")
    uploaded = st.file_uploader("Choose a JSON file", type=["json"])
    if uploaded:
        try:
            meeting = json.load(uploaded)
            st.success("Loaded transcript JSON.")
            if "title" in meeting:
                st.write("**Title:**", meeting["title"])
            if "attendees" in meeting and isinstance(meeting["attendees"], list):
                st.write("**Attendees:**", ", ".join(meeting["attendees"]))
        except Exception as e:
            st.error(f"Invalid JSON: {e}")

with tab_text:
    st.subheader("Paste Plain Text")
    default_text = """Priya: We will ship v1 without gift cards and add them in v1.1.
Carlos: I will handle promo code validation by next Friday if the API spec is ready.
Aisha: Carlos already has five high-priority tickets. We might slip if the spec is late."""
    txt = st.text_area("One line per utterance (format: Speaker: text)", height=200, value=default_text)
    title = st.text_input("Meeting title", value="Q4 Launch Sync")
    attendees = st.text_input("Attendees (comma-separated)", value="Priya,Carlos,Aisha")
    if st.button("Use pasted text"):
        meeting = {
            "title": title,
            "attendees": [a.strip() for a in attendees.split(",") if a.strip()],
            "utterances": []
        }
        for line in txt.splitlines():
            if ":" in line:
                speaker, text = line.split(":", 1)
                meeting["utterances"].append({"ts": "", "speaker": speaker.strip(), "text": text.strip()})
        st.success("Converted pasted text to transcript structure.")

st.divider()

if st.button("Process", type="primary"):
    if not meeting.get("utterances"):
        st.warning("No utterances found. Upload JSON or paste text first.")
    else:
        attendees = meeting.get("attendees", [])
        classified = batch_classify(meeting["utterances"], attendees=attendees)

        # (Optional) map of owner -> open high-priority tasks (you can wire this later)
        owner_loads = {a: 0 for a in attendees}
        # Example to showcase risk scoring:
        owner_loads.update({"Carlos": 5})

        scored = []
        for it in classified:
            if it.get("type") == "Risk":
                load = owner_loads.get((it.get("owner") or it.get("speaker") or ""), 0)
                scored.append(score_risk(it, owner_high_pri_open=load))
            else:
                scored.append(it)

        st.subheader("Classified Items")
        st.json(scored)

        st.subheader("Smart Summary (Markdown)")
        md = render_markdown(meeting, scored)
        st.code(md, language="markdown")

        st.download_button("Download summary.md", data=md, file_name="summary.md", mime="text/markdown")

st.caption("Personal project — focus on decision accountability & proactive risk prediction.")
