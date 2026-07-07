import pandas as pd

from src.config import settings
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


def load_validated_prices() -> int:
    """
    Load validated market price data from CSV into SQLite.

    Returns
    -------
    int
        Number of rows loaded into the validated_prices table.
    """

    file_path = settings.project_root / "data" / "interim" / "daily_bars_validated.csv"

    if not file_path.exists():
        raise FileNotFoundError(f"Validated price file not found: {file_path}")

    df = pd.read_csv(file_path)

    missing_columns = REQUIRED_COLUMNS - set(df.columns)
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    optional_columns = ["trade_count", "vwap"]
    for column in optional_columns:
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