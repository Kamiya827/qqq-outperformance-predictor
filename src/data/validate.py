"""
Validate and clean raw historical price data.
"""

import pandas as pd

from src.config import settings


RAW_REQUIRED_COLUMNS = {
    "symbol",
    "timestamp",
    "open",
    "high",
    "low",
    "close",
    "volume",
}

VALIDATED_REQUIRED_COLUMNS = {
    "ticker",
    "timestamp",
    "open",
    "high",
    "low",
    "close",
    "volume",
}


def validate_raw_price_data(
    df: pd.DataFrame,
    expected_tickers: list[str] | None = None,
) -> dict:
    """
    Validate raw OHLCV price data from Alpaca.

    Raw data is expected to use the provider column name: symbol.
    """
    issues = {
        "errors": [],
        "warnings": [],
        "fixable": [],
    }

    missing_columns = RAW_REQUIRED_COLUMNS - set(df.columns)
    if missing_columns:
        issues["errors"].append(f"Missing required columns: {missing_columns}")
        return issues

    if expected_tickers is not None:
        actual_tickers = set(df["symbol"].unique())
        expected_tickers_set = set(expected_tickers)

        unexpected = actual_tickers - expected_tickers_set
        missing = expected_tickers_set - actual_tickers

        if unexpected:
            issues["warnings"].append(f"Unexpected tickers found: {unexpected}")
        if missing:
            issues["warnings"].append(f"Expected tickers missing: {missing}")

    duplicate_count = df.duplicated(subset=["symbol", "timestamp"]).sum()
    if duplicate_count > 0:
        issues["fixable"].append(
            f"Found {duplicate_count} duplicate symbol/timestamp rows"
        )

    key_columns = ["symbol", "timestamp", "open", "high", "low", "close", "volume"]
    null_counts = df[key_columns].isna().sum()
    null_counts = null_counts[null_counts > 0]

    if not null_counts.empty:
        issues["warnings"].append(f"Missing values found: {null_counts.to_dict()}")

    price_columns = ["open", "high", "low", "close"]
    invalid_prices = (df[price_columns] <= 0).sum()
    invalid_prices = invalid_prices[invalid_prices > 0]

    if not invalid_prices.empty:
        issues["errors"].append(
            f"Non-positive prices found: {invalid_prices.to_dict()}"
        )

    negative_volume_count = (df["volume"] < 0).sum()
    if negative_volume_count > 0:
        issues["errors"].append(
            f"Found {negative_volume_count} rows with negative volume"
        )

    return issues


def validate_clean_price_data(
    df: pd.DataFrame,
    expected_tickers: list[str] | None = None,
) -> dict:
    """
    Validate cleaned OHLCV price data.

    Cleaned/interim data is expected to use the project-standard column name: ticker.
    """
    issues = {
        "errors": [],
        "warnings": [],
        "fixable": [],
    }

    missing_columns = VALIDATED_REQUIRED_COLUMNS - set(df.columns)
    if missing_columns:
        issues["errors"].append(f"Missing required columns: {missing_columns}")
        return issues

    if expected_tickers is not None:
        actual_tickers = set(df["ticker"].unique())
        expected_tickers_set = set(expected_tickers)

        unexpected = actual_tickers - expected_tickers_set
        missing = expected_tickers_set - actual_tickers

        if unexpected:
            issues["warnings"].append(f"Unexpected tickers found: {unexpected}")
        if missing:
            issues["warnings"].append(f"Expected tickers missing: {missing}")

    duplicate_count = df.duplicated(subset=["ticker", "timestamp"]).sum()
    if duplicate_count > 0:
        issues["errors"].append(
            f"Found {duplicate_count} duplicate ticker/timestamp rows"
        )

    key_columns = ["ticker", "timestamp", "open", "high", "low", "close", "volume"]
    null_counts = df[key_columns].isna().sum()
    null_counts = null_counts[null_counts > 0]

    if not null_counts.empty:
        issues["errors"].append(f"Missing values found: {null_counts.to_dict()}")

    price_columns = ["open", "high", "low", "close"]
    invalid_prices = (df[price_columns] <= 0).sum()
    invalid_prices = invalid_prices[invalid_prices > 0]

    if not invalid_prices.empty:
        issues["errors"].append(
            f"Non-positive prices found: {invalid_prices.to_dict()}"
        )

    negative_volume_count = (df["volume"] < 0).sum()
    if negative_volume_count > 0:
        issues["errors"].append(
            f"Found {negative_volume_count} rows with negative volume"
        )

    return issues


def clean_price_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean raw OHLCV price data while preserving the original raw file.

    Raw Alpaca data uses 'symbol'. The cleaned project-standard output uses 'ticker'.
    """
    cleaned = df.copy()

    cleaned["timestamp"] = pd.to_datetime(cleaned["timestamp"])

    cleaned = cleaned.drop_duplicates(subset=["symbol", "timestamp"])

    cleaned = cleaned.dropna(
        subset=["symbol", "timestamp", "open", "high", "low", "close", "volume"]
    )

    cleaned = cleaned[
        (cleaned["open"] > 0)
        & (cleaned["high"] > 0)
        & (cleaned["low"] > 0)
        & (cleaned["close"] > 0)
        & (cleaned["volume"] >= 0)
    ]

    cleaned = cleaned.sort_values(["symbol", "timestamp"]).reset_index(drop=True)

    cleaned = cleaned.rename(columns={"symbol": "ticker"})

    return cleaned


def main() -> None:
    input_path = settings.raw_data_dir / "daily_bars_starter.csv"
    output_path = settings.project_root / "data" / "interim" / "daily_bars_validated.csv"

    raw = pd.read_csv(input_path)

    before_report = validate_raw_price_data(raw, expected_tickers=["AAPL", "QQQ"])
    print("Validation report before cleaning:")
    print(before_report)

    if before_report["errors"]:
        raise ValueError(f"Raw validation failed: {before_report['errors']}")

    cleaned = clean_price_data(raw)

    after_report = validate_clean_price_data(cleaned, expected_tickers=["AAPL", "QQQ"])
    print("\nValidation report after cleaning:")
    print(after_report)

    if after_report["errors"]:
        raise ValueError(f"Validation failed after cleaning: {after_report['errors']}")

    cleaned.to_csv(output_path, index=False)
    print(f"\nSaved cleaned data to {output_path}")


if __name__ == "__main__":
    main()