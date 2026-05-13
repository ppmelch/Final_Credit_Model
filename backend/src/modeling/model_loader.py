import joblib
from pathlib import Path

from backend.src.modeling.config import MODELS_DIR


class ModelLoader:
    '''
    Utility class for loading trained machine learning models
    and their associated evaluation metrics.
    '''

    @staticmethod
    def load_model(model_version):
        '''
        Load a trained model version and metrics from disk.

        Parameters
        ----------
        model_version : str
            Name of the saved model version.

        Returns
        -------
        tuple
            model : object
                Loaded trained model.

            results : dict
                Stored evaluation metrics.
        '''

        model_path = MODELS_DIR / f"{model_version}.pkl"

        metrics_path = MODELS_DIR / f"{model_version}_metrics.pkl"

        if not Path(model_path).exists():

            raise FileNotFoundError(
                f"Model version '{model_version}' does not exist."
            )

        model = joblib.load(model_path)

        results = joblib.load(metrics_path)

        return model, results