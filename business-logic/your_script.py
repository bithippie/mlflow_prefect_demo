
import mlflow
import os

# Log to remote MLflow server
mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI"))

# Optional: Set experiment
mlflow.set_experiment("hello-world-experiment")

with mlflow.start_run():
    # Log parameters
    mlflow.log_param("param1", 5)

    # Log a metric
    mlflow.log_metric("accuracy", 0.89)

    # Log an artifact (e.g., a text file)
    with open("output.txt", "w") as f:
        f.write("Hello, world!")

    mlflow.log_artifact("output.txt")

    print("Run complete and logged to MLflow.")
