# Parking Detector and License Plate Recognition (LPR)

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square" />
  <img src="https://img.shields.io/badge/Deep%20Learning-PyTorch%20%7C%20Ultralytics%20YOLO-orange?style=flat-square" />
  <img src="https://img.shields.io/badge/Computer%20Vision-OpenCV%20%7C%20EasyOCR-green?style=flat-square" />
  <img src="https://img.shields.io/badge/Model%20Export-ONNX-lightgrey?style=flat-square" />
  <img src="https://img.shields.io/badge/Datasets-PKLot%20%7C%20CNRPark%20%7C%20CCPD-lightgrey?style=flat-square" />
</p>

---

## Presentation
[![Parking Detector + LPR Presentation](https://img.youtube.com/vi/yMmgbRg9xZE/0.jpg)](https://www.youtube.com/watch?v=yMmgbRg9xZE)

## Overview

This repository implements a full **parking analytics and license plate recognition system**, following the same structure and presentation style as the original Google Sites project page.

The system includes:

- **Parking space occupancy detection** (YOLOv8 fine‑tuned on PKLot)
- **Vehicle detection and tracking**
- **License plate detection**
- **OCR-based plate recognition** via EasyOCR or Tesseract
- **ONNX export** for deployment and hardware acceleration

---

## Features

- YOLOv8-based detection pipeline  
- Parking ROI mapping and binary occupied/empty classification  
- License plate cropping and OCR decoding  
- Evaluation of YOLO-small vs YOLO-nano variants  
- Visualization utilities for processed outputs  
- Containerized workflows for GPU and HPC environments  

---

## Datasets

- **PKLot** – Parking space occupancy  
- **CNRPark‑EXT** – Large parking dataset with varied lighting  
- **CCPD / OpenALPR** – License plate datasets  

---

## Environment Setup

See the Docker setup guide:

**docker/README.md**

---

## Training & Evaluation

Train detector models:

```bash
python source/train_models.py
```

Evaluate models:

```bash
python source/evaluate_models.py
```

Export model to ONNX:

```bash
python export_pklot_yolo.py --onnx
```

---

## Authors

Jacob M. Ramey – Virginia Tech, ECE 5554  
Paras Goda – Virginia Tech, ECE 5554  
GitHub: https://github.com/gawdygoda

---

# Photos & Captions

## Parking space occupancy  
<img src="https://github.com/user-attachments/assets/63b81163-07af-413f-98ad-46da0e5b2ec5" />

---

## License plate recognition  
<img src="https://github.com/user-attachments/assets/6cea82a2-d69d-4a37-adb0-dd43a52ad121" />

---

## YOLO‑World zero‑shot car and empty spot detection  
<img src="https://github.com/user-attachments/assets/5a42af45-24e6-4ed5-816a-5e568b7d9873" />

---

## Plate crops and OCR output  
<img src="https://github.com/user-attachments/assets/453ee7cf-c817-40e8-9489-c5f7d551e1a5" />
<img src="https://github.com/user-attachments/assets/8f4c90d8-6260-48ac-8eed-a6715af4f80f" />

---

## OCR challenges with angled or low‑resolution plates  
<img src="https://github.com/user-attachments/assets/57bb12a4-545e-4c16-9215-295121dd94d3" />

---

## PKLot original parking space occupancy  
<img src="https://github.com/user-attachments/assets/6f136b20-7a46-49aa-a6e3-c51c1eb8800a" />

---

## YOLO‑small vs YOLO‑nano result comparison  
<img src="https://github.com/user-attachments/assets/a6904b28-8e9b-4d66-bc73-ec37234023a3" />

---

<img src="https://github.com/user-attachments/assets/4494798c-be83-467b-befe-e8c9866ca89d" />

---
## Oriented bounding boxes vs axis‑aligned – reduced overlap  
<img src="https://github.com/user-attachments/assets/122fa0c4-1c38-44ad-8838-8e8cb450294e" />

---
## Heatmap: time‑of‑day / day‑of‑week occupancy  
<img src="https://github.com/user-attachments/assets/291a4d89-e997-40e9-8cc2-940986540afe" />

---
## Empty‑spot distribution by day – box & whisker plot  
<img src="https://github.com/user-attachments/assets/4c6443ed-a569-4d27-bf68-022be3aa4c9b" />

---

## Distorted image ground‑truth labels vs trained model output  
<img src="https://github.com/user-attachments/assets/99682f8a-9053-4b06-8cd6-ecacf9243931" />

