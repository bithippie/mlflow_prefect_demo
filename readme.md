# ✅ Step-by-step Instructions

# Setup
The `scripts/start.sh` script will:
1. Create the `mlflow-net` Docker network if it doesn't exist.
2. Build and start the MLflow, Prefect, and MinIO services using `docker-compose` on the shared network.
3. Wait for the MLflow and Prefect stacks to become available.
4. Run the example Python script (`business-logic/your_script.py`) which:
    - Logs parameters, 
    - Logs metrics, 
    - Creates an artifact (`artifact.txt`) to the MLflow server.

To run an end-to-end example:

```bash
sh scripts/start.sh
```

## View Results on the Web Services
| Service            | URL                                              | Notes                                |
|--------------------|--------------------------------------------------|--------------------------------------|
| **MLflow UI**      | [http://localhost:5001](http://localhost:5001)   |                                      |
| **Prefect UI**     | [http://localhost:4200](http://localhost:4200)   |                                      |
| **MinIO Console**  | [http://localhost:9001](http://localhost:9001)   | (login: `minioadmin` / `minioadmin`) |

# Tear Down

The `scripts/stop.sh` script will:
1. Stop and remove the MLflow, Prefect, and MinIO services started by `docker-compose`.
2. Remove the `mlflow-net` Docker network.

To stop and clean up the services:

```bash
sh scripts/stop.sh
```
