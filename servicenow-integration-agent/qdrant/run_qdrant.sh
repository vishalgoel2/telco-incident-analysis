#!/bin/bash

# Directory for Qdrant data
QDRANT_DATA_DIR="./data"

# Create data directory if it doesn't exist
mkdir -p $QDRANT_DATA_DIR

# Stop and remove existing container if it exists
docker stop qdrant 2>/dev/null || true
docker rm qdrant 2>/dev/null || true

# Run Qdrant container with mounted volume
docker run -d --name qdrant \
  -p 6333:6333 \
  -p 6334:6334 \
  -v "$(pwd)/$QDRANT_DATA_DIR:/qdrant/storage" \
  qdrant/qdrant

echo "Qdrant is running on port 6333 (API) and 6334 (Web UI)"
echo "Data is stored in $QDRANT_DATA_DIR"