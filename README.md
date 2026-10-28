# FreshAI ML Handoff

Read these for the context:

1. `PROJECT_CONTEXT.md` — project and ML context.
2. `ANNOTATION_SPEC.md` — exact labeling rules.

Current pipeline:

Videos → OpenCV frame extraction → review → annotation → YOLO dataset → training → evaluation → unseen-video inference → failure analysis → improved data → retraining.

OCR and inventory management are later stages.

Current status: preparing the dataset and first YOLO model.

The class list is provisional until the pilot annotation is completed.

Source: uploaded competition proposal `[Draft] Samsung Solve for tomorrow .docx`.
