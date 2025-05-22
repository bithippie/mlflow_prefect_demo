# ✅ Step-by-step Instructions

## 1. Create the Shared Network

```bash
docker network create mlflow-net
```

This ensures that both `mlflow-server` and `business-logic` can talk to each other.

## 2. Start the MLflow Server

```bash
cd mlflow-server
docker-compose up -d
```

This will spin up:

- **MLflow UI:** [http://localhost:5000](http://localhost:5000)
- **MinIO console (optional):** [http://localhost:9001](http://localhost:9001)  
  (login: `minioadmin` / `minioadmin`)

## 4. Run the Business Logic

```bash
cd ../business-logic
docker-compose up --build
```

This will:

- Run a single Python script
- Log parameters, metrics, and an artifact (`output.txt`) to the MLflow server

You should see a message like:

```
Run complete and logged to MLflow.
```

## 5. Check the MLflow UI

Visit [http://localhost:5000](http://localhost:5000)

You’ll see an experiment named `hello-world-experiment` with:

- `param1 = 5`
- `accuracy = 0.89`
- `output.txt` as an artifact

## 6. Optional Cleanup

```bash
docker-compose down
docker network rm mlflow-net
```
