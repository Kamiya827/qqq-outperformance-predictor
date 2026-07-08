"""
Technical feature calculations for historical market data.

All functions assume input data is sorted by ticker and timestamp.
Features must only use information available at or before each timestamp.
"""

import pandas as pd


def add_return_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add return-based features.
    """
    features = df.copy()

    features["return_1d"] = features.groupby("ticker")["close"].pct_change(1)
    features["return_5d"] = features.groupby("ticker")["close"].pct_change(5)

    return features


def add_moving_average_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add moving average features.
    """
    features = df.copy()

    features["sma_20"] = (
        features.groupby("ticker")["close"]
        .transform(lambda x: x.rolling(window=20).mean())
    )

    features["sma_50"] = (
        features.groupby("ticker")["close"]
        .transform(lambda x: x.rolling(window=50).mean())
    )

    features["ema_20"] = (
        features.groupby("ticker")["close"]
        .transform(lambda x: x.ewm(span=20, adjust=False).mean())
    )

    return features


def add_volatility_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add rolling volatility features.
    """
    features = df.copy()

    features["volatility_20"] = (
        features.groupby("ticker")["return_1d"]
        .transform(lambda x: x.rolling(window=20).std())
    )

    return features


def add_volume_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add volume-based features.
    """
    features = df.copy()

    rolling_volume_20 = (
        features.groupby("ticker")["volume"]
        .transform(lambda x: x.rolling(window=20).mean())
    )

    features["volume_ratio_20"] = features["volume"] / rolling_volume_20

    return features


def build_technical_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Build the initial technical feature set.

    Parameters
    ----------
    df : pd.DataFrame
        Validated OHLCV price data.

    Returns
    -------
    pd.DataFrame
        DataFrame containing ticker, timestamp, and engineered features.
    """
    features = df.copy()

    features["timestamp"] = pd.to_datetime(features["timestamp"])
    features = features.sort_values(["ticker", "timestamp"]).reset_index(drop=True)

    features = add_return_features(features)
    features = add_moving_average_features(features)
    features = add_volatility_features(features)
    features = add_volume_features(features)

    feature_columns = [
        "ticker",
        "timestamp",
        "return_1d",
        "return_5d",
        "sma_20",
        "sma_50",
        "ema_20",
        "volatility_20",
        "volume_ratio_20",
    ]

    return features[feature_columns]