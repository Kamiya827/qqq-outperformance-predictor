"""
Utilities for loading stock universe files.
"""

from pathlib import Path

import pandas as pd

from src.config import settings


def load_universe(file_path: Path | None = None) -> pd.DataFrame:
    """
    Load the stock universe CSV.

    Args:
        file_path: Optional custom path to a universe CSV.

    Returns:
        A DataFrame containing ticker, name, and sector columns.
    """
    if file_path is None:
        file_path = settings.project_root / "data" / "external" / "starter_universe.csv"

    universe = pd.read_csv(file_path)

    required_columns = {"ticker", "name", "sector"}
    missing_columns = required_columns - set(universe.columns)

    if missing_columns:
        raise ValueError(f"Universe file is missing columns: {missing_columns}")

    universe["ticker"] = universe["ticker"].str.upper().str.strip()

    return universe


def get_tickers(include_benchmark: bool = True) -> list[str]:
    """
    Return the list of tickers from the universe.

    Args:
        include_benchmark: Whether to include QQQ in the returned ticker list.

    Returns:
        A list of ticker symbols.
    """
    universe = load_universe()

    if not include_benchmark:
        universe = universe[universe["sector"] != "Benchmark"]

    return universe["ticker"].tolist()