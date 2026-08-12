# Feature Engineering

## Overview

The feature engineering layer transforms validated historical market data into model-ready predictors for determining whether a stock will outperform QQQ over the next five trading days.

Features are designed around three primary ideas:

1. Recent price, volatility, and trading activity
2. Trend and price positioning
3. Performance relative to the QQQ benchmark

Feature calculations use only information available at or before each observation timestamp to prevent future-data leakage.

---

# Feature Pipeline

The feature pipeline follows:

```text
Validated Prices
       │
       ▼
Technical Feature Engineering
       │
       ▼
Benchmark-Relative Feature Engineering
       │
       ▼
Feature Schema
       │
       ▼
Features Table
       │
       ▼
Training Dataset Builder
```

Feature generation is separated from model training so engineered features can be generated, validated, persisted, queried, and reused independently of individual machine learning models.

---

# Feature Definitions

The current system contains 14 engineered features organized into several feature families.

## Base Features

The base feature set contains seven features.

### `return_1d`

One-trading-day percentage return.

```text
return_1d(t) = close(t) / close(t-1) - 1
```

This measures short-term price movement.

---

### `return_5d`

Five-trading-day trailing percentage return.

```text
return_5d(t) = close(t) / close(t-5) - 1
```

This captures short-term momentum over a horizon similar to the prediction horizon.

This is a trailing return and therefore does not use future information.

---

### `sma_20`

20-trading-day simple moving average of closing price.

```text
sma_20(t) = mean(close(t-19), ..., close(t))
```

This represents the stock's intermediate short-term price trend.

---

### `sma_50`

50-trading-day simple moving average of closing price.

```text
sma_50(t) = mean(close(t-49), ..., close(t))
```

This provides a longer trend reference than the 20-day moving average.

---

### `ema_20`

20-trading-day exponential moving average of closing price.

Unlike a simple moving average, the exponential moving average assigns greater weight to recent observations.

This provides a more responsive measure of recent price trend.

---

### `volatility_20`

Rolling 20-trading-day volatility calculated from daily returns.

This measures the recent variability of stock returns.

Higher values indicate greater recent price variability.

---

### `volume_ratio_20`

Current trading volume relative to its 20-day rolling average volume.

Conceptually:

```text
volume_ratio_20(t) =
    volume(t) / mean(volume(t-19), ..., volume(t))
```

This provides information about whether current trading activity is unusually high or low relative to recent history.

---

# Relative Trend Features

Raw moving-average values depend heavily on the absolute price level of a stock.

For example, a moving average of 200 has a different interpretation for a $220 stock than for a $900 stock.

Relative trend features normalize these relationships.

The current relative trend feature set contains four features.

## `price_to_sma_20`

Measures the current closing price relative to the 20-day simple moving average.

Conceptually:

```text
close / sma_20 - 1
```

Positive values indicate the stock is trading above its 20-day average.

Negative values indicate the stock is trading below its 20-day average.

---

## `price_to_sma_50`

Measures the current closing price relative to the 50-day simple moving average.

Conceptually:

```text
close / sma_50 - 1
```

This provides a normalized measure of price positioning relative to a longer-term trend.

---

## `price_to_ema_20`

Measures the current closing price relative to the 20-day exponential moving average.

Conceptually:

```text
close / ema_20 - 1
```

This provides a normalized measure of price positioning relative to a trend indicator that places greater weight on recent prices.

---

## `sma_20_to_sma_50`

Measures the relationship between the short-term and longer-term moving averages.

Conceptually:

```text
sma_20 / sma_50 - 1
```

Positive values indicate the 20-day average is above the 50-day average.

Negative values indicate the 20-day average is below the 50-day average.

---

# Benchmark-Relative Features

Because the prediction target is defined relative to QQQ, the feature system also explicitly measures stock behavior relative to QQQ.

These features are calculated by aligning each stock observation with the QQQ observation from the same trading timestamp.

The current benchmark-relative feature set contains three features.

## `relative_return_1d`

Difference between the stock's one-day return and QQQ's one-day return.

```text
relative_return_1d =
    stock_return_1d - qqq_return_1d
```

Positive values indicate the stock outperformed QQQ during the previous trading day.

---

## `relative_return_5d`

Difference between the stock's trailing five-day return and QQQ's trailing five-day return.

```text
relative_return_5d =
    stock_return_5d - qqq_return_5d
```

Positive values indicate the stock outperformed QQQ over the trailing five-trading-day period.

This is distinct from the prediction label because it measures historical relative performance rather than future relative performance.

---

## `relative_volatility_20`

Difference between the stock's recent volatility and QQQ's recent volatility.

```text
relative_volatility_20 =
    stock_volatility_20 - qqq_volatility_20
```

Positive values indicate that the stock has recently been more volatile than QQQ.

---

# Feature Sets

Feature definitions are centralized in:

```text
src/features/schema.py
```

This prevents different parts of the project from maintaining inconsistent lists of feature names.

The current feature groups include:

```text
BASE_FEATURE_COLUMNS
RELATIVE_TREND_FEATURE_COLUMNS
BENCHMARK_RELATIVE_FEATURE_COLUMNS
STATIONARY_FEATURE_COLUMNS
FEATURE_COLUMNS
FEATURE_TABLE_COLUMNS
```

## Base

Contains the seven original technical features.

```text
return_1d
return_5d
sma_20
sma_50
ema_20
volatility_20
volume_ratio_20
```

## Relative Trend

Contains the four normalized trend features.

```text
price_to_sma_20
price_to_sma_50
price_to_ema_20
sma_20_to_sma_50
```

## Benchmark Relative

Contains the three QQQ-relative features.

```text
relative_return_1d
relative_return_5d
relative_volatility_20
```

## Combined

Contains all currently engineered features.

```text
7 base
+ 4 relative trend
+ 3 benchmark relative
= 14 features
```

## Stationary

The stationary feature set removes raw price-level moving-average features while retaining returns, volatility, volume, normalized trend relationships, and benchmark-relative features.

This feature set is intended to reduce dependence on absolute stock price levels and improve comparability across securities.

---

# Rolling Windows and Missing Values

Several features require historical observations before they can be calculated.

For example:

```text
return_1d          requires previous price history
return_5d          requires five previous observations
sma_20             requires a 20-day window
sma_50             requires a 50-day window
volatility_20      requires recent return history
volume_ratio_20    requires recent volume history
```

Missing values at the beginning of each ticker's history are therefore expected rather than treated as data-quality failures.

Feature generation preserves these observations.

The training dataset builder later removes rows that do not yet contain the complete feature history required for model training.

This separation allows the feature table to represent the full historical feature-generation process.

---

# Per-Ticker Calculations

Technical features are calculated independently for each ticker.

Rolling calculations must never cross ticker boundaries.

For example, the first AAPL observation must not use the final observation from another security when calculating returns.

Grouping calculations by ticker ensures each security maintains its own independent historical sequence.

---

# Benchmark Alignment

Benchmark-relative features require stock observations and QQQ observations to be aligned by trading timestamp.

Conceptually:

```text
Stock Features
      │
      │ timestamp
      ▼
QQQ Features
      │
      ▼
Benchmark-Relative Features
```

This ensures relative calculations compare market observations from the same trading session.

QQQ remains available during feature construction even though QQQ is excluded from the final prediction universe.

---

# Leakage Prevention

Preventing future-data leakage is a central requirement of the feature engineering system.

Features at timestamp `t` may use:

```text
t
t-1
t-2
...
```

but must never use:

```text
t+1
t+2
...
```

Forward returns are therefore not feature columns.

They are generated separately by the label pipeline and used only as prediction targets.

The distinction is particularly important for:

```text
relative_return_5d
```

versus:

```text
forward_return_5d
qqq_forward_return_5d
outperformed_qqq
```

`relative_return_5d` describes historical information available at prediction time.

The forward-return columns describe future outcomes and cannot be provided to the model as predictors.

---

# Feature Persistence

Generated features are stored in the SQLite `features` table.

Each row is uniquely identified by:

```text
ticker
timestamp
```

This key corresponds to the same ticker/timestamp structure used by validated prices and prediction labels.

The current feature table contains:

```text
11,022 rows
```

covering the ten modeled stocks and QQQ benchmark.

The table contains the complete 14-feature schema.

---

# Model-Ready Feature Data

The features table includes QQQ because benchmark data is required during feature construction.

The final model-ready dataset excludes QQQ as a prediction target.

After feature warm-up periods and unavailable forward labels are removed, the current training dataset contains:

```text
10 modeled stocks
948 observations per stock
9,480 observations total
```

All model-ready observations contain complete values for the selected feature columns.

---

# Feature Ablation

The preprocessing and evaluation systems support selecting feature subsets dynamically.

This allows models to be evaluated using the same chronological cross-validation process while changing only the supplied features.

Current comparisons include:

```text
Base
Relative Trend
Benchmark Relative
Stationary
Combined
```

This provides a controlled way to determine whether adding a feature family improves out-of-sample predictive performance.

Feature engineering decisions therefore do not rely only on intuition; they can be tested empirically against the same models and evaluation periods.

---

# Current Status

Implemented:

- Per-ticker return calculations
- Moving averages
- Exponential moving averages
- Rolling volatility
- Relative volume
- Normalized trend features
- QQQ-relative return features
- QQQ-relative volatility
- Centralized feature schema
- SQLite feature persistence
- Feature query utilities
- Feature validation
- Feature warm-up handling
- Feature subset selection
- Feature-ablation evaluation

Current feature count:

```text
14
```

Planned:

- Additional momentum features
- Additional volatility features
- Market regime features
- Feature importance analysis
- Feature selection
- Further benchmark-relative signals

Feature additions will be evaluated through chronological cross-validation before being incorporated into later modeling stages.
