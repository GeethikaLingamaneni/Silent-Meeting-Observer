import streamlit as st
import pandas as pd
import os
from app.classifier import batch_classify
from app.risk import score_risk
from app.render import render_markdown

st.set_page_config(page_title="Silent Meeting Observer", layout="wide")

st.title("📝 Silent Meeting Observer")

mode = st.radio("Choose Mode:", ["Upload Transcript", "Live Mic Capture"], index=0)

uploaded_file = None
if mode == "Upload Transcript":
    uploaded_file = st.file_uploader(
        "Upload transcript file", 
        type=["docx", "pdf", "txt"]
    )

if uploaded_file:
    text = ""

    # === Handle DOCX ===
    if uploaded_file.name.endswith(".docx"):
        import docx
        doc = docx.Document(uploaded_file)
        text = "\n".join([p.text for p in doc.paragraphs if p.text.strip()])

    # === Handle PDF (lazy import) ===
    elif uploaded_file.name.endswith(".pdf"):
        pdfplumber = __import__("pdfplumber")
        with pdfplumber.open(uploaded_file) as pdf:
            text = "\n".join([page.extract_text() or "" for page in pdf.pages])

    # === Handle TXT ===
    elif uploaded_file.name.endswith(".txt"):
        text = uploaded_file.read().decode("utf-8")

    if text.strip():
        st.success(f"Loaded file: {uploaded_file.name}")

        # Fake structure for now
        data = {"utterances": text.split("\n")}
        results = batch_classify(data["utterances"])
        scored = [score_risk(r) for r in results]

        st.subheader("Smart Summary")
        st.markdown(render_markdown(data, scored))
    else:
        st.error("No readable content found in the uploaded file.")

elif mode == "Live Mic Capture":
    st.warning("🎤 Live mic capture disabled in this build for faster startup.")
