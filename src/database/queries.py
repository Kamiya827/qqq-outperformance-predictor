import pandas as pd

from src.database.connection import get_connection


PRICE_COLUMNS = [
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

FEATURE_COLUMNS = [
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


def _select_columns(columns: list[str]) -> str:
    return ",\n        ".join(columns)


def get_all_prices() -> pd.DataFrame:
    """
    Return all validated price records.
    """
    query = f"""
    SELECT
        {_select_columns(PRICE_COLUMNS)}
    FROM validated_prices
    ORDER BY ticker, timestamp;
    """

    with get_connection() as connection:
        return pd.read_sql_query(query, connection)


def get_prices_for_ticker(ticker: str) -> pd.DataFrame:
    """
    Return validated prices for one ticker.
    """
    query = f"""
    SELECT
        {_select_columns(PRICE_COLUMNS)}
    FROM validated_prices
    WHERE ticker = ?
    ORDER BY timestamp;
    """

    with get_connection() as connection:
        return pd.read_sql_query(query, connection, params=(ticker.upper(),))


def get_price_history(
    ticker: str,
    start_date: str,
    end_date: str,
) -> pd.DataFrame:
    """
    Return validated prices for one ticker within a date range.

    Dates should be passed as strings in YYYY-MM-DD format.
    """
    query = f"""
    SELECT
        {_select_columns(PRICE_COLUMNS)}
    FROM validated_prices
    WHERE ticker = ?
      AND timestamp >= ?
      AND timestamp <= ?
    ORDER BY timestamp;
    """

    with get_connection() as connection:
        return pd.read_sql_query(
            query,
            connection,
            params=(ticker.upper(), start_date, end_date),
        )


def list_available_tickers() -> list[str]:
    """
    Return all tickers available in the validated_prices table.
    """
    query = """
    SELECT DISTINCT ticker
    FROM validated_prices
    ORDER BY ticker;
    """

    with get_connection() as connection:
        result = connection.execute(query).fetchall()

    return [row[0] for row in result]


def get_all_features() -> pd.DataFrame:
    """
    Return all engineered feature records.
    """
    query = f"""
    SELECT
        {_select_columns(FEATURE_COLUMNS)}
    FROM features
    ORDER BY ticker, timestamp;
    """

    with get_connection() as connection:
        return pd.read_sql_query(query, connection)


def get_features_for_ticker(ticker: str) -> pd.DataFrame:
    """
    Return engineered features for one ticker.
    """
    query = f"""
    SELECT
        {_select_columns(FEATURE_COLUMNS)}
    FROM features
    WHERE ticker = ?
    ORDER BY timestamp;
    """

    with get_connection() as connection:
        return pd.read_sql_query(query, connection, params=(ticker.upper(),))