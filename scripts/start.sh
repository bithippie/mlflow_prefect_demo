#!/bin/bash

# Get the directory of this script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Set repo root as parent of scripts/
REPO_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$REPO_ROOT" || exit 1

echo "Working directory set to repo root: $REPO_ROOT"

NETWORK_NAME="mlflow-net"

echo "Checking for shared docker network '${NETWORK_NAME}'..."
if docker network inspect ${NETWORK_NAME} >/dev/null 2>&1; then
  echo "Docker network '${NETWORK_NAME}' already exists. Skipping creation."
else
  echo "Docker network '${NETWORK_NAME}' not found. Creating it..."
  docker network create ${NETWORK_NAME}
  if [ $? -eq 0 ]; then
    echo "Docker network '${NETWORK_NAME}' created successfully."
  else
    echo "Failed to create docker network '${NETWORK_NAME}'." >&2
    exit 1
  fi
fi

echo "Starting mlflow server..."
docker-compose -f mlflow-server/docker-compose.yml up -d

echo "Starting prefect orchestration..."
docker-compose -f prefect-orchestration/docker-compose.yml up -d

echo "Waiting 1 minute for services to initialize..."
sleep 30

echo "Starting business logic container..."
docker-compose -f business-logic/docker-compose.yml up --build