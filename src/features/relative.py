"""
Benchmark-relative feature calculations.
"""

import pandas as pd


def add_benchmark_relative_features(
    features: pd.DataFrame,
    benchmark_ticker: str = "QQQ",
) -> pd.DataFrame:
    """
    Add features measuring each ticker relative to a benchmark.

    Parameters
    ----------
    features : pd.DataFrame
        Engineered feature dataset containing ticker, timestamp,
        return, and volatility features.
    benchmark_ticker : str
        Benchmark ticker used for relative comparisons.

    Returns
    -------
    pd.DataFrame
        Feature dataset with benchmark-relative features added.
    """
    required_columns = {
        "ticker",
        "timestamp",
        "return_1d",
        "return_5d",
        "volatility_20",
    }

    missing_columns = required_columns - set(features.columns)
    if missing_columns:
        raise ValueError(
            f"Missing required columns for benchmark-relative features: "
            f"{missing_columns}"
        )

    data = features.copy()

    benchmark = data[
        data["ticker"].str.upper() == benchmark_ticker.upper()
    ][
        [
            "timestamp",
            "return_1d",
            "return_5d",
            "volatility_20",
        ]
    ].rename(
        columns={
            "return_1d": "benchmark_return_1d",
            "return_5d": "benchmark_return_5d",
            "volatility_20": "benchmark_volatility_20",
        }
    )

    if benchmark.empty:
        raise ValueError(
            f"Benchmark ticker {benchmark_ticker} was not found in feature data."
        )

    data = data.merge(
        benchmark,
        on="timestamp",
        how="left",
        validate="many_to_one",
    )

    data["relative_return_1d"] = (
        data["return_1d"] - data["benchmark_return_1d"]
    )

    data["relative_return_5d"] = (
        data["return_5d"] - data["benchmark_return_5d"]
    )

    data["relative_volatility_20"] = (
        data["volatility_20"] / data["benchmark_volatility_20"]
    )

    data = data.drop(
        columns=[
            "benchmark_return_1d",
            "benchmark_return_5d",
            "benchmark_volatility_20",
        ]
    )

    return data