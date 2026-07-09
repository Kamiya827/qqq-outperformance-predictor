"""
Validate engineered feature data.
"""

import pandas as pd


REQUIRED_FEATURE_COLUMNS = {
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


def validate_features(df: pd.DataFrame) -> dict:
    """
    Validate engineered features and return a report.
    """
    issues = {
        "errors": [],
        "warnings": [],
    }

    missing_columns = REQUIRED_FEATURE_COLUMNS - set(df.columns)
    if missing_columns:
        issues["errors"].append(f"Missing required columns: {missing_columns}")
        return issues

    duplicate_count = df.duplicated(subset=["ticker", "timestamp"]).sum()
    if duplicate_count > 0:
        issues["errors"].append(
            f"Found {duplicate_count} duplicate ticker/timestamp feature rows"
        )

    invalid_volatility_count = (df["volatility_20"] < 0).sum()
    if invalid_volatility_count > 0:
        issues["errors"].append(
            f"Found {invalid_volatility_count} rows with negative volatility"
        )

    invalid_volume_ratio_count = (df["volume_ratio_20"] < 0).sum()
    if invalid_volume_ratio_count > 0:
        issues["errors"].append(
            f"Found {invalid_volume_ratio_count} rows with negative volume ratio"
        )

    null_counts = df.isna().sum()
    null_counts = null_counts[null_counts > 0]

    if not null_counts.empty:
        issues["warnings"].append(
            f"Missing values found, likely from rolling windows: {null_counts.to_dict()}"
        )

    return issues