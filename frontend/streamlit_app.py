import streamlit as st
import json
import os
import sys
import pandas as pd
import sys, os

# Add project root (where app/ lives) to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.classifier import batch_classify
from app.risk import score_risk
from app.render import render_markdown


# 🔧 Fix imports so app/ modules can be found
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.classifier import batch_classify
from app.risk import score_risk
from app.render import render_markdown, render_pdf


st.set_page_config(page_title="Silent Meeting Observer", layout="wide")
st.title("📝 Silent Meeting Observer")

# === File upload ===
uploaded_file = st.file_uploader(
    "Upload transcript file",
    type=["json", "txt", "docx", "pdf"],
)

if uploaded_file:
    filename = uploaded_file.name

    # --- Parse input file ---
    if filename.endswith(".json"):
        data = json.load(uploaded_file)

    elif filename.endswith(".txt"):
        text = uploaded_file.read().decode("utf-8")
        data = {"utterances": text.splitlines()}

    elif filename.endswith(".docx"):
        from docx import Document
        doc = Document(uploaded_file)
        text = [p.text for p in doc.paragraphs if p.text.strip()]
        data = {"utterances": text}

    elif filename.endswith(".pdf"):
        from PyPDF2 import PdfReader
        reader = PdfReader(uploaded_file)
        text = [p.extract_text() for p in reader.pages if p.extract_text()]
        data = {"utterances": text}

    else:
        st.error("Unsupported file format")
        st.stop()

    st.success(f"Loaded file: {filename}")

    # --- Classification ---
    if "utterances" in data:
        results = batch_classify(data["utterances"])
        scored = [score_risk(r) for r in results]
    else:
        st.error("Transcript format invalid — no 'utterances' found.")
        st.stop()

    # --- Smart Summary (Table) ---
    st.subheader("Smart Summary")

    action_items = [
        {"Owner": r.get("owner", "TBD"), "Action Item": r.get("text", ""), "Timeline": r.get("timeline", "TBD")}
        for r in scored if r.get("type") == "Action Item"
    ]

    if action_items:
        df = pd.DataFrame(action_items)
        st.table(df)
    else:
        st.info("No action items found.")

    # --- Full Meeting Summary ---
    st.markdown("## Meeting Summary")
    st.markdown(render_markdown(data, scored))

    # --- One Download Button (PDF only) ---
    st.download_button(
        label="⬇️ Download Full Summary (PDF)",
        data=render_pdf(data, scored),
        file_name="meeting_summary.pdf",
        mime="application/pdf",
    )
