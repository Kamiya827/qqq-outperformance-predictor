"""
Reusable model evaluation with time-series cross-validation.
"""

from collections.abc import Callable

import pandas as pd

from src.evaluation.metrics import evaluate_binary_classifier
from src.models.preprocess import (
    prepare_features_and_labels,
    standardize_features,
)
from src.models.split import time_series_cross_validation


def cross_validate_model(
    dataset: pd.DataFrame,
    model_builder: Callable,
    model_name: str,
    feature_columns: list[str] | None = None,
    scale_features: bool = False,
    n_splits: int = 5,
    gap: int = 5,
) -> pd.DataFrame:
    """
    Evaluate a model across chronological cross-validation folds.

    Parameters
    ----------
    dataset : pd.DataFrame
        Model-ready training dataset.
    model_builder : Callable
        Function that returns a new unfitted model.
    model_name : str
        Human-readable model name.
    feature_columns: list[str] | None
        Feature columns to use for model training.
    scale_features : bool
        Whether feature standardization is required.
    n_splits : int
        Number of time-series cross-validation folds.
    gap : int
        Number of trading timestamps excluded between training and validation.

    Returns
    -------
    pd.DataFrame
        Evaluation metrics for every validation fold.
    """
    folds = time_series_cross_validation(
        dataset,
        n_splits=n_splits,
        gap=gap,
    )

    fold_results = []

    for fold_number, (train, validation) in enumerate(folds, start=1):
        X_train, y_train = prepare_features_and_labels(
             train,
             feature_columns = feature_columns
        )

        X_validation, y_validation = prepare_features_and_labels(
             validation,
             feature_columns=feature_columns
        )

        if scale_features:
            X_train, X_validation, _ = standardize_features(
                X_train,
                X_validation,
            )

        model = model_builder()
        model.fit(X_train, y_train)

        predictions = model.predict(X_validation)
        probabilities = model.predict_proba(X_validation)[:, 1]

        metrics = evaluate_binary_classifier(
            y_true=y_validation,
            y_pred=predictions,
            y_probability=probabilities,
        )

        metrics["fold"] = fold_number
        metrics["model"] = model_name

        fold_results.append(metrics)

    return pd.DataFrame(fold_results)

def summarize_cross_validation(
    results: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Summarize mean and standard deviation of cross-validation metrics.
        """
        metric_columns = [
            "accuracy",
            "precision",
            "recall",
            "f1_score",
            "roc_auc",
        ]

        return pd.DataFrame(
            {
                "mean": results[metric_columns].mean(),
                "std": results[metric_columns].std(),
            }
        )
    