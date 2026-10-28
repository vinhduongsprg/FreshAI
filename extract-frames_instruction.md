# FreshAI — Dataset Preparation Pipeline

This is the first stage of the FreshAI computer-vision pipeline.

## Goal

Convert refrigerator/food video footage into a manageable collection of candidate images for manual review and YOLO annotation.

```text
Video
  ↓
OpenCV
  ├── frame sampling
  ├── blurry-frame rejection
  └── near-duplicate rejection
  ↓
Candidate frames
  ↓
Manual review
  ↓
YOLO annotation
  ↓
Train / validation / test
```

## Recommended project structure

```text
FreshAI/
├── videos/
│   ├── fridge_01.mp4
│   ├── fridge_02.mp4
│   └── ...
│
├── dataset/
│   ├── raw_frames/
│   │   ├── fridge_01/
│   │   ├── fridge_02/
│   │   └── ...
│   ├── reviewed/
│   └── yolo/
│       ├── images/
│       │   ├── train/
│       │   ├── val/
│       │   └── test/
│       └── labels/
│           ├── train/
│           ├── val/
│           └── test/
│
└── extract_frames.py
```

## Installation

```bash
pip install opencv-python
```

## Run

Put your videos inside `videos/`, then:

```bash
python extract_frames.py --input videos --output dataset/raw_frames --fps 2
```

For a more conservative dataset:

```bash
python extract_frames.py --input videos --output dataset/raw_frames --fps 1
```

The script currently:

1. Reads the video with OpenCV.
2. Samples frames at approximately the requested FPS.
3. Rejects very blurry frames.
4. Rejects recent near-duplicate frames.
5. Saves useful candidate frames as JPG files.
6. Keeps frames separated by source video.

## Important: do not train immediately

The extracted frames are **candidate images**, not your final dataset.

After extraction, manually inspect them and remove:

- frames where food is heavily motion-blurred
- almost identical frames
- frames where the food is too small to identify
- accidental frames containing no useful food
- frames that do not represent realistic refrigerator conditions

Keep difficult examples, however. Partially hidden food, poor lighting, unusual angles, and clutter can be valuable training data if a human can still reasonably label the object.

## Annotation

After review, annotate the selected images with bounding boxes.

Example:

```text
image: fridge_01_t00012.50s_f0000375.jpg

box 1 → milk
box 2 → fruits
box 3 → egg
```

The annotation should identify **where the object is**, not merely assign a label to the whole image.

## Dataset split

Do not randomly split frames from the same video without thinking about leakage.

For example, these two frames:

```text
fridge_01_t10.00s
fridge_01_t10.50s
```

may look almost identical.

If one goes into training and the other into validation, the validation score can look better than the model's real-world performance.

Prefer splitting by video/session when possible:

```text
Video/session A → train
Video/session B → train
Video/session C → validation
Video/session D → test
```

This is especially important for your project because the final camera will encounter continuous video rather than independent photographs.

## Next stage

Once the reviewed images exist, the next step is:

```text
reviewed images
      ↓
YOLO annotation
      ↓
YOLO dataset.yaml
      ↓
training
      ↓
validation
      ↓
test on completely unseen refrigerator footage
```

OCR should remain outside this stage. First establish that the system can reliably locate and classify food.
