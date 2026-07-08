"""
Build engineered features from validated market data.
"""

import pandas as pd

from src.database.queries import get_all_prices
from src.features.technical import build_technical_features


def build_features() -> pd.DataFrame:
    """
    Build the full feature dataset from validated prices.

    Returns
    -------
    pd.DataFrame
        Engineered feature dataset.
    """

    prices = get_all_prices()

    if prices.empty:
        raise ValueError("No validated prices found. Load price data before building features.")

    features = build_technical_features(prices)

    return features