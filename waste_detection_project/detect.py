```python
import argparse
import cv2
from ultralytics import YOLO
from waste_info import get_parent


PARENT_COLOR_BGR = {
    "Hazardous": (0, 0, 255),
    "Biodegradable": (0, 180, 0),
    "Non-biodegradable / Recyclable": (255, 140, 0),
    "Unknown": (128, 128, 128),
}


def load_model(weights_path):
    return YOLO(str(weights_path))


def detect_waste(model, image_bgr, conf=0.25, iou=0.5, imgsz=640):
    result = model.predict(
        source=image_bgr,
        conf=conf,
        iou=iou,
        imgsz=imgsz,
        verbose=False
    )[0]

    detections = []

    if result.boxes is None:
        return detections

    for box in result.boxes:
        class_id = int(box.cls[0])
        class_name = result.names[class_id]

        x1, y1, x2, y2 = [
            int(v) for v in box.xyxy[0].tolist()
        ]

        confidence = float(box.conf[0])

        detections.append({
            "class_name": class_name,
            "parent": get_parent(class_name),
            "confidence": confidence,
            "box": (x1, y1, x2, y2)
        })

    return detections


def draw_detections(image_bgr, detections):
    out = image_bgr.copy()

    scale = max(out.shape[:2]) / 1000.0
    thickness = max(2, int(3 * scale))
    font_scale = max(0.5, 0.7 * scale)

    for detection in detections:
        x1, y1, x2, y2 = detection["box"]
        color = PARENT_COLOR_BGR.get(
            detection["parent"],
            PARENT_COLOR_BGR["Unknown"]
        )

        cv2.rectangle(
            out, (x1, y1), (x2, y2), color, thickness
        )

        label = (
            f'{detection["class_name"]} '
            f'{detection["confidence"]:.2f}'
        )

        (tw, th), baseline = cv2.getTextSize(
            label,
            cv2.FONT_HERSHEY_SIMPLEX,
            font_scale,
            thickness
        )

        top = max(0, y1 - th - baseline)

        cv2.rectangle(
            out,
            (x1, top),
            (x1 + tw, top + th + baseline),
            color,
            -1
        )

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


def count_by_class(detections):
    counts = {}

    for detection in detections:
        name = detection["class_name"]
        counts[name] = counts.get(name, 0) + 1

    return counts


def count_by_parent(detections):
    counts = {}

    for detection in detections:
        parent = detection["parent"]
        counts[parent] = counts.get(parent, 0) + 1

    return counts


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Detect waste objects in one image using YOLO11n"
    )

    parser.add_argument("--weights", default="best.pt")
    parser.add_argument("--image", required=True)
    parser.add_argument("--out", default="result.jpg")
    parser.add_argument("--conf", type=float, default=0.25)
    parser.add_argument("--iou", type=float, default=0.5)
    parser.add_argument("--imgsz", type=int, default=640)

    args = parser.parse_args()

    model = load_model(args.weights)
    image = cv2.imread(args.image)

    if image is None:
        raise SystemExit(f"Could not read image: {args.image}")

    found = detect_waste(
        model,
        image,
        conf=args.conf,
        iou=args.iou,
        imgsz=args.imgsz
    )

    annotated_image = draw_detections(image, found)
    cv2.imwrite(args.out, annotated_image)

    if not found:
        print("No waste objects detected.")
    else:
        print(f"Detected {len(found)} object(s):")

        for detection in found:
            print(
                f'  {detection["class_name"]:22s} '
                f'{detection["confidence"]:.2f} '
                f'[{detection["parent"]}]'
            )

        print("Counts per class :", count_by_class(found))
        print("Counts per parent:", count_by_parent(found))

    print("Saved annotated image to", args.out)
```
