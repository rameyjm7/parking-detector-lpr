# Trained Models
## Parking Detector + License Plate Recognition Project

This directory contains the trained models for the Parking Detector + License Plate Recognition (LPR) project.

---

## Models

### PKLot
Models are fine-tuned with YOLOv8/v11 on a NVIDA GPU with the PKLot dataset. Select the correct task for use, see below.


```
pklot_yolov8_aabb_best.pt
```
This model was trained with the `detect` task to discover Axis-Aligned Bounding Boxes and classificaion. 


```
pklot_yolov11_obb_best.pt
```
This model was trained with the `oob` task to discover Oriented Bounding Boxes and classificaion.

---

## Usage

### PKLot
Prediciton and validation code can be found in the [source](../source/test_pklot.py) folder. You can set the 'USE_OBB' flag at top of the code to select the task.



