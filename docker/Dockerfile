FROM nvidia/cuda:12.1.1-cudnn8-runtime-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive

# ------------------------------------------------------------
# System dependencies (OpenCV, FFmpeg, Tesseract, dev tools)
# ------------------------------------------------------------
RUN apt-get clean && apt-get update -o Acquire::Retries=3 -o Acquire::http::No-Cache=True && \
    apt-get install -y \
        git wget curl \
        python3 python3-pip python3-dev \
        build-essential \
        ca-certificates \
        pkg-config \
        libopencv-dev python3-opencv \
        libv4l-dev \
        ffmpeg \
        tesseract-ocr \
        tesseract-ocr-eng \
        libtesseract-dev && \
    rm -rf /var/lib/apt/lists/*

# ------------------------------------------------------------
# Workspace
# ------------------------------------------------------------
WORKDIR /workspace
COPY . /workspace/

# ------------------------------------------------------------
# Python dependencies
# ------------------------------------------------------------
RUN pip install --upgrade pip && \
    pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu121 && \
    pip install timm && \
    pip install \
        ultralytics \
        easyocr \
        albumentations \
        numpy scipy scikit-learn scikit-image \
        matplotlib seaborn pandas \
        imutils \
        tqdm jupyterlab notebook ipywidgets \
        python-Levenshtein \
        lapx

# ------------------------------------------------------------
# Environment
# ------------------------------------------------------------
ENV PYTHONUNBUFFERED=1
ENV JUPYTER_TOKEN="parking"

EXPOSE 8888

# ------------------------------------------------------------
# Default command: launch Jupyter Lab
# ------------------------------------------------------------
CMD ["bash", "-c", "jupyter lab --ip=0.0.0.0 --port=8888 --no-browser --allow-root --NotebookApp.token=$JUPYTER_TOKEN"]
