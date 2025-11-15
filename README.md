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

## Repository Structure (TBD)
```
├── data/                # All datasets (PKLot, CNRPark, CCPD, OpenALPR, YOLO exports)
│   ├── pklot/
│   ├── cnrpark/
│   ├── ccpd/
│   ├── openalpr/
│   └── pklot_yolo/      # YOLOv8 images/labels + train/val/test splits
│
├── source/              # All Python source code for preprocessing, training, OCR, etc.
│   ├── download_datasets.py
│   ├── preprocess_images.py
│   ├── preprocess_datasets.py
│   ├── train_yolo.py
│   ├── train_convnext.py
│   ├── train_cnn.py
│   ├── evaluate_models.py
│   ├── visualize_results.py
│   ├── ocr_pipeline.py
│   ├── detect_spaces.py
│   └── evaluate_ocr.py
│
├── notebooks/           # Jupyter notebooks (EDA, YOLO export, visualization)
│   ├── eda_pklot.ipynb
│   └── export_yolo.ipynb
│
├── docker/              # Dockerfile, docker-compose.yml, Makefile
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── Makefile
│
├── models/              # Checkpoints: YOLO, ConvNeXt, ResNet, CNN
│   ├── yolo/
│   ├── convnext/
│   ├── resnet/
│   └── cnn/
│
├── results/             # Training logs, evaluation metrics, confusion matrices, plots
│   ├── yolo/
│   ├── convnext/
│   ├── cnn/
│   └── comparisons/
│
├── report/              # Final report assets
│   ├── final_report.docx
│   ├── figures/
│   └── tables/
│
├── video/               # Final project video, narration, demo clips
│   ├── script.txt
│   ├── raw_clips/
│   └── final_edit.mp4
│
└── README.md            # Top-level project description

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
Paras Goda     - Virginia Tech | ECE 5554 Computer Vision  https://github.com/gawdygoda


## High Level Plan
<img width="1496" height="1141" alt="image" src="https://github.com/user-attachments/assets/11b514b3-b238-4f05-beb5-d79ebf8ae31b" />


