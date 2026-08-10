"""
Shared definitions for engineered feature columns.
"""

BASE_FEATURE_COLUMNS = [
    "return_1d",
    "return_5d",
    "sma_20",
    "sma_50",
    "ema_20",
    "volatility_20",
    "volume_ratio_20",
]

RELATIVE_TREND_FEATURE_COLUMNS = [
    "price_to_sma_20",
    "price_to_sma_50",
    "price_to_ema_20",
    "sma_20_to_sma_50",
]

BENCHMARK_RELATIVE_FEATURE_COLUMNS = [
    "relative_return_1d",
    "relative_return_5d",
    "relative_volatility_20",
]

TECHNICAL_FEATURE_COLUMNS = (
    BASE_FEATURE_COLUMNS
    + RELATIVE_TREND_FEATURE_COLUMNS
)

TECHNICAL_FEATURE_TABLE_COLUMNS = [
    "ticker",
    "timestamp",
    *TECHNICAL_FEATURE_COLUMNS,
]

STATIONARY_FEATURE_COLUMNS = [
    "return_1d",
    "return_5d",
    "volatility_20",
    "volume_ratio_20",
    *RELATIVE_TREND_FEATURE_COLUMNS,
    *BENCHMARK_RELATIVE_FEATURE_COLUMNS,
]

FEATURE_COLUMNS = (
    BASE_FEATURE_COLUMNS
    + RELATIVE_TREND_FEATURE_COLUMNS
    + BENCHMARK_RELATIVE_FEATURE_COLUMNS
)

FEATURE_TABLE_COLUMNS = [
    "ticker",
    "timestamp",
    *FEATURE_COLUMNS,
]