"""
Generate supervised learning labels.

Labels use future returns and must remain separate from feature generation
to avoid lookahead bias.
"""

import pandas as pd


def build_outperformance_labels(
    prices: pd.DataFrame,
    benchmark_ticker: str = "QQQ",
    horizon: int = 5,
) -> pd.DataFrame:
    """
    Build labels indicating whether each ticker outperformed the benchmark.

    Parameters
    ----------
    prices : pd.DataFrame
        Validated price data with ticker, timestamp, and close columns.
    benchmark_ticker : str
        Benchmark ticker to compare against.
    horizon : int
        Forward return horizon in trading days.

    Returns
    -------
    pd.DataFrame
        Label dataset.
    """
    required_columns = {"ticker", "timestamp", "close"}
    missing_columns = required_columns - set(prices.columns)
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    data = prices.copy()
    data["timestamp"] = pd.to_datetime(data["timestamp"])
    data = data.sort_values(["ticker", "timestamp"]).reset_index(drop=True)

    data["forward_return_5d"] = (
        data.groupby("ticker")["close"].shift(-horizon) / data["close"] - 1
    )

    benchmark = data[data["ticker"] == benchmark_ticker][
        ["timestamp", "forward_return_5d"]
    ].rename(columns={"forward_return_5d": "qqq_forward_return_5d"})

    labels = data.merge(benchmark, on="timestamp", how="left")

    labels["outperformed_qqq"] = (
    labels["forward_return_5d"] > labels["qqq_forward_return_5d"]
    ).astype("Int64")

    missing_label_mask = (
    labels["forward_return_5d"].isna()
    | labels["qqq_forward_return_5d"].isna()
    )

    labels.loc[missing_label_mask, "outperformed_qqq"] = pd.NA

    labels = labels[
        [
            "ticker",
            "timestamp",
            "forward_return_5d",
            "qqq_forward_return_5d",
            "outperformed_qqq",
        ]
    ]

    return labels