import optuna
import mlflow

from backend.src.modeling.model import Model
from backend.src.modeling.model_evaluation import ModelEvaluation


class OptunaOptimizer:

    def __init__(
        self,
        model_name,
        param_space,
        X_train,
        y_train,
        X_test,
        y_test
    ):

        self.model_name = model_name
        self.param_space = param_space

        self.X_train = X_train
        self.y_train = y_train

        self.X_test = X_test
        self.y_test = y_test

    def _sample_params(self, trial):

        params = {}

        for param_name, config in self.param_space.items():

            if config["type"] == "int":

                params[param_name] = trial.suggest_int(
                    param_name,
                    config["low"],
                    config["high"]
                )

            elif config["type"] == "float":

                params[param_name] = trial.suggest_float(
                    param_name,
                    config["low"],
                    config["high"]
                )

        return params

    def objective(self, trial):

        params = self._sample_params(trial)

        with mlflow.start_run(nested=True):

            model = Model.get_model(
                task_type="classification",
                model_name=self.model_name,
                y_train=self.y_train
            )

            model.model.set_params(**params)

            model.train(
                self.X_train,
                self.y_train
            )

            y_prob = model.predict_proba(self.X_test)

            y_pred = (y_prob >= 0.5).astype(int)

            evaluator = ModelEvaluation()

            results = evaluator.evaluate(
                self.y_test,
                y_pred,
                y_prob
            )

            mlflow.log_params(params)

            for metric_name, metric_value in results.items():

                if metric_name != "confusion_matrix":

                    mlflow.log_metric(
                        metric_name,
                        metric_value
                    )

            return results["roc_auc"]

    def optimize(self, n_trials=5):

        study = optuna.create_study(
            direction="maximize"
        )

        study.optimize(
            self.objective,
            n_trials=n_trials
        )

        return study