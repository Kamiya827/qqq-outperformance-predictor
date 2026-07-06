# QQQ Outperformance Predictor

An end-to-end machine learning project that predicts whether an individual stock will outperform the **Invesco QQQ ETF** over the next **5 trading days**.

This project is being developed as a professional software engineering and machine learning portfolio project. The emphasis is on building a reproducible, well-documented ML pipeline rather than an automated trading system.

---

## Project Objective

Given historical market data available at the close of trading on day **t**, predict whether a stock will outperform the QQQ ETF over the following **5 trading days**.

This is formulated as a binary classification problem:

* **Label = 1:** The stock's 5-day forward return is greater than QQQ's 5-day forward return.
* **Label = 0:** Otherwise.

The project emphasizes proper time-series methodology, avoiding lookahead bias and data leakage while following software engineering best practices.

---

## What This Project Demonstrates

### Machine Learning

* Binary classification
* Feature engineering
* Time-series validation
* Model evaluation
* Experiment tracking
* Model comparison

### Data Engineering

* Alpaca Market Data API
* Data validation and cleaning
* SQLite database design *(coming next)*
* SQL data querying *(planned)*
* Reproducible data pipelines

### Software Engineering

* Modular Python architecture
* Configuration management
* Git version control
* Documentation
* Maintainable code
* Clean project organization

### Quantitative Finance

* Relative return prediction
* Benchmark-based labeling
* Market data processing
* Technical indicators
* Cross-sectional stock analysis

---

## Current Architecture

```text
                Alpaca API
                     │
                     ▼
          Raw Market Data (CSV)
                     │
                     ▼
        Validation & Cleaning Pipeline
                     │
                     ▼
           Validated Market Data
```

**Current implementation**

```text
Alpaca API
      ↓
Download Prices
      ↓
Raw CSV
      ↓
Validation & Cleaning
      ↓
Validated CSV
```

**Target architecture**

```text
                Alpaca API
                     │
                     ▼
          Raw Market Data (CSV)
                     │
                     ▼
        Validation & Cleaning Pipeline
                     │
                     ▼
              SQLite Database
                     │
      ┌──────────────┼──────────────┐
      ▼              ▼              ▼
 SQL Queries    Feature Engineering  Label Generation
      │              │              │
      └──────────────┼──────────────┘
                     ▼
             Training Dataset (X, y)
                     │
                     ▼
          Machine Learning Models
                     │
                     ▼
             Experiment Tracking
```

---

## Repository Structure

```text
qqq-outperformance-predictor/
│
├── data/
│   ├── raw/
│   ├── interim/
│   ├── processed/
│   └── external/
│
├── docs/
├── experiments/
├── notebooks/
├── tests/
│
├── src/
│   ├── data/
│   ├── features/
│   ├── models/
│   ├── evaluation/
│   ├── visualization/
│   ├── utils/
│   └── config.py
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

## Technology Stack

### Languages

* Python 3.11
* SQL (SQLite - planned)

### Libraries

* pandas
* NumPy
* scikit-learn
* matplotlib
* alpaca-py
* python-dotenv

### Tools

* Git
* GitHub
* VS Code

### Planned Additions

* SQLite
* MLflow
* XGBoost or LightGBM
* SHAP
* Optuna

---

## Development Roadmap

### Phase 1 — Foundation

* [x] Initialize Git repository
* [x] Configure Python environment
* [x] Build modular project structure
* [x] Configure Alpaca API
* [x] Create centralized configuration module
* [x] Build data download pipeline
* [x] Build data validation pipeline

### Phase 2 — Data Engineering

* [ ] Design SQLite schema
* [ ] Build database layer
* [ ] Load validated data into SQLite
* [ ] Create SQL query interface
* [ ] Automate data refresh

### Phase 3 — Feature Engineering

* [ ] Price return features
* [ ] Moving averages
* [ ] Momentum indicators
* [ ] Volatility indicators
* [ ] Volume features
* [ ] Relative strength features

### Phase 4 — Label Engineering

* [ ] Generate 5-day forward returns
* [ ] Generate benchmark (QQQ) returns
* [ ] Build binary classification labels
* [ ] Assemble training dataset

### Phase 5 — Machine Learning

* [ ] Exploratory data analysis
* [ ] Logistic Regression baseline
* [ ] Decision Tree
* [ ] Random Forest
* [ ] Gradient Boosting
* [ ] Hyperparameter tuning

### Phase 6 — Evaluation

* [ ] Time-series cross-validation
* [ ] Precision / Recall
* [ ] ROC-AUC
* [ ] Feature importance
* [ ] Error analysis

### Phase 7 — Experiment Tracking

* [ ] SQL experiment logging
* [ ] Compare model performance
* [ ] Track feature sets
* [ ] Record hypotheses and conclusions

### Phase 8 — Documentation

* [ ] Architecture diagrams
* [ ] Database schema
* [ ] Technical documentation
* [ ] Model cards
* [ ] Final project report

---

## Learning Objectives

This project serves as an applied extension of concepts learned through:

* IBM SQL for Data Science with Python
* Machine Learning Specialization (Andrew Ng)
* Independent study of quantitative finance
* Software engineering best practices

The goal is to integrate these concepts into a cohesive, production-inspired machine learning project.

---

## Current Status

**Current Phase:** Foundation Complete

### Completed

* Modular repository architecture
* Secure configuration management
* Alpaca market data ingestion
* Stock universe management
* Data validation and cleaning pipeline

### Next Milestone

Design and implement the SQLite database layer that will serve as the project's single source of truth.

---

## Future Enhancements

Potential future additions include:

* Support for additional market data providers
* Macroeconomic features (FRED)
* Earnings and news sentiment
* Explainable AI with SHAP
* MLflow experiment tracking
* Docker support
* Interactive model evaluation dashboard
