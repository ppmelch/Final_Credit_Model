import mlflow

from backend.src.modeling.config import OPTUNA_SEARCH_SPACE
from backend.src.modeling.optuna_optimizer import OptunaOptimizer


class ModelBenchmark:

    def __init__(
        self,
        X_train,
        y_train,
        X_test,
        y_test
    ):

        self.X_train = X_train
        self.y_train = y_train

        self.X_test = X_test
        self.y_test = y_test

    def run(self):

        best_model = None
        best_score = -1

        models = [
            "random_forest",
            "xgboost",
            "lightgbm"
        ]

        mlflow.set_experiment(
            "Credit_Risk_Benchmark"
        )

        for model_name in models:

            with mlflow.start_run(run_name=model_name):

                optimizer = OptunaOptimizer(
                    model_name=model_name,
                    param_space=OPTUNA_SEARCH_SPACE[model_name],
                    X_train=self.X_train,
                    y_train=self.y_train,
                    X_test=self.X_test,
                    y_test=self.y_test
                )

                study = optimizer.optimize(
                    n_trials=30
                )

                score = study.best_value

                mlflow.log_metric(
                    "best_roc_auc",
                    score
                )

                if score > best_score:

                    best_score = score
                    best_model = model_name

        return best_model