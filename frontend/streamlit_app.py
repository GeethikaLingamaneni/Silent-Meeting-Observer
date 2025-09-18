# frontend/streamlit_app.py
import streamlit as st
import json
import os
import sys
import pandas as pd
import tempfile

# Ensure Python can find app/ package
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.classifier import batch_classify
from app.risk import score_risk
from app.render import render_markdown, render_pdf

# Extra: speech + mic
import whisper
from streamlit_webrtc import webrtc_streamer, WebRtcMode
import av

# Load Whisper model once
model = whisper.load_model("base")

st.set_page_config(page_title="Silent Meeting Observer", layout="wide")
st.title("📝 Silent Meeting Observer")

mode = st.radio("Choose Mode:", ["Upload Transcript", "Live Mic Capture"])

# ---------------- File Upload Mode ----------------
if mode == "Upload Transcript":
    uploaded_file = st.file_uploader("Upload transcript file", type=["json", "txt", "docx", "pdf"])

    if uploaded_file:
        filename = uploaded_file.name

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

        results = batch_classify(data["utterances"])
        scored = [score_risk(r) for r in results]

        # Smart Summary table (simplified)
        st.subheader("Smart Summary")
        action_items = [
            {
                "Owner": r.get("owner", "TBD"),
                "Task": r.get("text", ""),
                "Timeline": r.get("timeline", "TBD")
            }
            for r in scored if r.get("type") == "Action Item"
        ]

        if action_items:
            st.table(pd.DataFrame(action_items))
        else:
            st.info("No action items found.")

        st.markdown(render_markdown(data, scored))

        st.download_button(
            label="📥 Download Full Summary (PDF)",
            data=render_pdf(data, scored),
            file_name="meeting_summary.pdf",
            mime="application/pdf",
        )

# ---------------- Live Mic Capture Mode ----------------
elif mode == "Live Mic Capture":
    st.info("🎤 Speak or let your meeting play through your microphone. Transcription happens live.")

    transcript_holder = st.empty()
    live_transcript = []

    def audio_frame_callback(frame: av.AudioFrame):
        pcm = frame.to_ndarray().flatten().astype("float32")
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmpfile:
            tmpfile.write(pcm.tobytes())
            tmpfile.flush()
            try:
                result = model.transcribe(tmpfile.name)
                if result and "text" in result and result["text"].strip():
                    live_transcript.append(result["text"])
                    transcript_holder.text("\n".join(live_transcript[-10:]))
            except Exception:
                pass
        return frame

    webrtc_streamer(
        key="meeting-listener",
        mode=WebRtcMode.RECVONLY,
        rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
        media_stream_constraints={"audio": True, "video": False},
        audio_frame_callback=audio_frame_callback,
    )

    if st.button("Generate MoM from Transcript"):
        if not live_transcript:
            st.warning("No transcript captured yet.")
        else:
            data = {"utterances": live_transcript}
            results = batch_classify(data["utterances"])
            scored = [score_risk(r) for r in results]

            st.markdown(render_markdown(data, scored))
            st.download_button(
                label="📥 Download Full Summary (PDF)",
                data=render_pdf(data, scored),
                file_name="meeting_summary.pdf",
                mime="application/pdf",
            )
