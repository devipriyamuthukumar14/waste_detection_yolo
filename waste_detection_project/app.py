"""
app.py: Streamlit web app for Real-World Waste Detection.
Run with:  streamlit run app.py
"""
from pathlib import Path

import cv2
import numpy as np
import pandas as pd
import streamlit as st
from PIL import Image, ImageOps

from detect import load_model, detect_waste, draw_detections, count_by_class, count_by_parent
from waste_info import (ALL_PARENTS, HAZARDOUS, HAZARD_DISCLAIMER, get_guidance, get_parent)

st.set_page_config(page_title="Waste Detection", page_icon="♻️", layout="wide")
st.title("♻️ Real-World Waste Detection and Classification")
st.write("Upload a photo of messy waste. The model finds each object, names it, and "
         "shows general disposal guidance.")

# Folder that contains this file (works on Streamlit Cloud and on your own computer)
APP_DIR = Path(__file__).parent

# ---------------- Sidebar: settings ----------------
with st.sidebar:
    st.header("Settings")
    weights_path = st.text_input("Model file", value=str(APP_DIR / "best.pt"))
    conf = st.slider("Confidence threshold", min_value=0.05, max_value=0.95, value=0.25, step=0.05,
                     help="Boxes with a score below this value are hidden. "
                          "Lower = finds more (but more false alarms).")
    st.markdown("**Box colours**  \n🟥 Hazardous  \n🟩 Biodegradable  \n🟦 Non-biodegradable / Recyclable")


@st.cache_resource
def get_model(path):
    """Load the YOLO model once and reuse it."""
    return load_model(path)


if not Path(weights_path).exists():
    st.error(f"Model file '{weights_path}' not found. Put your trained best.pt in this folder.")
    st.stop()
model = get_model(weights_path)

# ---------------- Image upload ----------------
uploaded = st.file_uploader("Upload a waste image (to try another image, simply upload a new one)",
                            type=["jpg", "jpeg", "png"])
if uploaded is None:
    st.info("👆 Upload an image to begin.")
    st.stop()

pil_image = ImageOps.exif_transpose(Image.open(uploaded)).convert("RGB")   # fix phone-photo rotation
image_bgr = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)           # OpenCV uses BGR
