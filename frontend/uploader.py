import streamlit as st  # type: ignore
import requests  # type: ignore
from api import BACKEND_URL
from video_player import render_video_player  # <- Assuming you split this out


def render_upload_form():
    uploaded = st.file_uploader(
        "Upload a video",
        type=["mp4", "mov", "avi", "mkv", "webm"],
        key="upload"
    )

    if uploaded and not st.session_state.get("uploaded_success"):
        with st.spinner("Uploading…"):
            try:
                r = requests.post(
                    f"{BACKEND_URL}/upload",
                    files={"file": (uploaded.name, uploaded.getbuffer())},
                    timeout=(10, 600)
                )
                if r.ok:
                    st.session_state["uploaded_success"] = True
                    st.session_state["uploaded_filename"] = uploaded.name
                    st.success("Video uploaded successfully")
                else:
                    st.error(r.json().get("detail", "Upload failed"))
            except Exception as e:
                st.error(f"Upload failed: {e}")

    if (st.session_state.get("uploaded_success")
            and st.session_state.get("uploaded_filename")):
        st.markdown("### Video Preview")
        # Example: assume backend always starts playing from 0
        render_video_player(st.session_state["uploaded_filename"], elapsed=0)
