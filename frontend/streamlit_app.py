import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import json
from io import StringIO
from docx import Document
import fitz  # PyMuPDF for PDFs

from app.classifier import batch_classify
from app.risk import score_risk
from app.render import render_markdown

st.title("🤖 Silent Meeting Observer")

uploaded = st.file_uploader("Upload transcript file", type=["json", "txt", "docx", "pdf"])

if uploaded:
    # -------------------------------
    # Handle JSON transcripts
    # -------------------------------
    if uploaded.name.endswith(".json"):
        data = json.load(uploaded)

    # -------------------------------
    # Handle TXT transcripts
    # Format: "Speaker: message"
    # -------------------------------
    elif uploaded.name.endswith(".txt"):
        stringio = StringIO(uploaded.getvalue().decode("utf-8"))
        lines = stringio.readlines()
        utterances = []
        for line in lines:
            if ":" in line:
                speaker, text = line.split(":", 1)
                utterances.append({"speaker": speaker.strip(), "text": text.strip()})
        data = {
            "title": "Uploaded TXT Meeting",
            "attendees": list({u["speaker"] for u in utterances}),
            "utterances": utterances,
        }

    # -------------------------------
    # Handle DOCX transcripts
    # Format: "Speaker: message"
    # -------------------------------
    elif uploaded.name.endswith(".docx"):
        doc = Document(uploaded)
        utterances = []
        for para in doc.paragraphs:
            if ":" in para.text:
                speaker, text = para.text.split(":", 1)
                utterances.append({"speaker": speaker.strip(), "text": text.strip()})
        data = {
            "title": "Uploaded Word Meeting",
            "attendees": list({u["speaker"] for u in utterances}),
            "utterances": utterances,
        }

    # -------------------------------
    # Handle PDF transcripts
    # Format: "Speaker: message"
    # -------------------------------
    elif uploaded.name.endswith(".pdf"):
        pdf = fitz.open(stream=uploaded.read(), filetype="pdf")
        utterances = []
        for page in pdf:
            text = page.get_text().splitlines()
            for line in text:
                if ":" in line:
                    speaker, msg = line.split(":", 1)
                    utterances.append({"speaker": speaker.strip(), "text": msg.strip()})
        data = {
            "title": "Uploaded PDF Meeting",
            "attendees": list({u["speaker"] for u in utterances}),
            "utterances": utterances,
        }

    # -------------------------------
    # Process transcript
    # -------------------------------
    st.subheader("Smart Summary")
    results = batch_classify(data["utterances"])
    scored = [score_risk(r) for r in results]
    st.markdown(render_markdown(data, scored))
