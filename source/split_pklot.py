import os
import xml.etree.ElementTree as ET
from pathlib import Path
import shutil
import random
import cv2
from tqdm import tqdm
import yaml
import time

# ============================================
# SETTINGS
# ============================================
TEST_RATIO = 0.20
VAL_RATIO  = 0.10
TRAIN_RATIO = 0.70
USE_OBB = True # Output OBB lables vs AABB


# ============================================
# PATHS
# ============================================
BASE_DIR = Path.cwd().parents[0]
PKLOT_ROOT = BASE_DIR / "data/pklot/PKLot/PKLot"  
if USE_OBB:
    OUT_DIR = BASE_DIR / "data/pklot_yolo_obb"
else:
    OUT_DIR = BASE_DIR / "data/pklot_yolo_aabb"

TRAIN_DIR = OUT_DIR / "train"
VAL_DIR   = OUT_DIR / "val"
TEST_DIR  = OUT_DIR / "test"


# ============================================
# HELPERS
# ============================================
def ensure_dirs():
    """Creates the necessary YOLO directory structure
    data/
     └── pklot_yolo/
           ├── images/
           ├── labels/
           ├── train/
           │    ├── images/
           │    └── labels/
           ├── val/
           │    ├── images/
           │    └── labels/
           └── test/
                ├── images/
                └── labels/
    """
    if OUT_DIR.exists():
        pass

    IMG_OUT.mkdir(parents=True, exist_ok=True)
    LBL_OUT.mkdir(parents=True, exist_ok=True)    
    for d in [TRAIN_DIR, VAL_DIR, TEST_DIR]:
        (d / "images").mkdir(parents=True, exist_ok=True)
        (d / "labels").mkdir(parents=True, exist_ok=True)

def parse_xml(xml_file):
    """Parses PKLot XML format for AABB (center + height and width)"""
    try:
        root = ET.parse(xml_file).getroot()
        items = []
        for s in root.findall("space"):
            occ = int(s.attrib.get("occupied", 0))
            rect = s.find("rotatedRect")
            c = rect.find("center")
            sz = rect.find("size")
            cx = float(c.attrib["x"])
            cy = float(c.attrib["y"])
            w  = float(sz.attrib["w"])
            h  = float(sz.attrib["h"])
            items.append((occ, cx, cy, w, h))
        return items
    except Exception as e:
        return None

def parse_xml_obb(xml_file):
    """Parses PKLot XML format for OBB (Extracts 4 contour points)"""
    try:
        root = ET.parse(xml_file).getroot()
        items = []
        for s in root.findall("space"):
            occ = int(s.attrib.get("occupied", 0))
            contour = s.find("contour")
            points = []
            if contour is not None:
                for pt in contour.findall("point"):
                    px = float(pt.attrib["x"])
                    py = float(pt.attrib["y"])
                    points.append((px, py))
            
            if len(points) == 4:
                items.append((occ, points))
                
        return items
    except Exception as e:
        print(f"Error parsing {xml_file}: {e}")
        return None

def convert_bbox(cx, cy, w, h, W, H):
    """Normalizes coordinates to 0-1 range"""
    return cx/W, cy/H, w/W, h/H

# ============================================
# EXPORT YOLO LABELS
# ============================================
def process_batch(file_list, destination_dir):
    """
    Copies images and creates label files for a specific list of files 
    to a specific destination (train, val, or test).
    """
    for (img_path, xml_path) in tqdm(file_list, desc=f"Processing to {destination_dir.name}"):
        if USE_OBB:
            ann = parse_xml_obb(xml_path)
        else:
           ann = parse_xml(xml_path) 

        if ann is None:
            continue

        img = cv2.imread(str(img_path))
        if img is None:
            continue
        H, W = img.shape[:2]

        filename = img_path.name
        out_img_path = destination_dir / "images" / filename
        out_lbl_path = destination_dir / "labels" / filename.replace(".jpg", ".txt")
        shutil.copy(img_path, out_img_path)

        with open(out_lbl_path, "w") as f:
            if USE_OBB:
                for occ, points in ann:
                    cls = 1 if occ == 1 else 0
                    normalized_points = []
                    for (px, py) in points:
                        nx = px / W
                        ny = py / H
                        nx = max(0.0, min(1.0, nx))
                        ny = max(0.0, min(1.0, ny))
                        normalized_points.extend([nx, ny])
                    
                    coords_str = " ".join([f"{p:.6f}" for p in normalized_points])
                    f.write(f"{cls} {coords_str}\n")
            else:
                for occ, cx, cy, w, h in ann:
                    cls = 1 if occ == 1 else 0
                    nx, ny, nw, nh = convert_bbox(cx, cy, w, h, W, H)
                    nx = max(0, min(1, nx))
                    ny = max(0, min(1, ny))
                    nw = max(0, min(1, nw))
                    nh = max(0, min(1, nh))
                    f.write(f"{cls} {nx:.6f} {ny:.6f} {nw:.6f} {nh:.6f}\n")

# ============================================
# STRATIFIED TRAIN/VAL/TEST SPLIT
# ============================================
def create_stratified_dataset():
    """
    Splits the dataset into train, val, or test and ensures
    each campus is represented equally in each set
    """
    ensure_dirs()
    print("=== scanning files ===")
    campus_data = {}

    for campus in sorted(os.listdir(PKLOT_ROOT)):
        campus_dir = PKLOT_ROOT / campus
        if not campus_dir.is_dir():
            continue
        
        campus_data[campus] = []
        print(f"Scanning Campus: {campus}...")

        for weather in os.listdir(campus_dir):
            weather_dir = campus_dir / weather
            if not weather_dir.is_dir(): 
                continue
            
            for date in os.listdir(weather_dir):
                date_dir = weather_dir / date
                if not date_dir.is_dir(): 
                    continue

                imgs = [f for f in os.listdir(date_dir) if f.endswith(".jpg")]
                
                for img_name in imgs:
                    img_path = date_dir / img_name
                    xml_path = img_path.with_suffix(".xml")
                    
                    if xml_path.exists():
                        campus_data[campus].append((img_path, xml_path))

    print("\n=== Splitting & Processing ===")
    
    for campus, files in campus_data.items():
        total_files = len(files)
        print(f"\nProcessing {campus}: {total_files} images found.")
        random.shuffle(files)
        n_test = int(total_files * TEST_RATIO)
        n_val = int(total_files * VAL_RATIO)
        test_files = files[:n_test]
        val_files = files[n_test : n_test + n_val]
        train_files = files[n_test + n_val:]
        
        print(f"  - Test:  {len(test_files)}")
        print(f"  - Val:   {len(val_files)}")
        print(f"  - Train: {len(train_files)}")

        process_batch(test_files, TEST_DIR)
        process_batch(val_files, VAL_DIR)
        process_batch(train_files, TRAIN_DIR)

# ============================================
# WRITE CONFIG
# ============================================
def write_yolo_config():
    config_path = OUT_DIR / "pklot_yolo.yaml"
    cfg = {
        "path": str(OUT_DIR.absolute()),
        "train": "train/images",
        "val":   "val/images",
        "test":  "test/images",
        "names": {0: "empty", 1: "occupied"}
    }
    with open(config_path, "w") as f:
        yaml.dump(cfg, f)
    print("\n\nYOLO config written ->", config_path)

# ============================================
# EXECUTE
# ============================================
if __name__ == "__main__":
    # ------------------------------
    # Start Time
    # ------------------------------
    start_time = time.time()

    create_stratified_dataset()
    write_yolo_config()
    
    print("\n=== COMPLETE ===")
    print(f"Images are saved in {OUT_DIR}")

    # ------------------------------
    # End Time
    # ------------------------------
    end_time = time.time()
    elapsed = end_time - start_time
    mins, secs = divmod(elapsed, 60)

    print(f"Total time: {mins:.0f} min {secs:.2f} sec")