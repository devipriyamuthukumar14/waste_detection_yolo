"""
app.py: Streamlit web app for Real-World Waste Detection.

Run with:
    streamlit run app.py
"""

from pathlib import Path

import cv2
import numpy as np
import pandas as pd
import streamlit as st
from PIL import Image, ImageOps

from detect import (
    load_model,
    detect_waste,
    draw_detections,
    count_by_class,
    count_by_parent,
)

from waste_info import (
    ALL_PARENTS,
    HAZARDOUS,
    HAZARD_DISCLAIMER,
    get_guidance,
    get_parent,
)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Waste Detection",
    page_icon="♻️",
    layout="wide",
)

st.title("♻️ Real-World Waste Detection and Classification")

st.write(
    "Upload a photo of messy waste. The model detects individual objects, "
    "classifies them, and shows their waste category and general disposal guidance."
)

APP_DIR = Path(__file__).parent


# ============================================================
# SIDEBAR SETTINGS
# ============================================================

with st.sidebar:
    st.header("⚙️ Settings")

    weights_path = st.text_input(
        "Model file",
        value=str(APP_DIR / "best.pt"),
    )

    conf = st.slider(
        "Confidence threshold",
        min_value=0.05,
        max_value=0.95,
        value=0.25,
        step=0.05,
        help=(
            "Detections below this confidence are hidden. "
            "Lower values may find more objects but can produce more false detections."
        ),
    )

    st.markdown("---")

    st.markdown(
        """
        **Waste categories**

        🟥 Hazardous  
        🟩 Biodegradable  
        🟦 Non-biodegradable / Recyclable
        """
    )


# ============================================================
# LOAD MODEL
# ============================================================

@st.cache_resource
def get_model(path):
    """Load the YOLO model once and reuse it."""
    return load_model(path)


if not Path(weights_path).exists():
    st.error(
        f"Model file not found:\n\n`{weights_path}`\n\n"
        "Place your trained `best.pt` file in the project folder "
        "or enter the correct model path in the sidebar."
    )
    st.stop()


try:
    model = get_model(weights_path)

except Exception as e:
    st.error(f"Could not load the YOLO model: {e}")
    st.stop()


# ============================================================
# IMAGE UPLOAD
# ============================================================

uploaded = st.file_uploader(
    "Upload a waste image",
    type=["jpg", "jpeg", "png"],
    help="Upload an image containing one or more waste objects.",
)


if uploaded is None:
    st.info("👆 Upload an image to begin.")
    st.stop()


# ============================================================
# READ IMAGE
# ============================================================

try:
    pil_image = ImageOps.exif_transpose(
        Image.open(uploaded)
    ).convert("RGB")

    image_bgr = cv2.cvtColor(
        np.array(pil_image),
        cv2.COLOR_RGB2BGR,
    )

except Exception as e:
    st.error(f"Could not read the uploaded image: {e}")
    st.stop()


# ============================================================
# RUN DETECTION
# ============================================================

with st.spinner("🔍 Detecting waste objects..."):

    try:
        detections = detect_waste(
            model,
            image_bgr,
            conf=conf,
        )

    except Exception as e:
        st.error(f"Detection failed: {e}")
        st.stop()


# ============================================================
# DISPLAY DETECTION IMAGE
# ============================================================

try:
    annotated_bgr = draw_detections(
        image_bgr.copy(),
        detections,
    )

    annotated_rgb = cv2.cvtColor(
        annotated_bgr,
        cv2.COLOR_BGR2RGB,
    )

except Exception as e:
    st.error(f"Could not draw detection boxes: {e}")
    st.stop()


st.subheader("🔎 Detection Result")

st.image(
    annotated_rgb,
    caption="Detected waste objects",
    use_container_width=True,
)


# ============================================================
# NO DETECTIONS
# ============================================================

if not detections:
    st.warning(
        "No waste objects were detected above the selected confidence threshold."
    )

    st.info(
        "Try lowering the confidence threshold in the sidebar "
        "or upload a clearer image."
    )

    st.stop()


# ============================================================
# COUNTS
# ============================================================

class_counts = count_by_class(detections)
parent_counts = count_by_parent(detections)


# ============================================================
# SUMMARY METRICS
# ============================================================

st.subheader("📊 Waste Summary")

total_objects = len(detections)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Objects",
        total_objects,
    )

with col2:
    st.metric(
        "Hazardous",
        parent_counts.get("Hazardous", 0),
    )

with col3:
    st.metric(
        "Biodegradable",
        parent_counts.get("Biodegradable", 0),
    )

with col4:
    st.metric(
        "Non-biodegradable",
        parent_counts.get(
            "Non-biodegradable / Recyclable",
            0,
        ),
    )


# ============================================================
# CLASS-WISE COUNTS
# ============================================================

st.subheader("🏷️ Class-wise Object Counts")

class_rows = []

for class_name, count in class_counts.items():

    parent = get_parent(class_name)

    class_rows.append(
        {
            "Waste Class": class_name,
            "Count": count,
            "Category": parent,
        }
    )

class_df = pd.DataFrame(class_rows)

st.dataframe(
    class_df,
    use_container_width=True,
    hide_index=True,
)


# ============================================================
# DETECTION DETAILS
# ============================================================

st.subheader("🔍 Detection Details")

detail_rows = []

for detection in detections:

    class_name = detection["class_name"]
    confidence = detection["confidence"]

    parent = get_parent(class_name)

    detail_rows.append(
        {
            "Detected Object": class_name,
            "Confidence": f"{float(confidence):.1%}",
            "Category": parent,
        }
    )


details_df = pd.DataFrame(detail_rows)

st.dataframe(
    details_df,
    use_container_width=True,
    hide_index=True,
)


# ============================================================
# CATEGORY BREAKDOWN
# ============================================================

st.subheader("📂 Category Breakdown")

category_rows = []

for category in ALL_PARENTS:

    category_rows.append(
        {
            "Category": category,
            "Number of Objects": parent_counts.get(
                category,
                0,
            ),
        }
    )

category_df = pd.DataFrame(category_rows)

st.dataframe(
    category_df,
    use_container_width=True,
    hide_index=True,
)


# ============================================================
# DISPOSAL GUIDANCE
# ============================================================

st.subheader("♻️ General Disposal Guidance")

unique_classes = list(class_counts.keys())

for class_name in unique_classes:

    parent = get_parent(class_name)

    guidance = get_guidance(class_name)

    with st.expander(
        f"{class_name} — {parent}"
    ):

        st.write(guidance)

        # Show the hazardous disclaimer only for
        # genuinely hazardous parent categories.
        if parent == HAZARDOUS:
            st.warning(HAZARD_DISCLAIMER)


# ============================================================
# PROJECT DISCLAIMER
# ============================================================

st.markdown("---")
