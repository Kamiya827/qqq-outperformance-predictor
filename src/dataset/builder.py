"""
Build model-ready training datasets from engineered features and labels.
"""

import pandas as pd

from src.database.queries import get_all_features, get_all_labels
from src.features.schema import FEATURE_COLUMNS

IDENTIFIER_COLUMNS = ["ticker", "timestamp"]

FEATURE_COLUMNS = [
    "return_1d",
    "return_5d",
    "sma_20",
    "sma_50",
    "ema_20",
    "volatility_20",
    "volume_ratio_20",
]

LABEL_COLUMN = "outperformed_qqq"

def build_training_dataset(
        benchmark_ticker: str = "QQQ",
        drop_missing_labels: bool = True,
        drop_missing_features: bool = True
) -> pd.DataFrame:
    """
    Join engineered features with supervised learning labels.

    Parameters
    ----------
    benchmark_ticker : str
        Benchmark security to exclude from model-training observations.
    drop_missing_labels : bool
        Whether to remove rows where the label is missing.
    drop_missing_features : bool
        Whether to remove rows with incomplete engineered features.

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
        on = IDENTIFIER_COLUMNS,
        how = "inner",
        validate = "one_to_one"
    )

    dataset = dataset[
        dataset["ticker"].str.upper() != benchmark_ticker.upper()
    ].copy()

    if drop_missing_labels:
        dataset = dataset.dropna(subset=[LABEL_COLUMN])

    if drop_missing_features:
        dataset = dataset.dropna(subset = FEATURE_COLUMNS)

    if not dataset[LABEL_COLUMN].isna().any():
        dataset[LABEL_COLUMN] = dataset[LABEL_COLUMN].astype(int)

    dataset = dataset.sort_values(["ticker", "timestamp"]).reset_index(drop=True)

    return dataset