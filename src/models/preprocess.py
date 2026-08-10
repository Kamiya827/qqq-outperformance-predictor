"""
Preprocessing utilities for machine learning models.
"""

import pandas as pd
from sklearn.preprocessing import StandardScaler

from src.dataset.builder import LABEL_COLUMN
from src.features.schema import FEATURE_COLUMNS


NON_FEATURE_COLUMNS = [
    "ticker",
    "timestamp",
    "forward_return_5d",
    "qqq_forward_return_5d",
    LABEL_COLUMN,
]


def prepare_features_and_labels(
    dataset: pd.DataFrame,
    feature_columns: list[str] | None = None,
) -> tuple[pd.DataFrame, pd.Series]:
    """
    Split a model-ready dataset into selected model features and target labels.
    """
    missing_columns = set(NON_FEATURE_COLUMNS) - set(dataset.columns)
    if missing_columns:
        raise ValueError(
            f"Dataset is missing required columns: {missing_columns}"
        )

    if feature_columns is None:
        feature_columns = FEATURE_COLUMNS

    missing_features = set(feature_columns) - set(dataset.columns)
    if missing_features:
        raise ValueError(
            f"Dataset is missing requested feature columns: {missing_features}"
        )

    X = dataset[feature_columns].copy()
    y = dataset[LABEL_COLUMN]

    return X, y


def standardize_features(
    X_train: pd.DataFrame,
    X_test: pd.DataFrame,
) -> tuple:
    """
    Fit a StandardScaler on training features and apply it to train and test data.
    """
    if list(X_train.columns) != list(X_test.columns):
        raise ValueError(
            "Training and testing feature columns must match."
        )

    scaler = StandardScaler()

    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    return X_train_scaled, X_test_scaled, scaler