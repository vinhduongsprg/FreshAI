# FreshAI — AI Handoff / Project Context

## Project
KAVIN FreshAI is a Vietnamese high-school competition project for smart refrigerator food management. The current ML focus is food object detection.

## Current technical direction
- OpenCV: video/image handling, frame extraction, preprocessing, later camera-frame handling.
- YOLO: food object detection.
- OCR: postponed until food detection is reliable; later for expiry/manufacturing dates.
- Human-in-the-loop: later for low-confidence/unknown detections.
- Inventory tracking: later, after reliable detection.

The proposal currently discusses YOLOv8 and an Image Difference step that can trigger object detection when the refrigerator view changes.

## Current pipeline
Videos/camera → OpenCV → frame extraction → manual review → bounding-box annotation → YOLO dataset → train/validate/test → unseen-video testing → failure analysis → dataset improvement → retraining → OpenCV integration → later OCR/inventory/human-in-the-loop.

## Data
The team already has food-related video footage. Frames are extracted with OpenCV rather than saving every frame blindly. Blurry and near-duplicate frames can be filtered.

**Critical:** split by video/session, not randomly by adjacent frame, to avoid train/validation/test leakage.

The proposal describes a target of 2,500+ images with varied lighting, angles, occlusion, and refrigerator conditions. Treat this as a target, not a magic number; dataset quality and coverage matter more.

## Current class list (v1)
| ID | Class |
|---:|---|
| 0 | canned food |
| 1 | cooked chicken |
| 2 | dumpling |
| 3 | egg |
| 4 | fish |
| 5 | fruits |
| 6 | lemon |
| 7 | meat |
| 8 | milk |
| 9 | pate |
| 10 | rice noodle |
| 11 | tomato |
| 12 | vegetable |
| 13 | yogurt |

This list is provisional until a pilot annotation is completed. Do not silently add/rename classes.

## Dataset structure
```text
FreshAI/
├── videos/
├── dataset/
│   ├── raw_frames/
│   ├── reviewed/
│   │   ├── keep/
│   │   └── discard/
│   └── yolo/
│       ├── images/{train,val,test}
│       ├── labels/{train,val,test}
│       └── data.yaml
└── tools/
```

## YOLO labels
Each image has a matching `.txt` file. Each object is one row:
`class_id x_center y_center width height`
with coordinates normalized to 0–1.

## Proposed data.yaml
```yaml
path: .
train: images/train
val: images/val
test: images/test
names:
  0: canned food
  1: cooked chicken
  2: dumpling
  3: egg
  4: fish
  5: fruits
  6: lemon
  7: meat
  8: milk
  9: pate
  10: rice noodle
  11: tomato
  12: vegetable
  13: yogurt
```

## Training philosophy
Use a pretrained YOLO model/transfer learning. First priority is a clean end-to-end baseline, not hyperparameter optimization.

Evaluate:
- precision
- recall
- mAP
- per-class performance
- qualitative performance on unseen refrigerator video
- failure cases

Iterate: collect → extract → review → annotate → train → test → analyze failures → collect targeted data → retrain.

## Future stages
1. Reliable food detector.
2. OCR on relevant package regions for expiry/manufacturing dates.
3. Inventory/event tracking.
4. Human-in-the-loop confirmation and future active-learning data.


## Source
The broader system design comes from the uploaded competition proposal `[Draft] Samsung Solve for tomorrow .docx`. It currently describes YOLOv8, OpenCV/computer vision, Image Difference, OCR, human-in-the-loop, augmentation, transfer learning, Roboflow/LabelImg, 2,500+ images, and mAP evaluation.
