from ultralytics import YOLO
from ultralytics import settings
import os
import torch
import time

# ============================================
# SETTINGS
# ============================================
USE_OBB = False # Output OBB lables vs AABB

if USE_OBB:
    DATA_DIR = "../data/pklot_yolo_obb"
    MODEL_WEIGHTS = f"{DATA_DIR}/yolo11s-obb.pt"
else:
    DATA_DIR = "../data/pklot_yolo_aabb"
    MODEL_WEIGHTS = f"{DATA_DIR}/yolov8s.pt"

YAML_PATH = f"{DATA_DIR}/pklot_yolo.yaml"
PROJECT_DIR = f"{DATA_DIR}/runs"

# ------------------------------
# Start Time
# ------------------------------
start_time = time.time()

print(f"Is CUDA available? {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"Current Device: {torch.cuda.get_device_name(0)}")
else:
    print("Warning: Running on CPU!")

model = YOLO(MODEL_WEIGHTS)

results = model.train(data=YAML_PATH, 
                    project=PROJECT_DIR,
                    val=True,
                    imgsz=1280,
                    epochs=10,
                    patience=3,
                    save=True,
                    plots=True,
)

# ------------------------------
# End Time
# ------------------------------
end_time = time.time()
elapsed = end_time - start_time
mins, secs = divmod(elapsed, 60)

print(f"Total time: {mins:.0f} min {secs:.2f} sec")