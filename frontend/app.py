
import streamlit as st  # type: ignore
from api import get_video_status, start_ping_thread
from video_player import render_video_player
from uploader import render_upload_form
from weather_ui import render_weather_info

st.set_page_config(page_title="Synchronized Video Watcher", layout="centered")

render_weather_info()

st.title("🎬 Synchronized Video Watcher")


# ────────────────────────────────
# Initial status check
# ────────────────────────────────
elapsed, video_filename = get_video_status()

# If a video is available
if video_filename:
    # Only re-render the video if it's a new one
    if st.session_state.get("last_video") != video_filename:
        st.session_state["last_video"] = video_filename
        st.success("Video is playing. Syncing to current position…")
        #start_ping_thread()

    # Always render video player (but avoid syncTime spam in JS)
    render_video_player(video_filename, elapsed)

# If no video is uploaded yet
else:
    st.warning("No video currently playing. Upload one to start a session.")
    render_upload_form()
