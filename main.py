import pandas as pd
from backend.src.pipeline import CreditPipeline
from backend.src.utils.prints import PrintUtils
from backend.src.visualization.viz import Visualization
from backend.src.modeling.experiment_runner import ExperimentRunner


def main():
    """
    Execute the complete credit risk modeling workflow.

    Workflow
    --------
    1. Load the dataset
    2. Run benchmarking and hyperparameter optimization
    3. Select the best-performing model
    4. Execute the final credit risk pipeline
    5. Display evaluation results
    6. Export dashboard visualization data
    7. Save final processed dataset

    Notes
    -----
    - Benchmarking is performed using MLflow and Optuna.
    - Multiple machine learning models are compared automatically.
    - The best model is selected using ROC-AUC performance.
    - The final pipeline includes:
        * Probability of Default estimation
        * Expected Loss computation
        * Business decision logic
        * Risk segmentation
        * Interest rate estimation
        * Geospatial risk analysis
    """

    # 1. Load dataset
    data = pd.read_csv("data/dataset_modelado_final.csv")

    # 2. Benchmark + MLflow + Optuna
    runner = ExperimentRunner(data=data)

    best_model = runner.run()

    # 3. Final pipeline using best model
    pipeline = CreditPipeline(data=data, model_name=best_model)

    # 4. Run pipeline
    results, data_final = pipeline.run()

    # 5. Print results
    printer = PrintUtils(data_final)

    printer.print_all(results)

    # 6. Export dashboard data
    viz = Visualization()

    viz.export_dashboard_data(results, data_final)

    # 7. Save final dataset
    data_final.to_csv("data/results.csv", index=False)


if __name__ == "__main__":
    main()
