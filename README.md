# Parking Detector and License Plate Recognition (LPR)

## Overview
This Computer Vision project detects vehicles, classifies parking space occupancy, and recognizes license plates in real-world parking lot footage.  
The system integrates object detection, classification, and OCR pipelines to automate parking analytics.

## Features
- **Vehicle Detection** using YOLOv8, ResNet, or a custom CNN-based model
- **Parking Occupancy Analysis** using ROI mapping and car centroid tracking
- **License Plate Recognition** via EasyOCR / Tesseract
- **Comparative Evaluation** of YOLO, ResNet, and CNN on accuracy, speed, and robustness
- **Visualization Tools** for annotated detections and parking space overlays

## Datasets
- **PKLot** – Parking occupancy classification  
- **CNRPark-EXT** – Extended parking space dataset  
- **CCPD / OpenALPR** – License plate detection and OCR datasets

## Repository Structure
```
├── data/                # Datasets (PKLot, CNRPark, CCPD, OpenALPR)
├── scripts/             # Preprocessing and training scripts
├── models/              # Trained YOLO / ResNet / CNN weights
├── results/             # Evaluation metrics and visual outputs
├── report/              # Final report and figures
├── video/               # Project presentation materials
└── README.md
```

## Environment Setup
```bash
python3 -m venv cv_env
source cv_env/bin/activate
pip install -r requirements.txt
```

## Training and Evaluation
Run detection model training (YOLO / ResNet / CNN):
```bash
python scripts/train_models.py
```

Evaluate models and generate comparative results:
```bash
python scripts/evaluate_models.py
```

## Deliverables
- **Final Report** (Due Dec 7) – Full methodology, experiments, and results  
- **Project Video** (Due Dec 10) – 1–2 minute narrated summary with demos

## Author
Jacob M. Ramey - Virginia Tech | ECE 5554 Computer Vision  
Paras Goda     - Virginia Tech | ECE 5554 Computer Vision  
