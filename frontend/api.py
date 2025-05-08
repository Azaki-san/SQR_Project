import requests # type: ignore
import time
import threading
import streamlit as st # type: ignore
import uuid

BACKEND_URL = "http://192.168.3.29:8000"
VIEWER_ID = str(uuid.uuid4())  # Or use a known user ID from your app

def get_video_status():
    try:
        res = requests.get(f"{BACKEND_URL}/status", timeout=5)
        if res.ok and res.json().get("status") == "playing":
            data = res.json()
            return round(data.get("elapsed", 0)), data.get("filename")
    except Exception as e:
        st.error(f"Failed to fetch video status: {e}")
    return 0, None

def start_ping_thread():
    def ping():
        while True:
            try:
                requests.post(f"{BACKEND_URL}/ping", json={"viewer_id": VIEWER_ID})
            except Exception as e:
                print("Ping failed:", e)
            time.sleep(15)
    threading.Thread(target=ping, daemon=True).start()

def get_weather_status():
    try:
        r =requests.get(f"{BACKEND_URL}/weather", timeout=5)
        return r.json()
    except Exception as e:
        return {"error": str(e)}