"""
Utilities for chronological train/test splits.
"""

import pandas as pd
from sklearn.model_selection import TimeSeriesSplit

def time_series_split(
    dataset: pd.DataFrame,
    train_fraction: float = 0.80,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Split a dataset chronologically into train and test sets using unique trading timestamps.

    Parameters
    ----------
    dataset : pd.DataFrame
        Model-ready dataset containing ticker and timestamp columns.
    train_fraction : float
        Fraction of unique timestamps assigned to the training set.

    Returns
    -------
    tuple[pd.DataFrame, pd.DataFrame]
        Chronologically ordered training and testing datasets.
    """
    if dataset.empty:
        raise ValueError("Dataset is empty.")

    if "timestamp" not in dataset.columns:
        raise ValueError("Dataset must contain a timestamp column.")

    if "ticker" not in dataset.columns:
        raise ValueError("Dataset must contain a ticker column.")

    if not 0 < train_fraction < 1:
        raise ValueError("train_fraction must be between 0 and 1.")

    data = dataset.copy()
    data["timestamp"] = pd.to_datetime(data["timestamp"])
    data = data.sort_values(["timestamp", "ticker"]).reset_index(drop=True)

    timestamps = data["timestamp"].drop_duplicates().sort_values().reset_index(drop=True)

    split_index = int(len(timestamps) * train_fraction)

    if split_index <= 0 or split_index >= len(timestamps):
        raise ValueError(
            "train_fraction produces an invalid train/test split."
        )

    train_timestamps = timestamps.iloc[:split_index]
    test_timestamps = timestamps.iloc[split_index:]

    train = data[data["timestamp"].isin(train_timestamps)].copy()

    test = data[data["timestamp"].isin(test_timestamps)].copy()

    return (
        train.reset_index(drop=True),
        test.reset_index(drop=True),
    )

def time_series_cross_validation(
    dataset: pd.DataFrame,
    n_splits: int = 5,
    gap: int = 5,
):
    """
    Generate chronological train/validation folds.

    Parameters
    ----------
    dataset : pd.DataFrame
        Model-ready dataset.
    n_splits : int
        Number of chronological validation folds.
    gap : int
        Number of timestamps excluded between training and validation.

    Yields
    ------
    tuple[pd.DataFrame, pd.DataFrame]
        Training and validation datasets for each fold.
    """
    if dataset.empty:
        raise ValueError("Dataset is empty.")

    if "timestamp" not in dataset.columns:
        raise ValueError("Dataset must contain a timestamp column.")

    data = dataset.copy()
    data["timestamp"] = pd.to_datetime(data["timestamp"])
    data = data.sort_values(["timestamp", "ticker"]).reset_index(drop=True)

    timestamps = data["timestamp"].drop_duplicates().sort_values().reset_index(drop=True)

    splitter = TimeSeriesSplit(
        n_splits=n_splits,
        gap=gap,
    )

    for train_indices, validation_indices in splitter.split(timestamps):
        train_timestamps = timestamps.iloc[train_indices]
        validation_timestamps = timestamps.iloc[validation_indices]

        train = data[data["timestamp"].isin(train_timestamps)].copy()
        validation = data[data["timestamp"].isin(validation_timestamps)].copy()

        yield (
            train.reset_index(drop=True),
            validation.reset_index(drop=True),
        )