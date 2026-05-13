import pandas as pd
from backend.src.pipeline import CreditPipeline
from backend.src.utils.prints import PrintUtils
from backend.src.visualization.viz import Visualization
from backend.src.modeling.experiment_runner import ExperimentRunner

RUN_BENCHMARK = False

MODEL_VERSION = "logistic_v1"

def main():
    """
    Execute the complete credit risk modeling workflow.

    Workflow
    --------
    1. Load the dataset
    2. Optionally run benchmarking and hyperparameter optimization
    3. Load the selected trained model version
    4. Execute the final credit risk pipeline
    5. Display evaluation results
    6. Export dashboard visualization data
    7. Save final processed dataset

    Notes
    -----
    - Benchmarking is performed using MLflow and Optuna.
    - Multiple machine learning models can be compared automatically.
    - The selected model version is loaded directly from MLflow artifacts.
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

    # 2. Optional benchmarking
    if RUN_BENCHMARK:

        runner = ExperimentRunner(data=data)

        runner.run()

    # 3. Load selected model version
    pipeline = CreditPipeline(data=data, model_version=MODEL_VERSION)

    # 4. Run pipeline
    results, data_final , _= pipeline.run()

    # 5. Print results
    printer = PrintUtils(data_final)

    printer.print_all(results)

    # 6. Export dashboard data
    viz = Visualization()
    
    viz.plot_all(results, data_final)

    viz.export_dashboard_data(results, data_final)

    # 7. Save final dataset
    data_final.to_csv("data/results.csv", index=False)

if __name__ == "__main__":
    main()