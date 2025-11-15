# ============================================================
#  Parking Detector + License Plate Recognition Project
#  Unified Docker and Apptainer Makefile
#  Author: Jacob Ramey
# ============================================================

DOCKER_USER  = rameyjm7
IMAGE_NAME   = parking-detector-lpr
TAG          = latest
PORT         = 8888
TOKEN        = parking
CONTAINER    = parking-detector-lpr
SIF_NAME     = parking_detector_lpr.sif

# ------------------------------------------------------------
# Docker: Build image
# ------------------------------------------------------------
build:
	@echo "Building Docker image..."
	docker build -t $(DOCKER_USER)/$(IMAGE_NAME):$(TAG) .

# ------------------------------------------------------------
# Docker: Push to Docker Hub
# ------------------------------------------------------------
push:
	@echo "Pushing Docker image to Docker Hub..."
	docker push $(DOCKER_USER)/$(IMAGE_NAME):$(TAG)

# ------------------------------------------------------------
# Docker: Run Jupyter through docker-compose
# ------------------------------------------------------------
run:
	@echo "Launching Jupyter Lab on http://localhost:$(PORT)"
	docker compose up

# ------------------------------------------------------------
# Docker: Stop services
# ------------------------------------------------------------
stop:
	@echo "Stopping docker-compose..."
	docker compose down

# ------------------------------------------------------------
# Docker: Interactive shell
# If container exists, exec into it.
# If not, start a GPU-enabled container and open a shell.
# ------------------------------------------------------------
shell:
	@if docker ps --format '{{.Names}}' | grep -q '^$(CONTAINER)$$'; then \
	    echo "Entering running container..."; \
	    docker exec -it $(CONTAINER) /bin/bash; \
	else \
	    echo "Starting container and opening shell..."; \
	    docker run --gpus all --rm -it \
	        --name $(CONTAINER) \
	        -p $(PORT):8888 \
	        -v $$(pwd):/workspace \
	        $(DOCKER_USER)/$(IMAGE_NAME):$(TAG) \
	        /bin/bash; \
	fi

# ------------------------------------------------------------
# Docker: Remove local image
# ------------------------------------------------------------
clean:
	@echo "Removing local Docker image..."
	docker image rm $(DOCKER_USER)/$(IMAGE_NAME):$(TAG) -f || true

# ============================================================
# Apptainer / Singularity Targets (HPC)
# All commands load the module automatically
# ============================================================

# ------------------------------------------------------------
# Apptainer: Build SIF image from Docker Hub
# ------------------------------------------------------------
sif:
	@echo "Building Apptainer SIF image from Docker Hub..."
	module load apptainer && \
	apptainer build $(SIF_NAME) docker://$(DOCKER_USER)/$(IMAGE_NAME):$(TAG)

# ------------------------------------------------------------
# Apptainer: Interactive shell inside SIF (with GPU)
# ------------------------------------------------------------
apptainer-shell:
	@echo "Starting Apptainer shell (GPU enabled)..."
	module load apptainer && \
	apptainer exec --nv $(SIF_NAME) /bin/bash

# ------------------------------------------------------------
# Apptainer: Launch Jupyter Lab inside SIF
# ------------------------------------------------------------
apptainer-lab:
	@echo "Launching Jupyter Lab inside Apptainer on port $(PORT)"
	module load apptainer && \
	apptainer exec --nv $(SIF_NAME) \
	    jupyter lab --ip=0.0.0.0 --port=$(PORT) \
	    --no-browser --allow-root --NotebookApp.token=$(TOKEN)

# ------------------------------------------------------------
# Help
# ------------------------------------------------------------
help:
	@echo ""
	@echo "Parking Detector - LPR Makefile Commands"
	@echo ""
	@echo " Docker:"
	@echo "   make build            Build Docker image"
	@echo "   make push             Push image to Docker Hub"
	@echo "   make run              Launch Jupyter Lab via docker-compose"
	@echo "   make stop             Stop docker-compose"
	@echo "   make shell            Enter container with bash"
	@echo "   make clean            Remove local Docker image"
	@echo ""
	@echo " Apptainer (HPC):"
	@echo "   make sif              Build SIF image from Docker Hub"
	@echo "   make apptainer-shell  Interactive shell inside SIF"
	@echo "   make apptainer-lab    Launch Jupyter Lab inside SIF"
	@echo ""
