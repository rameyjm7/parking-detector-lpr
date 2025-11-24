from ultralytics import YOLO
import torch
import os
from collections import Counter
import time
from tqdm import tqdm
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns

# ============================================
# SETTINGS
# ============================================
USE_OBB = False # Output OBB lables vs AABB

if USE_OBB:
    DATA_DIR = "../data/pklot_yolo_obb"
else:
    DATA_DIR = "../data/pklot_yolo_aabb"

YAML_PATH = f"{DATA_DIR}/pklot_yolo.yaml"
PROJECT_DIR = f"{DATA_DIR}/runs"
MODEL_WEIGHTS = f"{DATA_DIR}/runs/train/weights/best.pt"
SOURCE_DIR = f'{DATA_DIR}/test/images'

num_files = len([f for f in os.listdir(SOURCE_DIR) if f.endswith(('.jpg'))])

# ------------------------------
# Start Time
# ------------------------------
start_time = time.time()

total_spots_histogram = Counter()
data_records = []
inference_times_ms = []

model = YOLO(MODEL_WEIGHTS)

results = model.predict(
    source=SOURCE_DIR,
    project=PROJECT_DIR,
    conf=0.25,      
    save=True,
    verbose=False,
    line_width=1,
    agnostic_nms=True,
    stream=True
)

for result in tqdm(results, total=num_files, desc="Predicting on Images"):    
    inference_times_ms.append(sum(result.speed.values()))
    counts = {"empty": 0, "occupied": 0}

    if USE_OBB:
        if result.obb is not None:
            detected_classes = result.obb.cls.cpu().numpy()
        else:
            detected_classes = []
    else:
        if result.boxes is not None:
            detected_classes = result.boxes.cls.cpu().numpy()
        else:
            detected_classes = []

    current_total_spots = len(detected_classes)
    total_spots_histogram[current_total_spots] += 1
    
    for class_id in detected_classes:
        class_name = model.names[int(class_id)]
        if class_name in counts:
            counts[class_name] += 1
        else:
            counts[class_name] = 1

    full_path = result.path
    filename = os.path.basename(full_path)
    filename_date = os.path.splitext(filename)[0]

    try:
        timestamp = datetime.strptime(filename_date, "%Y-%m-%d_%H_%M_%S")
        data_records.append({
            'timestamp': timestamp,
            'empty': counts['empty'],
            'total': current_total_spots
        })
    except ValueError:
        pass


print("\n" + "="*40)
print("PARKING LOT CAPACITY ANALYSIS")
print("="*40)
print("Total Spots | Occurrences (Frames)")
print("-" * 30)
for total, frequency in total_spots_histogram.most_common():
    print(f" {total:<10} | {frequency}")

# ============================================
# Plotting
# ============================================
print("\nGenerating Graph...")

if data_records:
    df = pd.DataFrame(data_records)
    df.set_index('timestamp', inplace=True)
    df.sort_index(inplace=True)
    segments = [
        ("PUCPR", df.index < "2012-11-21", 100),
        ("UFPR04", (df.index >= "2012-11-21") & (df.index <= "2013-01-29"), 28),
        ("UFPR05", df.index > "2013-01-29", 40)
    ]

    for name, mask, current_capacity in segments:
        sub_df = df[mask]
        if sub_df.empty:
            print(f"Skipping {name}: No data found in this date range.")
            continue
        
        # ---------------------------------------------------------
        # 1. Occupancy Graphs
        # ---------------------------------------------------------
        plt.figure(figsize=(30, 6))
        plt.plot(sub_df.index, sub_df['empty'], label='Empty Spots', color='green', linewidth=2)
        plt.plot(sub_df.index, sub_df['total'], label='Total Spots', color='blue', linewidth=2, linestyle='--')
        plt.axhline(y=current_capacity, color='red', linestyle=':', linewidth=1.5, alpha=0.7, label=f'Capacity')
        plt.title(f'Parking Lot Occupancy - {name}')
        plt.xlabel('Date/Time')
        plt.ylabel('Number of Cars')
        plt.legend(loc='upper right')
        plt.grid(True, alpha=0.3)
        ax = plt.gca()    
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        output_filename = f'{DATA_DIR}/occupancy_graph_{name}.png'
        plt.savefig(output_filename)
        plt.close()

        print(f"Graph saved to: {output_filename}")

        # ---------------------------------------------------------
        # 2. Temporal Analysis Box Plots
        # ---------------------------------------------------------
        sub_df = sub_df.copy()
        sub_df['DayOfWeek'] = sub_df.index.day_name()
        sub_df['Hour'] = sub_df.index.hour
        days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        plt.figure(figsize=(12, 6))
        sns.boxplot(x='DayOfWeek', y='empty', data=sub_df, order=days_order, palette="viridis")
        plt.title(f'{name} - Empty Spots Distribution by Day')
        plt.ylabel('Number of Empty Spots')
        plt.grid(True, alpha=0.3)
        plt.savefig(f'{DATA_DIR}/analysis_boxplot_{name}.png')
        plt.close()

        # ---------------------------------------------------------
        # 3. Temporal Analysis Heatmaps
        # ---------------------------------------------------------
        try:
            pivot = sub_df.pivot_table(index='DayOfWeek', columns='Hour', values='empty', aggfunc='mean')
            pivot = pivot.reindex(days_order)
            plt.figure(figsize=(12, 6))
            sns.heatmap(pivot, cmap="RdYlGn", annot=True, fmt=".0f", linewidths=.5)
            plt.title(f'{name} - Average Empty Spots (Heatmap)')
            plt.savefig(f'{DATA_DIR}/analysis_heatmap_{name}.png')
            plt.close()
        except Exception as e:
            print(f"Skipping heatmap for {name} (not enough data): {e}")
else:
    print("No valid date-formatted files found. Skipping graph.")

# ============================================
# Performance Statistics
# ============================================
print("\n" + "="*40)
print("PERFORMANCE REPORT")
print("="*40)

if inference_times_ms:
    avg_latency = sum(inference_times_ms) / len(inference_times_ms)
    avg_fps = 1000.0 / avg_latency    
    print(f"Avg Latency (End-to-End): {avg_latency:.2f} ms per image")
    print(f"True Model Speed:         {avg_fps:.2f} FPS")
else:
    print("No times recorded.")

metrics = model.val(
    data=YAML_PATH,
    project=PROJECT_DIR,
    split='test',
    imgsz=1280,      
    conf=0.25,
    plots=True,
    verbose=True
)

# ------------------------------
# End Time
# ------------------------------
end_time = time.time()
elapsed = end_time - start_time
mins, secs = divmod(elapsed, 60)

print(f"Total time: {mins:.0f} min {secs:.2f} sec")