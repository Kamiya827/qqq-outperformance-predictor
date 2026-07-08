from pathlib import Path

import pandas as pd

from src.database.connection import get_connection


REQUIRED_COLUMNS = {
    "ticker",
    "timestamp",
    "open",
    "high",
    "low",
    "close",
    "volume",
}


def load_validated_prices(file_path: Path) -> int:
    """
    Load validated market price data from CSV into SQLite.
    """

    if not file_path.exists():
        raise FileNotFoundError(f"Validated price file not found: {file_path}")

    df = pd.read_csv(file_path)

    missing_columns = REQUIRED_COLUMNS - set(df.columns)
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    for column in ["trade_count", "vwap"]:
        if column not in df.columns:
            df[column] = None

    df = df[
        [
            "ticker",
            "timestamp",
            "open",
            "high",
            "low",
            "close",
            "volume",
            "trade_count",
            "vwap",
        ]
    ]

    rows = list(df.itertuples(index=False, name=None))

    insert_sql = """
    INSERT OR REPLACE INTO validated_prices (
        ticker,
        timestamp,
        open,
        high,
        low,
        close,
        volume,
        trade_count,
        vwap
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
    """

    with get_connection() as connection:
        connection.executemany(insert_sql, rows)
        connection.commit()

    return len(rows)

def load_features(features: pd.DataFrame) -> int:
    """
    Load engineered features into the SQLite features table.

    Parameters
    ----------
    features : pd.DataFrame
        Feature DataFrame containing ticker, timestamp, and feature columns.

    Returns
    -------
    int
        Number of feature rows loaded.
    """

    required_columns = {
        "ticker",
        "timestamp",
        "return_1d",
        "return_5d",
        "sma_20",
        "sma_50",
        "ema_20",
        "volatility_20",
        "volume_ratio_20",
    }

    missing_columns = required_columns - set(features.columns)
    if missing_columns:
        raise ValueError(f"Missing required feature columns: {missing_columns}")

    feature_data = features[
        [
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
    ].copy()

    feature_data["timestamp"] = feature_data["timestamp"].astype(str)

    rows = list(feature_data.itertuples(index=False, name=None))

    insert_sql = """
    INSERT OR REPLACE INTO features (
        ticker,
        timestamp,
        return_1d,
        return_5d,
        sma_20,
        sma_50,
        ema_20,
        volatility_20,
        volume_ratio_20
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
    """

    with get_connection() as connection:
        connection.executemany(insert_sql, rows)
        connection.commit()

    return len(rows)