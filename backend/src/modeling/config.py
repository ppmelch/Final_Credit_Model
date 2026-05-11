"""
Configuration module for the credit risk modeling project.

This module centralizes:
- Hyperparameters for different machine learning models
- Project directory paths

This design allows easy modification of model settings and ensures
consistency across the pipeline.
"""

from pathlib import Path


MODEL_CONFIG = {
    "logistic": {
        "max_iter": 1000,
        "solver": "lbfgs",
        "class_weight": "balanced",
        "random_state": 42
    },

    "random_forest": {
        "n_estimators": 300,
        "max_depth": 5,
        "min_samples_leaf": 20,
        "min_samples_split": 40,
        "class_weight": "balanced",
        "random_state": 42,
        "n_jobs": -1
    },

    "xgboost": {
        "objective": "binary:logistic",
        "n_estimators": 250,
        "max_depth": 4,
        "learning_rate": 0.01,
        "subsample": 0.8,
        "colsample_bytree": 0.8,
        "min_child_weight": 10,
        "gamma": 1,
        "reg_alpha": 1,
        "reg_lambda": 2,
        "eval_metric": "logloss",
        "random_state": 42
    }, 
    
    "lightgbm": {
        "objective": "binary",
        "n_estimators": 300,
        "learning_rate": 0.01,
        "max_depth": 4,
        "num_leaves": 20,
        "subsample": 0.8,
        "colsample_bytree": 0.8,
        "reg_alpha": 2,
        "reg_lambda": 3,
        "class_weight": "balanced",
        "random_state": 42,
        "verbosity": -1
    }
}


OPTUNA_SEARCH_SPACE = {

    "logistic": {

        "C": {
            "type": "float",
            "low": 0.001,
            "high": 10
        }
    },

    "random_forest": {

        "n_estimators": {
            "type": "int",
            "low": 100,
            "high": 500
        },

        "max_depth": {
            "type": "int",
            "low": 3,
            "high": 15
        },

        "min_samples_split": {
            "type": "int",
            "low": 2,
            "high": 50
        },

        "min_samples_leaf": {
            "type": "int",
            "low": 1,
            "high": 20
        }
    },

    "xgboost": {

        "n_estimators": {
            "type": "int",
            "low": 100,
            "high": 500
        },

        "max_depth": {
            "type": "int",
            "low": 3,
            "high": 10
        },

        "learning_rate": {
            "type": "float",
            "low": 0.01,
            "high": 0.2
        },

        "subsample": {
            "type": "float",
            "low": 0.6,
            "high": 1.0
        },

        "colsample_bytree": {
            "type": "float",
            "low": 0.6,
            "high": 1.0
        },

        "min_child_weight": {
            "type": "int",
            "low": 1,
            "high": 15
        },

        "gamma": {
            "type": "float",
            "low": 0,
            "high": 5
        },

        "reg_alpha": {
            "type": "float",
            "low": 0,
            "high": 5
        },

        "reg_lambda": {
            "type": "float",
            "low": 0,
            "high": 10
        }
    },

    "lightgbm": {

        "n_estimators": {
            "type": "int",
            "low": 100,
            "high": 500
        },

        "learning_rate": {
            "type": "float",
            "low": 0.01,
            "high": 0.2
        },

        "max_depth": {
            "type": "int",
            "low": 3,
            "high": 10
        },

        "num_leaves": {
            "type": "int",
            "low": 20,
            "high": 100
        },

        "subsample": {
            "type": "float",
            "low": 0.6,
            "high": 1.0
        },

        "colsample_bytree": {
            "type": "float",
            "low": 0.6,
            "high": 1.0
        },

        "reg_alpha": {
            "type": "float",
            "low": 0,
            "high": 5
        },

        "reg_lambda": {
            "type": "float",
            "low": 0,
            "high": 10
        }
    }
}

# Root directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent

# Directory where trained models are stored
MODELS_DIR = BASE_DIR / "models"