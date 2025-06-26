import os
from datetime import datetime

from prefect import flow, task
import mlflow

import numpy as np

import optuna
from optuna_integration import MLflowCallback

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import roc_auc_score, mean_squared_error, mean_absolute_error, r2_score
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.datasets import make_classification # for sample data

RUN_NAME = f"ml-{datetime.now().strftime('%Y%m%d-%H%M%S')}"

mlflow.autolog()

def train():  
    with mlflow.start_run(run_name=RUN_NAME) as parent_run:
      mlflc = MLflowCallback(
        metric_name="accuracy",
        mlflow_kwargs={
            "experiment_id": 'ml.py',
            "run_id": parent_run.info.run_id,
            "nested": True
        }
      )

      # 1. Generate sample data (replace with your actual data)
      X, y = make_classification(n_samples=1000, n_features=20, random_state=42)

      # 2. Split data into training and testing sets
      X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

      # 3. Create the pipeline
      # pipeline = Pipeline([
      #   ('scaler', StandardScaler()),       # Step 1: Scale the data
      #   ('rf_classifier', RandomForestClassifier(random_state=42)) # Step 2: Random Forest Classifier
      # ])

      @mlflc.track_in_mlflow()
      @task(log_prints=True)
      def objective(trial):
          n_estimators = trial.suggest_int("n_estimators", 10, 200, log=True)
          max_depth = trial.suggest_int("max_depth", 2, 32)
          min_samples_split = trial.suggest_int("min_samples_split", 2, 10)
          min_samples_leaf = trial.suggest_int("min_samples_leaf", 1, 10)

          # Create and fit random forest model
          model = RandomForestRegressor(
            n_estimators=n_estimators,
            max_depth=max_depth,
            min_samples_split=min_samples_split,
            min_samples_leaf=min_samples_leaf,
            random_state=42,
            verbose=10
          )
          
          model.fit(X_train, y_train)

          # Make predictions and calculate RMSE
          y_pred = model.predict(X_test)
          rmse = np.sqrt(mean_squared_error(y_test, y_pred))
          mae = mean_absolute_error(y_test, y_pred)
          r2 = r2_score(y_test, y_pred)

          if trial.number == 0:
              return 0/0
          # Return MAE
          return mae


      study = optuna.create_study(study_name="my_other_study")
      study.optimize(objective, n_trials=10, callbacks=[mlflc], catch=(Exception,))

      best_trial = study.best_trial
      best_params = best_trial.params

      # Refit the model with best_params on the full dataset or a larger validation set
      # Example with scikit-learn:
      model = RandomForestRegressor(**best_params)
      model.fit(X_train, y_train)

      mlflow.log_params(best_params)
      mlflow.sklearn.log_model(
          model, 
          input_example=X_train[[0]], 
          name="model"
      )
    

    # mlflow_callback = MLflowCallback(
    #     tracking_uri=os.getenv("MLFLOW_TRACKING_URI"),
    #     metric_name="accuracy",
    #     create_experiment=True,
    #     mlflow_kwargs={
    #         "experiment_id": 'ml.py'
    #     }
    # )


    #   clf = SVC(gamma='auto')
    #   param_distributions = {
    #       "C": optuna.distributions.FloatDistribution(1e-10, 1e10, log=True),
    #       "degree": optuna.distributions.IntDistribution(1, 5),
    #   }

    #   # @mlflc.track_in_mlflow()
    #   # def objective(trial):
    #   #     x = trial.suggest_float("x", -10, 10)
    #   #     mlflow.log_param("power", 2)
    #   #     mlflow.log_metric("base of metric", x - 2)

    #   #     return (x - 2) ** 2



    #   optuna_search = optuna.integration.OptunaSearchCV(
    #       clf, param_distributions, n_trials=100, timeout=600, verbose=2, callbacks=[mlflow_callback]
    #   )

    #   optuna_search = optuna.integration.OptunaSearchCV(
    #       clf,
    #       param_distributions
          
    #   )
    #   optuna_search.fit(X, y)
    #   y_pred = optuna_search.predict(X)



@flow(flow_run_name=RUN_NAME)
def training_flow():
    mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI"))
    mlflow.set_experiment("my_other_study")

    train()

if __name__ == "__main__":
    training_flow()