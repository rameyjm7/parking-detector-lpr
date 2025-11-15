# Docker and Apptainer Environment
## Parking Detector + License Plate Recognition Project

This directory contains the complete containerization setup for reproducible GPU-enabled experiments for the Parking Detector + License Plate Recognition (LPR) project. The Makefile provides unified commands for building, running, and managing both Docker and Apptainer (Singularity) environments.

---

# Makefile Targets

## Docker Targets

### `make build`
Builds the Docker image using the Dockerfile in this directory.

Image produced:
```
$(DOCKER_USER)/$(IMAGE_NAME):$(TAG)
```

### `make push`
Pushes the built Docker image to Docker Hub under:
```
docker.io/$(DOCKER_USER)/$(IMAGE_NAME):$(TAG)
```

### `make run`
Launches JupyterLab using `docker-compose`, exposing port 8888 by default.  
The project root is mounted to `/workspace` inside the container.

### `make stop`
Stops all services launched with docker-compose.

### `make shell`
Opens an interactive bash shell inside the container.

Behavior:
- If a container named `parking-detector-lpr` is already running, it opens a shell inside it.
- If not, it starts a temporary GPU-enabled container and opens a shell.

### `make clean`
Removes the local Docker image:
```
docker image rm rameyjm7/parking-detector-lpr:latest
```

---

## Apptainer (HPC) Targets

All Apptainer commands automatically load the `apptainer` module.

### `make sif`
Builds a `.sif` Apptainer image from the Docker Hub version of the container:
```
parking_detector_lpr.sif
```

### `make apptainer-shell`
Starts an interactive shell inside the `.sif` image with GPU passthrough enabled.

Equivalent to:
```
apptainer exec --nv parking_detector_lpr.sif /bin/bash
```

### `make apptainer-lab`
Launches JupyterLab inside the Apptainer container with GPU enabled.

Default token:
```
parking
```

---

## Usage Summary

### Build and run locally
```
make build
make run
```

Open browser at:
```
http://localhost:8888
```

### Enter container shell
```
make shell
```

### HPC Workflows
```
make sif
make apptainer-shell
make apptainer-lab
```

---

## Notes

- The environment supports CUDA 12.1, PyTorch (GPU), OpenCV, ultralytics (YOLOv8), EasyOCR, timm (ConvNeXt), and JupyterLab.
- The project root must be mounted to `/workspace` for training scripts and notebooks to access datasets.

