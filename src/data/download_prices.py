"""
Download historical daily stock price data from Alpaca.
"""

from datetime import datetime

import pandas as pd
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame

from src.config import settings
from src.data.client import get_client


def download_daily_bars(
    tickers: list[str],
    start: datetime,
    end: datetime,
) -> pd.DataFrame:
    """
    Download daily OHLCV bars for a list of tickers.

    Args:
        tickers: Stock symbols to download.
        start: Start datetime.
        end: End datetime.

    Returns:
        DataFrame of historical daily price bars.
    """
    client = get_client()

    request = StockBarsRequest(
        symbol_or_symbols=tickers,
        timeframe=TimeFrame.Day,
        start=start,
        end=end,
    )

    bars = client.get_stock_bars(request)
    data = bars.df.reset_index()

    return data


if __name__ == "__main__":
    tickers = ["AAPL", "QQQ"]

    data = download_daily_bars(
        tickers=tickers,
        start=datetime(2022, 1, 1),
        end=datetime(2025, 12, 31),
    )

    output_path = settings.raw_data_dir / "daily_bars_starter.csv"
    data.to_csv(output_path, index=False)

    print(f"Saved {len(data):,} rows to {output_path}")