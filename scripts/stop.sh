#!/bin/bash

# Get the directory of this script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# Set repo root as parent of scripts/
REPO_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$REPO_ROOT" || exit 1

echo "Working directory set to repo root: $REPO_ROOT"

echo "Stopping mlflow server..."
docker-compose -f mlflow-server/docker-compose.yml down

echo "Stopping prefect orchestration..."
docker-compose -f prefect-orchestration/docker-compose.yml down

echo "Stopping business logic container..."
docker-compose -f business-logic/docker-compose.yml down

echo "Removing the network..."
docker network rm mlflow-net