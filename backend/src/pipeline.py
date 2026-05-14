from backend.src.modeling.model import Model
from backend.src.modeling.config import MODELS_DIR
from backend.src.data.data_splitter import DataSplitter
from backend.src.modeling.model_loader import ModelLoader
from backend.src.data.data_preparation import DataPreparation
from backend.src.modeling.business_logic import BusinessLogic
from backend.src.modeling.geospatial_risk import GeospatialRisk
from backend.src.modeling.risk_calculator import RiskCalculator
from backend.src.modeling.model_evaluation import ModelEvaluation
from backend.src.modeling.threshold_optimization import ThresholdOptimizer


class CreditPipeline:
    '''
    End-to-end pipeline for credit risk modeling.

    This pipeline automates:
    - Data preparation
    - Train-test split
    - Model training
    - Probability prediction
    - Threshold optimization
    - Model evaluation
    - Risk metric computation
    - Business decision logic
    - Geospatial risk analysis
    - Model persistence
    '''

    def __init__(self, data, model_name="random_forest", model_version=None):
        '''
        Initialize the credit risk pipeline.

        Parameters
        ----------
        data : pd.DataFrame
            Input dataset used for modeling.

        model_name : str, optional
            Machine learning model to use.
            Default is "random_forest".

        model_version : str, optional
            Saved model version to load from disk.
            If provided, training is skipped.
        '''

        self.data = data
        self.model_name = model_name
        self.model_version = model_version

    def train_and_evaluate(self):
        '''
        Train and evaluate the selected machine learning model.

        Workflow
        --------
        1. Data preparation
        2. Train-test split
        3. Model training
        4. Probability prediction
        5. Threshold optimization using Optuna
        6. Model evaluation

        Returns
        -------
        dict
            Dictionary containing:
            - results : evaluation metrics
            - model : trained model object
            - X : processed feature matrix
        '''

        prep = DataPreparation(self.data)

        X, y = prep.prepare_data()

        splitter = DataSplitter()

        X_train, X_test, y_train, y_test = splitter.split(X, y)

        model = Model.get_model(
            "classification",
            self.model_name,
            y_train=y_train
        )

        model.train(X_train, y_train)

        y_train_proba = model.predict_proba(X_train)

        y_train_pred = (y_train_proba >= 0.5).astype(int)

        y_test_proba = model.predict_proba(X_test)

        optimizer = ThresholdOptimizer(y_test, y_test_proba)

        best_threshold = optimizer.optimize_threshold()

        y_test_pred = (y_test_proba >= best_threshold).astype(int)

        evaluator = ModelEvaluation()

        results = evaluator.evaluate_full(
            y_train=y_train,
            y_train_pred=y_train_pred,
            y_train_proba=y_train_proba,
            y_test=y_test,
            y_test_pred=y_test_pred,
            y_test_proba=y_test_proba
        )

        results["optimal_threshold"] = best_threshold

        return {
            "results": results,
            "model": model,
            "X": X
        }

    def run(self):
        '''
        Execute the complete credit risk pipeline.

        Workflow
        --------
        1. Load a trained model version or train a new model
        2. Compute risk metrics
        3. Apply business decision logic
        4. Estimate interest rates
        5. Perform geospatial risk analysis

        Returns
        -------
        tuple
            results : dict
                Model evaluation metrics.

            self.data : pd.DataFrame
                Final enriched dataset including:
                - PD predictions
                - Expected loss
                - Credit decisions
                - Risk buckets
                - Interest rates

            model : object
                Trained machine learning model.
        '''

        prep = DataPreparation(self.data)

        X, y = prep.prepare_data()

        if self.model_version:

            model, results = ModelLoader.load_model(
                self.model_version
            )

        else:

            training_output = self.train_and_evaluate()

            results = training_output["results"]

            model = training_output["model"]

            X = training_output["X"]

        risk = RiskCalculator(lgd=0.45)

        pd_values = risk.calculate_pd(model, X)

        self.data["predicted_pd"] = pd_values

        ead = risk.calculate_ead(self.data)

        lgd = risk.calculate_lgd(self.data)

        self.data["expected_loss"] = risk.calculate_expected_loss(
            pd_values,
            lgd,
            ead
        )

        logic = BusinessLogic(
            threshold=results["optimal_threshold"],
            LGD=0.45,
            rf=0.069971,
            spread_fondeo=0.03,
            operating_cost=0.035,
            capital_cost=0.0189,
            profit_margin=0.015
        )

        self.data["decision"] = logic.credit_decision(pd_values)

        self.data["risk_bucket"] = logic.risk_buckets(pd_values)

        self.data["interest_rate_model"] = logic.calculate_interest_rate(
            pd_values)

        geo = GeospatialRisk()

        geo.build_municipality_risk(self.data)

        return results, self.data, model
