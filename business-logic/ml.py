import os
from datetime import datetime

from prefect import flow, task
import mlflow
import optuna
from optuna_integration import MLflowCallback
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.datasets import make_classification # for sample data

RUN_NAME = f"ml-{datetime.now().strftime('%Y%m%d-%H%M%S')}"

mlflow.autolog()

@task()
def train():
    with mlflow.start_run(run_name=RUN_NAME, nested=True) as run:
      # 1. Generate sample data (replace with your actual data)
      X, y = make_classification(n_samples=1000, n_features=20, random_state=42)

      # 2. Split data into training and testing sets
      X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

      mlflow_callback = MLflowCallback(
          tracking_uri=os.getenv("MLFLOW_TRACKING_URI"),
          metric_name="accuracy",
          create_experiment=True,
          mlflow_kwargs={
              "experiment_id": 'ml.py'
          }
      )


      clf = SVC(gamma='auto')
      param_distributions = {
          "C": optuna.distributions.FloatDistribution(1e-10, 1e10, log=True),
          "degree": optuna.distributions.IntDistribution(1, 5),
      }

      # @mlflc.track_in_mlflow()
      # def objective(trial):
      #     x = trial.suggest_float("x", -10, 10)
      #     mlflow.log_param("power", 2)
      #     mlflow.log_metric("base of metric", x - 2)

      #     return (x - 2) ** 2



      optuna_search = optuna.integration.OptunaSearchCV(
          clf, param_distributions, n_trials=100, timeout=600, verbose=2, callbacks=[mlflow_callback]
      )

      optuna_search = optuna.integration.OptunaSearchCV(
          clf,
          param_distributions
          
      )
      optuna_search.fit(X, y)
      y_pred = optuna_search.predict(X)



@flow(flow_run_name=RUN_NAME)
def training_flow():
    mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI"))
    mlflow.set_experiment("mlflow-optuna-example")

    train()

if __name__ == "__main__":
    training_flow()