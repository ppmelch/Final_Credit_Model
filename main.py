import pandas as pd
from backend.src.pipeline import CreditPipeline
from backend.src.utils.prints import PrintUtils
from backend.src.visualization.viz import Visualization
from backend.src.modeling.experiment_runner import ExperimentRunner

RUN_BENCHMARK = False

MODEL_VERSION = "logistic_v2"  # random_forest_v2


def main():
    """
    Execute the end-to-end credit risk modeling pipeline.

    Workflow
    --------
    1. Load the final modeled dataset.
    2. Optionally run benchmarking and hyperparameter optimization.
    3. Load the selected trained model version.
    4. Execute the credit risk pipeline.
    5. Print evaluation metrics and MLflow experiment results.
    6. Export dashboard visualization data.
    7. Save the final processed dataset.

    The pipeline integrates:
    - Data preprocessing
    - Machine learning inference
    - Risk segmentation
    - Business logic
    - Expected loss estimation
    - Dashboard data generation

    Notes
    -----
    The selected model version is controlled through the
    MODEL_VERSION variable.

    If RUN_BENCHMARK is enabled, the system executes
    experimentation and model comparison before loading
    the final selected model.
    """
    # 1. Load dataset
    data = pd.read_csv("data/dataset_modelado_final.csv")

    # 2. Optional benchmarking
    if RUN_BENCHMARK:

        runner = ExperimentRunner(data=data)

        runner.run()

    # 3. Load selected model version
    pipeline = CreditPipeline(data=data, model_version=MODEL_VERSION)

    # 4. Run pipeline
    results, data_final, _ = pipeline.run()

    # 5. Print results
    printer = PrintUtils(data_final)

    printer.print_all(results)

    printer.print_mlflow_experiments()

    # 7. Export dashboard data
    viz = Visualization()

    # viz.plot_all(results, data_final)

    viz.export_dashboard_data(results, data_final)

    # 8. Save final dataset
    data_final.to_csv("data/results.csv", index=False)


if __name__ == "__main__":
    main()
