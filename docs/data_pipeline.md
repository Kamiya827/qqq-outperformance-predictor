# Data Pipeline

## Overview

The QQQ Outperformance Predictor follows a modular data engineering and machine learning pipeline in which each stage has a single responsibility.

```text
Stock Universe
      │
      ▼
Alpaca API
      │
      ▼
Raw Market Data (CSV)
      │
      ▼
Validation & Cleaning
      │
      ▼
Validated Market Data (CSV)
      │
      ▼
Validated Prices Table
      │
      ├─────────────────────┐
      ▼                     ▼
Feature Engineering    Label Generation
      │                     │
      ▼                     ▼
Features Table          Labels Table
      └──────────┬──────────┘
                 ▼
        Training Dataset Builder
                 │
                 ▼
         Model-Ready Dataset
                 │
                 ▼
     Chronological Data Splitting
                 │
                 ▼
       Machine Learning Models
                 │
                 ▼
          Model Evaluation
                 │
                 ▼
       Feature / Model Comparison
                 │
                 ▼
         Experiment Tracking
            (planned)
```

---

# Stock Universe

The development universe is defined in:

```text
data/external/starter_universe.csv
```

The current universe contains ten modeled stocks:

- AAPL
- AMZN
- AVGO
- COST
- GOOGL
- META
- MSFT
- NFLX
- NVDA
- TSLA

QQQ is included as the benchmark.

The universe loader provides the ticker list used by the market data download and validation stages, avoiding separate hardcoded ticker definitions across the pipeline.

---

# Raw Market Data

Historical daily market data is downloaded from Alpaca.

The raw dataset contains provider-supplied market data including:

- Symbol
- Timestamp
- Open
- High
- Low
- Close
- Volume
- Trade count
- VWAP

Raw data is stored without modification so the original provider output remains available for debugging and reproducibility.

The current raw dataset contains:

```text
11 symbols
11,022 observations
```

---

# Validation and Cleaning

Raw market data is validated before being used downstream.

Validation checks include:

- Required columns
- Expected tickers
- Duplicate symbol/timestamp rows
- Missing values
- Non-positive prices
- Negative volume

The cleaning stage:

- Parses timestamps
- Removes duplicate observations
- Removes invalid or incomplete observations
- Sorts observations chronologically by symbol
- Renames the provider-specific `symbol` column to the project-standard `ticker` column

The cleaned dataset is written to:

```text
data/interim/daily_bars_validated.csv
```

Validation is performed again after cleaning.

---

# Database Loading

Validated market data is loaded into the SQLite database.

The database acts as the persistent source of truth for downstream pipeline stages.

The `validated_prices` table currently contains:

```text
11,022 rows
```

across the ten modeled stocks and QQQ benchmark.

Database loading and querying are separated from feature engineering and modeling logic through reusable database modules.

---

# Feature Engineering

Engineered features are generated from validated historical market data.

The current feature system includes:

## Base Technical Features

- 1-day return
- 5-day return
- 20-day simple moving average
- 50-day simple moving average
- 20-day exponential moving average
- 20-day volatility
- 20-day volume ratio

## Relative Trend Features

- Price relative to 20-day SMA
- Price relative to 50-day SMA
- Price relative to 20-day EMA
- 20-day SMA relative to 50-day SMA

## Benchmark-Relative Features

- 1-day return relative to QQQ
- 5-day return relative to QQQ
- 20-day volatility relative to QQQ

The combined feature set currently contains:

```text
14 engineered features
```

Feature calculations use only information available at or before each observation timestamp.

Engineered features are persisted in the SQLite `features` table.

---

# Label Generation

The prediction target measures whether a stock outperforms QQQ over the following five trading days.

For each stock and timestamp:

```text
stock forward 5-day return
            versus
QQQ forward 5-day return
```

The binary target is:

```text
1 = stock outperforms QQQ
0 = stock does not outperform QQQ
```

QQQ provides the benchmark return but is not itself included as a prediction target.

Generated labels are persisted in the SQLite `labels` table.

---

# Training Dataset

The training dataset builder joins engineered features and labels by:

```text
ticker
timestamp
```

Observations without sufficient historical data for feature calculation or sufficient future data for label generation are removed.

The current model-ready dataset contains:

```text
10 modeled stocks
948 observations per stock
9,480 total observations
```

The current label distribution is:

```text
Outperformed QQQ:      4,911
Did not outperform:    4,569
```

This produces a relatively balanced binary classification dataset.

---

# Chronological Splitting

Market data must not be randomly divided into training and evaluation sets because doing so could introduce future information into model development.

Both the holdout train/test splitter and cross-validation splitter therefore operate on unique trading timestamps.

All stocks from the same market date are assigned to the same partition.

The holdout split currently uses an 80/20 chronological division of unique timestamps.

The cross-validation system uses:

```text
5 chronological folds
5 trading-timestamp gap
expanding training window
```

The five-timestamp gap separates training and validation periods to account for the five-trading-day prediction horizon.

---

# Machine Learning

The current baseline modeling layer includes:

- Logistic Regression
- Decision Tree
- Random Forest
- Gradient Boosting

Shared preprocessing and evaluation utilities prevent model-specific pipelines from duplicating feature preparation, scaling, splitting, and metric calculations.

---

# Model Evaluation

Models are evaluated using chronological cross-validation.

Current classification metrics include:

- Accuracy
- Precision
- Recall
- F1 score
- ROC-AUC

Fold-level results are summarized using the mean and standard deviation of each metric.

ROC-AUC is used as an important comparison metric because the objective is to determine whether models can distinguish stocks that will outperform QQQ from those that will not.

---

# Feature Ablation

The evaluation pipeline supports selecting specific feature subsets without duplicating model-training logic.

Current feature sets include:

- Base
- Relative Trend
- Benchmark Relative
- Stationary
- Combined

Each feature set can be evaluated across the same baseline models and chronological cross-validation folds.

This allows the contribution of different feature families to be measured systematically.

Initial single-stock experiments were followed by evaluation across the expanded ten-stock universe to test whether observed patterns generalize across securities.

---

## Current Status

Implemented:

- Stock universe management
- Historical market data download
- Raw data preservation
- Data validation and cleaning
- SQLite database initialization
- Validated data loading into SQLite
- Reusable SQL query utilities
- Technical feature engineering
- Relative trend feature engineering
- Benchmark-relative feature engineering
- Feature persistence
- Feature validation
- Label generation
- Label persistence
- Training dataset construction
- Panel-safe chronological train/test splitting
- Time-series cross-validation
- Five-trading-day cross-validation gap
- Shared model preprocessing
- Logistic Regression baseline
- Decision Tree baseline
- Random Forest baseline
- Gradient Boosting baseline
- Shared evaluation metrics
- Baseline model comparison
- Feature-set ablation

Planned:

- Persistent experiment tracking
- Additional feature engineering
- Feature importance analysis
- Hyperparameter optimization
- Portfolio-level backtesting and strategy evaluation

Each pipeline stage is intentionally independent so that datasets can be regenerated without modifying previous stages, supporting reproducibility and maintainability.
