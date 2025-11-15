#!/usr/bin/env python3
"""
Dataset Downloader for Parking Detector + LPR Project

Downloads:
- PKLot dataset
- CNRPark-EXT dataset (or instruct manual download)
- CCPD dataset (or instruct manual download)
- OpenALPR benchmark dataset

Creates unified structure under data/:
    data/images/
    data/labels/
    data/subsets/
"""

import os
import sys
import urllib.request
import zipfile
import tarfile
from pathlib import Path

try:
    import requests
except ImportError:
    print("Missing dependency: requests. Please run: pip install requests")
    sys.exit(1)

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

# Dataset URLs / instructions
PKLOT_URL        = "https://www.inf.ufpr.br/vri/databases/PKLot.tar.gz"
CNRPARK_URL      = "https://aimagelab.ing.unimore.it/files/CNRPark-EXT/CNRPark-EXT.zip"
CCPD_ZENODO_URL  = "https://zenodo.org/records/15647076/files/CCPD2019.tar.xz?download=1"  # reliable archive mirror
OPENALPR_URL     = "https://github.com/openalpr/benchmarks/archive/refs/heads/master.zip"

def ensure_dir(path: Path):
    if not path.exists():
        print(f"Creating directory: {path}")
        path.mkdir(parents=True, exist_ok=True)

def download_file_basic(url: str, dest: Path):
    if dest.exists():
        print(f"File already downloaded: {dest}")
        return
    print(f"Downloading: {url}")
    try:
        urllib.request.urlretrieve(url, dest)
        print(f"Saved to: {dest}")
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        sys.exit(1)

def download_file_stream(url: str, dest: Path, headers=None):
    if dest.exists():
        print(f"File already downloaded: {dest}")
        return
    print(f"Downloading (stream): {url}")
    try:
        with requests.get(url, stream=True, headers=headers or {"User-Agent":"Mozilla/5.0"}) as r:
            r.raise_for_status()
            content_type = r.headers.get("Content-Type", "")
            if "text/html" in content_type:
                print(f"Error: Server returned HTML instead of archive. URL may be blocked: {url}")
                return False
            with open(dest, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            print(f"Saved to: {dest}")
            return True
    except Exception as e:
        print(f"Error downloading {url} via stream: {e}")
        return False

def extract_archive(filepath: Path, dest: Path):
    print(f"Extracting {filepath} to {dest}")
    if filepath.suffix in [".zip"]:
        with zipfile.ZipFile(filepath, "r") as zf:
            zf.extractall(dest)
    elif filepath.suffix in [".gz", ".tgz", ".tar", ".xz"]:
        with tarfile.open(filepath, "r:*") as tf:
            tf.extractall(dest)
    else:
        print(f"Unknown archive format: {filepath}")
    print("Extraction complete.")

def download_pklot():
    print("\n=== PKLot Dataset ===")
    out_dir = DATA_DIR / "pklot"
    ensure_dir(out_dir)
    tar_file = out_dir / "PKLot.tar.gz"
    download_file_basic(PKLOT_URL, tar_file)
    extract_archive(tar_file, out_dir)

def download_cnrpark_ext():
    print("\n=== CNRPark-EXT Dataset ===")
    out_dir = DATA_DIR / "cnrpark"
    ensure_dir(out_dir)
    zip_file = out_dir / "CNRPark-EXT.zip"
    success = download_file_stream(CNRPARK_URL, zip_file)
    if not success:
        print("Unable to download CNRPark-EXT automatically.")
        print(f"Please manually download from: {CNRPARK_URL}")
        print(f"and place the file in: {zip_file}")
        return
    extract_archive(zip_file, out_dir)

def download_ccpd():
    print("\n=== CCPD Dataset ===")
    out_dir = DATA_DIR / "ccpd"
    ensure_dir(out_dir)
    # Use Zenodo mirror for reliability
    archive_file = out_dir / "CCPD2019.tar.xz"
    success = download_file_stream(CCPD_ZENODO_URL, archive_file)
    if not success:
        print("Unable to download CCPD automatically.")
        print(f"Please manually download from GitHub or Zenodo and place in: {archive_file}")
        return
    extract_archive(archive_file, out_dir)

def download_openalpr():
    print("\n=== OpenALPR Benchmark Dataset ===")
    out_dir = DATA_DIR / "openalpr"
    ensure_dir(out_dir)
    zip_file = out_dir / "openalpr.zip"
    download_file_basic(OPENALPR_URL, zip_file)
    extract_archive(zip_file, out_dir)

def create_unified_structure():
    print("\n=== Creating unified directory structure ===")
    for sub in ["images", "labels", "subsets"]:
        ensure_dir(DATA_DIR / sub)

def main():
    print("Starting dataset download and setup...\n")
    ensure_dir(DATA_DIR)
    download_pklot()
    download_cnrpark_ext()
    download_ccpd()
    download_openalpr()
    create_unified_structure()
    print("\nAll downloads attempted; check manually any that failed.")
    print("Next: preprocess annotations and images.")

if __name__ == "__main__":
    main()
