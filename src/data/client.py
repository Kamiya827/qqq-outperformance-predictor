"""
Factory for creating authenticated Alpaca clients.
"""

from alpaca.data.historical import StockHistoricalDataClient

from src.config import settings


def get_client() -> StockHistoricalDataClient:
    """
    Create and return an authenticated Alpaca historical data client.
    """
    return StockHistoricalDataClient(
        api_key=settings.alpaca_api_key,
        secret_key=settings.alpaca_secret_key,
    )