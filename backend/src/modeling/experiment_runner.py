import mlflow
import optuna
from backend.src.pipeline import CreditPipeline
from backend.src.modeling.config import OPTUNA_SEARCH_SPACE, MODEL_CONFIG


class ExperimentRunner:

    def __init__(self, data, model_names=None):
        self.data = data
        self.model_names = model_names or ["logistic", "random_forest", "xgboost", "lightgbm"]

    def _get_next_version(self, experiment_id):
        runs = mlflow.search_runs(experiment_ids=[experiment_id])

        if runs.empty:
            return 1

        return len(runs) + 1

    def optimize_model(self, model_name):

        def objective(trial):

            params = {}

            search_space = OPTUNA_SEARCH_SPACE.get(model_name, {})

            for param_name, config in search_space.items():

                if config["type"] == "int":
                    params[param_name] = trial.suggest_int(param_name, config["low"], config["high"])

                elif config["type"] == "float":
                    params[param_name] = trial.suggest_float(param_name, config["low"], config["high"])

            MODEL_CONFIG[model_name].update(params)
            
            pipeline = CreditPipeline(
                data=self.data.copy(),
                model_name=model_name
            )

            output = pipeline.train_and_evaluate()

            results = output["results"]

            return results["test_roc_auc"]
            

        study = optuna.create_study(direction="maximize")

        study.optimize(objective, n_trials=10)

        return study.best_params

    def run(self):

        mlflow.set_tracking_uri("file:./mlruns")

        experiment = mlflow.set_experiment("EXPERIMENTOS")

        best_model = None
        best_score = -1

        for model_name in self.model_names:

            best_params = self.optimize_model(model_name)

            MODEL_CONFIG[model_name].update(best_params)

            version = self._get_next_version(experiment.experiment_id)

            run_name = f"{model_name}_v{version}"

            print(f"\nRunning: {run_name}")

            with mlflow.start_run(experiment_id=experiment.experiment_id, run_name=run_name):

                mlflow.set_tags({
                    "model_type": model_name,
                    "project": "Credit Risk Model",
                    "stage": "benchmarking"
                })

                pipeline = CreditPipeline(data=self.data.copy(), model_name=model_name)

                results, _ = pipeline.run()

                score = results["test_roc_auc"]

                mlflow.log_param("model_name", model_name)

                mlflow.log_params(best_params)

                mlflow.log_metric("test_roc_auc", score)

                mlflow.log_metric("test_f1_score", results["test_f1_score"])

                mlflow.log_metric("test_precision", results["test_precision"])

                mlflow.log_metric("test_recall", results["test_recall"])

                mlflow.log_metric("optimal_threshold", results["optimal_threshold"])

                print(f"{model_name}: {score:.4f}")

                if score > best_score:
                    best_score = score
                    best_model = model_name

        print(f"\nBest Model: {best_model}")

        print(f"Best ROC-AUC: {best_score:.4f}")

        return best_model