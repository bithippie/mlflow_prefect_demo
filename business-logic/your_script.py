
from prefect import flow, task
import mlflow
import os
from datetime import datetime

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

        with open("artifact.txt", "w") as f:
            f.write("Prefect-run artifact!")
        mlflow.log_artifact("artifact.txt")

@flow(flow_run_name=RUN_NAME)
def training_flow():
    train()

if __name__ == "__main__":
    training_flow()
