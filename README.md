# Parking Detector and License Plate Recognition (LPR)

## Overview
This Computer Vision project detects vehicles, classifies parking space occupancy, and recognizes license plates in real-world parking lot footage.  
The system integrates object detection, classification, and OCR pipelines to automate parking analytics.

## Features
- Vehicle Detection using YOLOv8, ResNet, or a custom CNN-based model
- Parking Occupancy Analysis using ROI mapping and car centroid tracking
- License Plate Recognition via EasyOCR / Tesseract
- Comparative Evaluation of YOLO, ResNet, and CNN on accuracy, speed, and robustness
- Visualization Tools for annotated detections and parking space overlays

## Datasets
- PKLot – Parking occupancy classification  
- CNRPark-EXT – Extended parking space dataset  
- CCPD / OpenALPR – License plate detection and OCR datasets

## Repository Structure (TBD)
```
├── data/
│   ├── pklot/
│   ├── cnrpark/
│   ├── ccpd/
│   ├── openalpr/
│   └── pklot_yolo/
│
├── source/
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
├── notebooks/
│   ├── eda_pklot.ipynb
│   └── export_yolo.ipynb
│
├── docker/
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── Makefile
│
├── models/
│   ├── yolo/
│   ├── convnext/
│   ├── resnet/
│   └── cnn/
│
├── results/
│   ├── yolo/
│   ├── convnext/
│   ├── cnn/
│   └── comparisons/
│
├── report/
│   ├── final_report.docx
│   ├── figures/
│   └── tables/
│
├── video/
│   ├── script.txt
│   ├── raw_clips/
│   └── final_edit.mp4
│
└── README.md
```

## Environment Setup
For all local development and HPC workflows, see the Docker setup guide:

**[docker/README.md](docker/README.md)**

## Training and Evaluation
Run detection model training (YOLO / ResNet / CNN):
```bash
python source/train_models.py
```

Evaluate models and generate comparative results:
```bash
python source/evaluate_models.py
```

## Deliverables
- **Final Report** (Due Dec 7) – Full methodology, experiments, and results  
- **Project Video** (Due Dec 10) – 1–2 minute narrated summary with demos

## Authors
Jacob M. Ramey – Virginia Tech | ECE 5554 Computer Vision  
Paras Goda – Virginia Tech | ECE 5554 Computer Vision  
GitHub: https://github.com/gawdygoda

## High Level Plan
<img width="1496" height="1141" src="https://github.com/user-attachments/assets/11b514b3-b238-4f05-beb5-d79ebf8ae31b" />
