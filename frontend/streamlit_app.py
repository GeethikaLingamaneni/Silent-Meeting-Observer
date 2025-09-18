import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode, AudioProcessorBase
import av
import tempfile
import os
from docx import Document
import pdfplumber
import json

from app.classifier import batch_classify
from app.risk import score_risk
from app.render import render_markdown, render_pdf


st.set_page_config(page_title="Silent Meeting Observer", layout="wide")
st.title("📝 Silent Meeting Observer")

mode = st.radio("Choose Mode:", ["Upload Transcript", "Live Mic Capture"])


# ==============================
# File Upload Mode
# ==============================
if mode == "Upload Transcript":
    uploaded = st.file_uploader("Upload transcript file", type=["docx", "pdf", "txt", "json"])
    if uploaded:
        st.success(f"Loaded file: {uploaded.name}")

        text = ""
        if uploaded.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            doc = Document(uploaded)
            text = "\n".join([p.text for p in doc.paragraphs])
        elif uploaded.type == "application/pdf":
            with tempfile.NamedTemporaryFile(delete=False) as tmp:
                tmp.write(uploaded.read())
                tmp_path = tmp.name
            with pdfplumber.open(tmp_path) as pdf:
                text = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])
            os.remove(tmp_path)
        elif uploaded.type == "text/plain":
            text = uploaded.read().decode("utf-8")
        elif uploaded.type == "application/json":
            data = json.load(uploaded)
            text = " ".join(data.get("utterances", []))

        if text.strip():
            # Process transcript
            results = batch_classify(text.split("\n"))
            scored = [score_risk(r) for r in results]

            # Show MOM
            st.subheader("Smart Summary")
            st.markdown(render_markdown({"utterances": text.split("\n")}, scored))

            # Download PDF
            pdf_bytes = render_pdf({"utterances": text.split("\n")}, scored)
            st.download_button("⬇️ Download Meeting Summary (PDF)", pdf_bytes, file_name="meeting_summary.pdf")


# ==============================
# Live Mic Capture Mode
# ==============================
elif mode == "Live Mic Capture":
    st.info("🎤 Speak or let your meeting play through your microphone. Transcription happens live.")

    class AudioProcessor(AudioProcessorBase):
        def __init__(self):
            self.chunks = []

        def recv_audio(self, frame: av.AudioFrame) -> av.AudioFrame:
            # Here you could add speech-to-text integration
            # For now, we just collect raw audio
            self.chunks.append(frame.to_ndarray())
            return frame

    webrtc_streamer(
        key="meeting-listener",
        mode=WebRtcMode.RECVONLY,
        rtc_configuration={
            "iceServers": [
                {"urls": ["stun:stun.l.google.com:19302"]},
                {
                    "urls": ["turn:openrelay.metered.ca:80", "turn:openrelay.metered.ca:443"],
                    "username": "openrelayproject",
                    "credential": "openrelayproject",
                },
            ]
        },
        media_stream_constraints={"audio": True, "video": False},
        audio_processor_factory=AudioProcessor,
    )

    st.warning("⚠️ Note: Live transcription requires connecting to STUN/TURN servers. Upload mode is more stable for Streamlit Cloud.")
