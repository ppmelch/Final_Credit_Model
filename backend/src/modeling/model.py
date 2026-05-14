from backend.src.modeling.classification_model import ClassificationModel
from backend.src.modeling.config import MODEL_CONFIG
from backend.src.utils.utils import compute_scale_pos_weight


class Model:
    """
    Factory class for initializing machine learning models.

    This class centralizes model creation and configuration
    management, allowing different classification algorithms
    to be instantiated dynamically under a unified interface.

    Supported models include:
    - Logistic Regression
    - Random Forest
    - XGBoost
    - LightGBM
    """

    @staticmethod
    def get_model(task_type: str, model_name: str, y_train=None):
        """
        Return an initialized machine learning model.

        Parameters
        ----------
        task_type : str
            Type of machine learning task.

        model_name : str
            Name of the model to initialize.

        y_train : pd.Series, optional
            Training labels used for dynamic parameter
            computation in imbalanced classification tasks.

        Returns
        -------
        ClassificationModel
            Initialized classification model instance.

        Raises
        ------
        ValueError
            If the task type or model name is invalid.
        """

        if task_type == "classification":

            allowed_models = [
                "logistic",
                "random_forest",
                "xgboost",
                "lightgbm"
            ]

            if model_name not in allowed_models:

                raise ValueError(
                    f"Model '{model_name}' not supported"
                )

            model_config = MODEL_CONFIG[model_name].copy()

            # Dynamic runtime parameters
            if model_name == "xgboost" and y_train is not None:

                model_config["scale_pos_weight"] = (
                    compute_scale_pos_weight(y_train)
                )

            return ClassificationModel(
                model_name,
                **model_config
            )

        else:

            raise ValueError("Invalid model type")
