# Project Architecture

## Purpose

The QQQ Outperformance Predictor is designed as a production-inspired machine learning system rather than a collection of scripts. The goal is to demonstrate software engineering, data engineering, machine learning, quantitative finance, and documentation best practices within a single cohesive project. The system predicts whether an individual stock will outperform QQQ over the next five trading days.

The architecture is intentionally modular so that each component has a single responsibility and can evolve independently as the project grows.

---

# Design Principles

The architecture is guided by several core principles.

## Single Responsibility Principle

Each module should have one clearly defined responsibility.

Examples:

* `config.py` manages project configuration.
* `client.py` creates authenticated Alpaca clients.
* `download_prices.py` downloads historical market data.
* `validate.py` validates and cleans raw market data.
* `features/` contains feature engineering logic.
* `models/` contains preprocessing, splitting, and model definitions.
* `evaluation/` contains reusable model evaluation logic.
* `pipelines/` contains executable workflows that connect project components.

Separating responsibilities makes the project easier to test, maintain, and extend.

---

## Reproducibility

Every stage of the pipeline should be reproducible.

Rather than manually editing datasets, each stage consumes a well-defined input and produces a well-defined output.

This allows the complete data and modeling pipeline to be rerun whenever the stock universe, features, labels, or models change.

---

## Separation of Data and Logic

Raw data is never modified directly.

Instead, each processing stage creates a new representation of the data while preserving previous stages.

The current data lifecycle separates:

- Raw market data
- Validated market data
- Engineered features
- Prediction labels
- Model-ready training data

This makes debugging significantly easier and preserves the original source data.

---

## Configuration Management

Secrets and environment-specific configuration are never hardcoded.

Configuration is centralized through `.env` and `src/config.py`, allowing credentials and settings to be managed independently of the application logic.

---

## Leakage Prevention

The modeling architecture is designed to prevent future information from leaking into model training.

Feature calculations use only information available at or before each timestamp.

Prediction labels use future returns but are stored separately from model features.

Chronological train/test splitting and cross-validation operate on unique trading timestamps so that all stocks from the same market date remain in the same partition.

Cross-validation also uses a five-trading-day gap between training and validation periods to account for the five-day prediction horizon.

---

# System Architecture

The current high-level architecture is shown below.

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
        Validation & Cleaning Pipeline
                     │
                     ▼
        Validated Market Data (CSV)
                     │
                     ▼
              SQLite Database
                     │
      ┌──────────────┴──────────────┐
      ▼                             ▼
Feature Engineering          Label Generation
      │                             │
      ▼                             ▼
 Features Table              Labels Table
      └──────────────┬──────────────┘
                     ▼
        Training Dataset Builder
                     ▼
        Model-Ready Dataset (X, y)
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

# Development Stock Universe

The development universe currently contains ten modeled stocks plus QQQ as the benchmark.

The modeled universe includes:

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

QQQ is included in the market dataset as the benchmark but is not treated as a prediction target.

The universe is defined centrally in:

```text
data/external/starter_universe.csv
```

Data downloading and validation use this universe rather than maintaining separate hardcoded ticker lists.

The current validated market dataset contains 11,022 daily price observations across the eleven symbols.

---

# Repository Organization

The repository is organized around functional responsibilities.

```text
src/
│
├── data/
├── database/
├── dataset/
├── evaluation/
├── features/
├── models/
├── pipelines/
├── utils/
└── visualization/
```

Major responsibilities include:

```text
data/
    Market data acquisition, universe management,
    validation, and cleaning

database/
    SQLite schema, connections, loaders, and queries

dataset/
    Construction of model-ready datasets

features/
    Technical and benchmark-relative feature engineering

models/
    Model definitions, preprocessing, and chronological splitting

evaluation/
    Reusable metrics and cross-validation logic

pipelines/
    Executable workflows connecting project components
```

This structure separates ingestion, persistence, feature engineering, modeling, and evaluation rather than combining the workflow into a single script or notebook.


---

# Data Flow

The current data flow is:

1. Load the configured stock universe.
2. Download historical daily market data from Alpaca.
3. Store raw market data without modification.
4. Validate and clean the downloaded data.
5. Store validated market data in SQLite.
6. Generate technical and benchmark-relative features.
7. Store engineered features in the features table.
8. Generate five-day forward-return labels relative to QQQ.
9. Store prediction labels in the labels table.
10. Join features and labels into a model-ready training dataset.
11. Remove observations without sufficient feature history or forward labels.
12. Split data chronologically using unique trading timestamps.
13. Train and evaluate baseline machine learning models.
14. Compare feature sets through feature ablation.
15. Compare model and feature-set evaluation results.

---

# Feature Architecture

Feature engineering is separated from model training so that features can be generated, inspected, persisted, and reused independently of individual models.

The current feature system contains several feature families:

```text
Base Technical Features
        │
        ├── Returns
        ├── Moving averages
        ├── Volatility
        └── Volume

Relative Trend Features
        │
        ├── Price relative to moving averages
        └── Moving-average relationships

Benchmark-Relative Features
        │
        ├── Relative 1-day return
        ├── Relative 5-day return
        └── Relative volatility
        ▼
     QQQ Benchmark
```

Shared feature definitions are centralized so that dataset construction, database persistence, preprocessing, and feature-ablation experiments use consistent feature names.

The current combined feature set contains 14 engineered features.

---

# Training Dataset

The training dataset is constructed by joining engineered features with prediction labels using ticker and timestamp.

QQQ observations are used to construct benchmark-relative features and labels but are excluded from the final prediction universe.

After feature warm-up periods and unavailable forward-return observations are removed, the current model-ready dataset contains:

```text
10 modeled stocks
948 observations per stock
9,480 total observations
```

The target is approximately balanced, with 4,911 positive observations and 4,569 negative observations in the current model-ready dataset.

---

# Time-Series Evaluation

Standard random train/test splitting is inappropriate for this project because it could allow future market observations to influence evaluation of earlier periods.

The project therefore uses chronological evaluation.

Both the holdout train/test splitter and cross-validation splitter operate on unique trading timestamps rather than individual dataframe rows.

This guarantees that all stocks from a given market date remain together.

Cross-validation currently uses:

```text
5 chronological folds
5 trading-timestamp gap
expanding training window
```

The gap separates each training period from its validation period and helps prevent leakage associated with the five-trading-day forward prediction horizon.

---

# Modeling Architecture

The initial modeling layer provides several baseline classifiers:

- Logistic Regression
- Decision Tree
- Random Forest
- Gradient Boosting

Model evaluation is centralized rather than duplicated across model-specific pipelines.

The evaluation layer supports:

- Accuracy
- Precision
- Recall
- F1 score
- ROC-AUC
- Fold-level evaluation
- Cross-validation summaries

Feature subsets can be passed into the shared evaluation pipeline, allowing the same models and cross-validation methodology to be reused for feature-ablation experiments.

This allows model changes and feature changes to be evaluated independently.

---

# Why SQLite?

The project uses SQLite because it provides:

* A lightweight relational database
* Strong SQL support
* Easy reproducibility
* No server installation
* Excellent integration with Python and pandas

SQLite is sufficient for a portfolio-scale project while still demonstrating practical database design and SQL skills.

The database currently acts as the central persistence layer for validated market data, engineered features, and prediction labels.

---

# Experimentation Layer

The project supports systematic comparison of:

- Model architectures
- Feature families
- Combined feature sets

Feature-ablation experiments allow the project to determine whether additional features improve performance across multiple stocks rather than relying on results from a single security.

Persistent experiment tracking is the next planned extension of this layer.

---

# Future Evolution

The architecture is intentionally modular so that future improvements can be introduced without major redesign.

Potential enhancements include:

* Persistent experiment tracking
* Additional feature families
* Broader stock universe
* Hyperparameter optimization
* Additional market data providers
* Automated data refresh
* Explainable AI (SHAP)
* Portfolio construction and backtesting
* Interactive dashboards
* Cloud deployment

The objective is to evolve the project incrementally while maintaining clean architecture and reproducibility.
