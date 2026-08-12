# Modeling

## Overview

The modeling layer of the QQQ Outperformance Predictor evaluates whether engineered market features contain enough predictive information to identify stocks that will outperform QQQ over the next five trading days.

The problem is formulated as binary classification:

```text
1 = stock outperforms QQQ over the next five trading days
0 = stock does not outperform QQQ over the next five trading days
```

The modeling system is designed around three priorities:

1. Prevent time-series leakage
2. Establish reproducible baseline performance
3. Compare models and feature sets using the same evaluation framework

The current stage of the project focuses on baseline modeling and feature evaluation rather than aggressive model optimization.

---

# Modeling Problem

For each stock at trading timestamp `t`, the model receives engineered features calculated using information available at or before `t`.

The model attempts to predict whether:

```text
stock forward 5-day return > QQQ forward 5-day return
```

The target column is:

```text
outperformed_qqq
```

Forward-return columns are retained for dataset construction and analysis but are explicitly excluded from model features.

---

# Prediction Universe

The current development universe contains ten modeled stocks:

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

QQQ is used as the benchmark but is excluded from the prediction targets.

After feature warm-up periods and unavailable forward labels are removed, the current model-ready dataset contains:

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

The target is therefore relatively balanced.

---

# Feature Preparation

Model preprocessing is centralized so that models use consistent feature-selection logic.

The preprocessing layer separates:

```text
X = model features
y = outperformed_qqq
```

The following columns are not allowed to enter the feature matrix:

```text
ticker
timestamp
forward_return_5d
qqq_forward_return_5d
outperformed_qqq
```

This prevents identifiers and future outcome information from being supplied to the models.

Feature subsets can be passed explicitly into the preprocessing pipeline, enabling controlled feature-ablation experiments.

---

# Feature Sets

The modeling system currently evaluates several feature families.

## Base

Seven original technical features:

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

Four normalized trend features:

```text
price_to_sma_20
price_to_sma_50
price_to_ema_20
sma_20_to_sma_50
```

## Benchmark Relative

Three features describing stock behavior relative to QQQ:

```text
relative_return_1d
relative_return_5d
relative_volatility_20
```

## Stationary

A feature set designed to reduce dependence on absolute stock price levels.

It combines returns, volatility, volume, normalized trend relationships, and benchmark-relative information while excluding raw moving-average price levels.

## Combined

The complete current feature set containing all 14 engineered features.

---

# Feature Scaling

Some machine learning algorithms are sensitive to differences in feature scale.

The project therefore provides reusable feature standardization using:

```text
StandardScaler
```

The scaler is fit only on training data.

Conceptually:

```text
Training Data
      │
      ▼
Fit StandardScaler
      │
      ├───────────────┐
      ▼               ▼
Transform Train   Transform Validation
```

The validation dataset is never used to estimate scaling parameters.

This prevents information from the validation period from influencing preprocessing of the training period.

Scaling is enabled only for models that require or benefit from standardized features.

---

# Chronological Train/Test Split

Random train/test splitting is inappropriate for financial time-series data because it can allow future market observations to influence evaluation of earlier observations.

The project therefore implements a chronological holdout split.

The splitter operates on unique trading timestamps rather than individual dataframe rows.

This is important because the dataset contains multiple stocks for every trading date.

Conceptually:

```text
Historical Data
────────────────────────────────────────────► Time

|-------------- Training --------------| Test |
```

All stocks from the same timestamp are placed in the same partition.

The current default holdout split uses:

```text
80% training timestamps
20% testing timestamps
```

For the current dataset, the resulting split contains:

```text
Training observations: 7,580
Testing observations:  1,900
```

with no chronological overlap between the partitions.

---

# Time-Series Cross-Validation

Model comparison uses time-series cross-validation rather than standard shuffled cross-validation.

The current implementation uses:

```text
TimeSeriesSplit
```

applied to unique trading timestamps.

The system currently uses:

```text
5 folds
5 trading-timestamp gap
expanding training window
```

Conceptually:

```text
Fold 1:
TRAIN ───── GAP ─ VALIDATION

Fold 2:
TRAIN ─────────── GAP ─ VALIDATION

Fold 3:
TRAIN ───────────────── GAP ─ VALIDATION

Fold 4:
TRAIN ─────────────────────── GAP ─ VALIDATION

Fold 5:
TRAIN ───────────────────────────── GAP ─ VALIDATION
```

Training data expands through time while validation always occurs strictly after training.

---

# Cross-Validation Gap

The prediction target uses a five-trading-day forward return.

Without a gap, observations near the end of a training period could have labels whose forward-return windows overlap the validation period.

A five-trading-timestamp gap is therefore inserted between training and validation because the prediction label uses a five-trading-day forward return.

This prevents the forward-return windows used to construct training labels from extending into the validation period, reducing the risk of temporal leakage between training and evaluation.

---

# Baseline Models

The project currently evaluates four baseline classifiers.

## Logistic Regression

Logistic Regression provides a simple linear baseline.

It is useful for determining whether the engineered features contain approximately linear predictive relationships.

Features are standardized before fitting Logistic Regression.

---

## Decision Tree

The Decision Tree provides a nonlinear baseline capable of learning threshold-based relationships and interactions between features.

It also provides a useful comparison against ensemble tree methods.

---

## Random Forest

Random Forest combines multiple decision trees to reduce the variance associated with a single tree.

It provides a more flexible nonlinear baseline and can capture interactions among engineered market features.

---

## Gradient Boosting

Gradient Boosting sequentially combines weak decision trees to model more complex nonlinear relationships.

It provides an additional nonlinear baseline for testing whether sequential tree-based learning can capture predictive relationships not identified by the simpler models.

---

# Evaluation Metrics

All models are evaluated through the same reusable evaluation pipeline.

Current metrics include:

```text
Accuracy
Precision
Recall
F1 Score
ROC-AUC
```

## Accuracy

Measures the proportion of predictions that are correct.

Because the current target is relatively balanced, accuracy remains useful, although it is not sufficient on its own.

## Precision

Measures how frequently predicted outperformers actually outperform QQQ.

This becomes especially important if model predictions are later used to select stocks for a trading strategy.

## Recall

Measures how many actual outperformers are successfully identified by the model.

## F1 Score

Combines precision and recall into a single metric.

## ROC-AUC

Measures the model's ability to rank positive observations above negative observations across classification thresholds.

ROC-AUC is currently an important model-comparison metric because it evaluates ranking ability without relying on a single classification threshold.

---

# Baseline Evaluation

Initial baseline experiments were first performed on a small development dataset before the stock universe was expanded.

The expanded dataset materially changed the evaluation problem.

Current multi-stock experiments show that baseline predictive performance remains close to random classification.

Across the current feature-ablation results, ROC-AUC values are generally near:

```text
0.50
```

with the strongest current results only modestly above that level.

This is an important result rather than a reason to immediately increase model complexity.

It indicates that the current feature set does not yet provide a strong, consistently generalizable signal across the expanded stock universe.

---

# Feature Ablation

Feature ablation is used to determine whether particular feature families contribute useful predictive information.

The same baseline models, folds, gap, and evaluation metrics are reused while changing only the selected feature columns.

Current comparisons include:

```text
Base
Relative Trend
Benchmark Relative
Stationary
Combined
```

This provides a controlled experimental framework.

For example:

```text
Same model
Same observations
Same folds
Same evaluation metrics
Different feature set
```

Differences in performance can therefore be attributed more directly to the supplied features.

---

# Current Feature-Ablation Findings

The expanded-universe experiments produced an important finding.

Benchmark-relative features initially appeared more promising when evaluated on the smaller development dataset.

After expanding the prediction universe to ten stocks, that apparent advantage largely disappeared.

The current expanded-universe results show that no feature family consistently produces strong predictive performance across the baseline models.

The best current ROC-AUC results are only modestly above random performance.

This suggests that signals observed on a single security should not be assumed to generalize across a broader universe.

The project therefore prioritizes improving the experimental framework and feature quality before performing extensive hyperparameter optimization.

---

# Model Comparison

Model comparison is centralized through reusable cross-validation utilities.

Each model produces fold-level metrics that can be summarized using:

```text
mean
standard deviation
```

This allows comparison of both predictive performance and stability across market periods.

A model with slightly higher average performance but extreme variation between folds may be less useful than a more stable alternative.

---

# Current Modeling Philosophy

The current modeling stage follows the principle:

```text
Validate signal before optimizing model complexity.
```

The project intentionally begins with relatively simple baseline models.

If the current features contain little generalizable predictive information, extensive hyperparameter tuning or significantly more complicated models may simply overfit noise.

The current development sequence therefore prioritizes:

```text
Reliable evaluation
        ↓
Feature engineering
        ↓
Feature ablation
        ↓
Signal validation
        ↓
Model optimization
```

rather than immediately optimizing model parameters.

---

# Current Status

Implemented:

- Binary classification target
- Model-ready dataset construction
- Feature/label separation
- Explicit exclusion of future-return columns
- Dynamic feature subset selection
- Feature standardization
- Panel-safe chronological holdout splitting
- Time-series cross-validation
- Five-trading-day evaluation gap
- Logistic Regression baseline
- Decision Tree baseline
- Random Forest baseline
- Gradient Boosting baseline
- Shared classification metrics
- Fold-level evaluation
- Cross-validation summaries
- Baseline model comparison
- Feature-ablation experiments
- Expanded-universe evaluation

Current result:

```text
Baseline predictive performance remains close to random
across the expanded ten-stock universe.
```

This indicates that additional signal discovery is required before moving to aggressive model optimization.

---

# Planned Modeling Work

The next modeling improvements include:

- Persistent experiment tracking
- Additional feature engineering
- Feature importance analysis
- Additional feature selection experiments
- Hyperparameter optimization after stronger signals are identified
- Final holdout evaluation
- Probability-based stock ranking
- Portfolio construction
- Backtesting

More complex models should be introduced only when justified by improvements in out-of-sample performance.

The objective is not to maximize model complexity, but to build a reproducible system capable of identifying genuine and generalizable predictive signal.
