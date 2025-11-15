#!/usr/bin/env python3
"""
Reliable dataset downloader for Parking Detector + LPR Project

Uses CLI wget (via os.popen) because HPC proxies often block Python requests.
Validates downloaded files and deletes invalid HTML/empty files.
"""

import os
import sys
import zipfile
import tarfile
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

PKLOT_URL       = "https://www.inf.ufpr.br/vri/databases/PKLot.tar.gz"
CNRPARK_URL     = "https://aimagelab.ing.unimore.it/files/CNRPark-EXT/CNRPark-EXT.zip"
CCPD_URL        = "https://zenodo.org/records/15647076/files/CCPD2019.tar.xz?download=1"
OPENALPR_URL    = "https://github.com/openalpr/benchmarks/archive/refs/heads/master.zip"


# ----------------------------------------------------------------------
def ensure_dir(path: Path):
    if not path.exists():
        print(f"Creating directory: {path}")
        path.mkdir(parents=True, exist_ok=True)


# ----------------------------------------------------------------------
def download_with_wget(url: str, dest: Path):
    """
    Uses CLI wget EXACTLY as the user would type in the terminal.
    This bypasses proxy/SSL restrictions that break Python libraries.
    """

    # Already downloaded
    if dest.exists():
        print(f"File already exists: {dest}")
        return True

    print(f"\nRunning wget for: {url}")
    cmd = f"wget -O '{dest}' '{url}' 2>&1"
    stream = os.popen(cmd)
    output = stream.read()
    ret = stream.close()

    if ret is not None:
        print("wget failed. Output:")
        print(output)
        return False

    # Validate file (not HTML, not empty)
    if dest.stat().st_size < 1024:
        print("Downloaded file is too small. Likely an HTML error page.")
        dest.unlink(missing_ok=True)
        return False

    with open(dest, "rb") as f:
        sig = f.read(4)

    # ZIP magic: 50 4B 03 04
    # TAR/GZ/XZ magic:
    valid_headers = [
        b"PK\x03\x04",  # zip
        b"\x1f\x8b\x08",  # gzip
        b"*\x00\x00\x00",  # xz
    ]

    if not any(sig.startswith(h) for h in valid_headers):
        print("Downloaded file is not a valid archive (HTML or error). Deleting.")
        dest.unlink(missing_ok=True)
        return False

    print(f"Downloaded OK: {dest}")
    return True


# ----------------------------------------------------------------------
def extract_archive(filepath: Path, dest: Path):
    print(f"Extracting: {filepath}")

    try:
        if filepath.suffix == ".zip":
            with zipfile.ZipFile(filepath, "r") as zf:
                zf.extractall(dest)
        else:
            with tarfile.open(filepath, "r:*") as tf:
                tf.extractall(dest)
    except Exception as e:
        print(f"Extraction failed for {filepath}: {e}")
        return False

    print("Extraction complete.")
    return True


# ----------------------------------------------------------------------
def download_pklot():
    print("\n=== PKLot Dataset ===")
    out = DATA_DIR / "pklot"
    ensure_dir(out)
    f = out / "PKLot.tar.gz"

    if download_with_wget(PKLOT_URL, f):
        extract_archive(f, out)
    else:
        print("PKLot download failed. Please manually download.")


def download_cnrpark():
    print("\n=== CNRPark-EXT Dataset ===")
    out = DATA_DIR / "cnrpark"
    ensure_dir(out)
    f = out / "CNRPark-EXT.zip"

    if download_with_wget(CNRPARK_URL, f):
        extract_archive(f, out)
    else:
        print("CNRPark-EXT download failed.")
        print("Manual URL:")
        print("  https://aimagelab.ing.unimore.it/files/CNRPark-EXT/CNRPark-EXT.zip")
        print(f"Place file at: {f}")


def download_ccpd():
    print("\n=== CCPD Dataset ===")
    out = DATA_DIR / "ccpd"
    ensure_dir(out)
    f = out / "CCPD2019.tar.xz"

    if download_with_wget(CCPD_URL, f):
        extract_archive(f, out)
    else:
        print("CCPD download failed.")
        print("Manual URL (Zenodo):")
        print("  https://zenodo.org/records/15647076")
        print(f"Place file at: {f}")


def download_openalpr():
    print("\n=== OpenALPR Benchmark Dataset ===")
    out = DATA_DIR / "openalpr"
    ensure_dir(out)
    f = out / "openalpr.zip"

    if download_with_wget(OPENALPR_URL, f):
        extract_archive(f, out)
    else:
        print("OpenALPR download failed.")


# ----------------------------------------------------------------------
def create_unified_structure():
    print("\n=== Creating unified data structure ===")
    for folder in ["images", "labels", "subsets"]:
        ensure_dir(DATA_DIR / folder)


# ----------------------------------------------------------------------
def main():
    print("Starting dataset download...\n")
    ensure_dir(DATA_DIR)

    # download_pklot()
    # download_cnrpark()
    # download_ccpd()
    # download_openalpr()

    create_unified_structure()

    print("\nDataset download process complete.")
    print("Check any failed datasets manually.")


if __name__ == "__main__":
    main()
