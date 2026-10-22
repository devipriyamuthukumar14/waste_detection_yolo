"""
detect.py

Loads the trained YOLO11n model, detects waste objects in an image,
draws bounding boxes, and counts detected objects.

Can be imported by app.py or run from the command line:

    python detect.py --weights best.pt --image photo.jpg --out result.jpg
"""

import argparse

import cv2
from ultralytics import YOLO

from waste_info import get_parent


# ---------------------------------------------------------
# Parent category colors
# ---------------------------------------------------------
# OpenCV uses BGR format.
PARENT_COLOR_BGR = {
    "Hazardous": (0, 0, 255),                     # Red
    "Biodegradable": (0, 180, 0),                # Green
    "Non-biodegradable / Recyclable": (255, 140, 0),  # Blue/Orange
    "Unknown": (128, 128, 128),                  # Gray
}


# ---------------------------------------------------------
# Load YOLO model
# ---------------------------------------------------------
def load_model(weights_path):
    """
    Load the trained YOLO model from a .pt file.
    """
    return YOLO(str(weights_path))


# ---------------------------------------------------------
# Detect waste objects
# ---------------------------------------------------------
def detect_waste(model, image_bgr, conf=0.25, iou=0.5, imgsz=640):
    """
    Run YOLO detection on one image.

    Parameters:
        model      : Loaded YOLO model
        image_bgr  : OpenCV BGR image
        conf       : Minimum confidence threshold
        iou        : IoU threshold for non-maximum suppression
        imgsz      : YOLO input image size

    Returns:
        A list of dictionaries containing:
        - class_name
        - parent
        - confidence
        - box
    """

    result = model.predict(
        source=image_bgr,
        conf=conf,
        iou=iou,
        imgsz=imgsz,
        verbose=False
    )[0]

    detections = []

    # If no objects are detected
    if result.boxes is None:
        return detections

    for box in result.boxes:

        # Class ID predicted by YOLO
        class_id = int(box.cls[0])

        # Class name from the trained model
        class_name = result.names[class_id]

        # Bounding box coordinates
        x1, y1, x2, y2 = [
            int(v) for v in box.xyxy[0].tolist()
        ]

        # Confidence score
        confidence = float(box.conf[0])

        # Parent category
        parent = get_parent(class_name)

        detections.append(
            {
                "class_name": class_name,
                "parent": parent,
                "confidence": confidence,
                "box": (x1, y1, x2, y2),
            }
        )

    return detections


# ---------------------------------------------------------
# Draw bounding boxes
# ---------------------------------------------------------
def draw_detections(image_bgr, detections):
    """
    Return a copy of the image with bounding boxes and labels.

    Each label contains:
        class name + confidence

    The box color represents the parent category.
    """

    out = image_bgr.copy()

    # Scale text and line thickness according to image size
    scale = max(out.shape[:2]) / 1000.0

    thickness = max(2, int(3 * scale))
    font_scale = max(0.5, 0.7 * scale)

    for detection in detections:

        x1, y1, x2, y2 = detection["box"]

        parent = detection["parent"]

        color = PARENT_COLOR_BGR.get(
            parent,
            PARENT_COLOR_BGR["Unknown"]
        )

        # Draw bounding box
        cv2.rectangle(
            out,
            (x1, y1),
            (x2, y2),
            color,
            thickness
        )

        # Label
        label = (
            f'{detection["class_name"]} '
            f'{detection["confidence"]:.2f}'
        )

        # Calculate label size
        (tw, th), baseline = cv2.getTextSize(
            label,
            cv2.FONT_HERSHEY_SIMPLEX,
            font_scale,
            thickness
        )

        # Position label above the box
        top = max(0, y1 - th - baseline)

        # Label background
        cv2.rectangle(
            out,
            (x1, top),
            (x1 + tw, top + th + baseline),
            color,
            -1
        )

        # Label text
        cv2.putText(
            out,
            label,
            (x1, top + th),
            cv2.FONT_HERSHEY_SIMPLEX,
            font_scale,
            (255, 255, 255),
            max(1, thickness // 2)
        )

    return out


# ---------------------------------------------------------
# Count objects by individual class
# ---------------------------------------------------------
def count_by_class(detections):
    """
    Return the number of detected objects for each class.

    Example:
        {
            "Plastic_bottles": 3,
            "Cans": 2
        }
    """

    counts = {}

    for detection in detections:

        class_name = detection["class_name"]

        counts[class_name] = (
            counts.get(class_name, 0) + 1
        )

    return counts


# ---------------------------------------------------------
# Count objects by parent category
# ---------------------------------------------------------
def count_by_parent(detections):
    """
    Return the number of detected objects in each parent category.

    Example:
        {
            "Hazardous": 1,
            "Biodegradable": 2,
            "Non-biodegradable / Recyclable": 4
        }
    """

    counts = {}

    for detection in detections:

        parent = detection["parent"]

        counts[parent] = (
            counts.get(parent, 0) + 1
        )

    return counts


# ---------------------------------------------------------
# Command-line usage
# ---------------------------------------------------------
if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Detect waste objects in one image using YOLO11n"
    )

    parser.add_argument(
        "--weights",
        default="best.pt",
        help="Path to trained YOLO weights"
    )

    parser.add_argument(
        "--image",
        required=True,
        help="Path to input image"
    )

    parser.add_argument(
        "--out",
        default="result.jpg",
        help="Path to save annotated output image"
    )

    parser.add_argument(
        "--conf",
        type=float,
        default=0.25,
        help="Confidence threshold"
    )

    parser.add_argument(
        "--iou",
        type=float,
        default=0.5,
        help="IoU threshold"
    )

    parser.add_argument(
        "--imgsz",
        type=int,
        default=640,
        help="YOLO image size"
    )

    args = parser.parse_args()

    # Load model
    model = load_model(args.weights)

    # Read image
    image = cv2.imread(args.image)

    if image is None:
        raise SystemExit(
            f"Could not read image: {args.image}"
        )

    # Run detection
    found = detect_waste(
        model,
        image,
        conf=args.conf,
        iou=args.iou,
        imgsz=args.imgsz
    )

    # Draw detections
    annotated_image = draw_detections(
        image,
        found
    )

    # Save result
    cv2.imwrite(
        args.out,
        annotated_image
    )

    # Print results
    if not found:

        print("No waste objects detected.")

    else:

        print(
            f"Detected {len(found)} object(s):"
        )

        for detection in found:

            print(
                f'  {detection["class_name"]:22s} '
                f'{detection["confidence"]:.2f} '
                f'[{detection["parent"]}]'
            )

        print(
            "Counts per class :",
            count_by_class(found)
        )

        print(
            "Counts per parent:",
            count_by_parent(found)
        )

    print(
        "Saved annotated image to",
        args.out
    )
