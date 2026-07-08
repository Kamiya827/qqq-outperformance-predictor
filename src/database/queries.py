import pandas as pd

from src.database.connection import get_connection


def get_all_prices() -> pd.DataFrame:
    """
    Return all validated price records.
    """
    query = """
    SELECT
        ticker,
        timestamp,
        open,
        high,
        low,
        close,
        volume,
        trade_count,
        vwap
    FROM validated_prices
    ORDER BY ticker, timestamp;
    """

    with get_connection() as connection:
        return pd.read_sql_query(query, connection)


def get_prices_for_ticker(ticker: str) -> pd.DataFrame:
    """
    Return validated prices for one ticker.
    """
    query = """
    SELECT
        ticker,
        timestamp,
        open,
        high,
        low,
        close,
        volume,
        trade_count,
        vwap
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
    query = """
    SELECT
        ticker,
        timestamp,
        open,
        high,
        low,
        close,
        volume,
        trade_count,
        vwap
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