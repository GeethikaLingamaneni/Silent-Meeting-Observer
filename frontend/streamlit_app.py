import streamlit as st
import json
import os
import tempfile
from app.classifier import batch_classify
from app.risk import score_risk
from app.render import render_markdown, render_pdf
from docx import Document
from app.classifier import batch_classify
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app.classifier import batch_classify
from app.risk import score_risk
from app.render import render_markdown, render_pdf
from frontend.app.classifier import batch_classify
from frontend.app.risk import score_risk
from frontend.app.render import render_markdown, render_pdf




st.set_page_config(page_title="Silent Meeting Observer", layout="wide")

st.title("📝 Silent Meeting Observer")
st.write("Upload a transcript file (JSON, TXT, DOCX, PDF) to generate a smart meeting summary.")

uploaded_file = st.file_uploader(
    "Upload transcript file",
    type=["json", "txt", "docx", "pdf"]
)

if uploaded_file:
    file_ext = os.path.splitext(uploaded_file.name)[-1].lower()

    # === 1. Parse the uploaded file ===
    if file_ext == ".json":
        data = json.load(uploaded_file)

    elif file_ext == ".txt":
        text = uploaded_file.read().decode("utf-8")
        data = {"utterances": text.split("\n")}

    elif file_ext == ".docx":
        doc = Document(uploaded_file)
        text = "\n".join([p.text for p in doc.paragraphs if p.text.strip()])
        data = {"utterances": text.split("\n")}

    elif file_ext == ".pdf":
        import PyPDF2
        reader = PyPDF2.PdfReader(uploaded_file)
        text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
        data = {"utterances": text.split("\n")}

    else:
        st.error("Unsupported file type.")
        st.stop()

    # === 2. Classify transcript ===
    results = batch_classify(data["utterances"])

    # === 3. Score risks while keeping structure ===
    scored = {}
    for section, items in results.items():
        if section == "Risks":
            scored[section] = [score_risk(item) for item in items]
        else:
            scored[section] = items

    # === 4. Render to screen ===
    st.subheader("Smart Summary")
    st.markdown(render_markdown(data, scored))

    # === 5. Download full report as PDF ===
    pdf_buffer = render_pdf(data, scored)
    st.download_button(
        label="📥 Download Full Summary (PDF)",
        data=pdf_buffer,
        file_name="meeting_summary.pdf",
        mime="application/pdf"
    )
