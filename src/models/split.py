"""
Utilities for chronological train/test splits.
"""

import pandas as pd


def time_series_split(
    dataset: pd.DataFrame,
    train_fraction: float = 0.80,
):
    """
    Split a dataset chronologically into train and test sets.

    Parameters
    ----------
    dataset : pd.DataFrame
        Model-ready dataset sorted by timestamp.
    train_fraction : float
        Fraction of observations assigned to the training set.

    Returns
    -------
    train : pd.DataFrame
    test : pd.DataFrame
    """
    if dataset.empty:
        raise ValueError("Dataset is empty.")

    if not 0 < train_fraction < 1:
        raise ValueError("train_fraction must be between 0 and 1.")

    dataset = dataset.sort_values("timestamp").reset_index(drop=True)

    split_index = int(len(dataset) * train_fraction)

    train = dataset.iloc[:split_index].copy()
    test = dataset.iloc[split_index:].copy()

    return train, test