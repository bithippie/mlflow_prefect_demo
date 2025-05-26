
from prefect import flow, task
import mlflow
import os
from datetime import datetime
import tempfile

RUN_NAME = f"atorres-run-{datetime.now().strftime('%Y%m%d-%H%M%S')}"

@task()
def train():
    mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI"))
    mlflow.set_experiment("prefect-hello-world")

    with mlflow.start_run(run_name=RUN_NAME) as run:
        # Log parameters
        mlflow.log_param("param1", 5)

        # Log a metric
        mlflow.log_metric("accuracy", 0.89)
        
        # Create a temporary file
        with tempfile.NamedTemporaryFile("w", delete=False, suffix=".txt") as f:
            f.write("Prefect-run artifact!")
            temp_file_path = f.name

        # Log the artifact directly to MLflow (MLflow will handle S3 upload if configured)
        mlflow.log_artifact(temp_file_path)

@flow(flow_run_name=RUN_NAME)
def training_flow():
    train()

if __name__ == "__main__":
    training_flow()
