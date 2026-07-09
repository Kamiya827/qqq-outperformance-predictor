"""
Build model-ready training datasets from engineered features and labels.
"""

import pandas as pd

from src.database.queries import get_all_features, get_all_labels


def build_training_dataset(drop_missing_labels: bool = True) -> pd.DataFrame:
    """
    Join engineered features with supervised learning labels.

    Parameters
    ----------
    drop_missing_labels : bool
        Whether to remove rows where the label is missing.

    Returns
    -------
    pd.DataFrame
        Model-ready dataset.
    """

    features = get_all_features()
    labels = get_all_labels()

    if features.empty:
        raise ValueError("No features found. Generate features before building dataset.")

    if labels.empty:
        raise ValueError("No labels found. Generate labels before building dataset.")

    dataset = features.merge(
        labels,
        on=["ticker", "timestamp"],
        how="inner",
    )

    if drop_missing_labels:
        dataset = dataset.dropna(subset=["outperformed_qqq"])

    dataset = dataset.sort_values(["ticker", "timestamp"]).reset_index(drop=True)

    return dataset