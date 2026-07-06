# Project Architecture

## Purpose

The QQQ Outperformance Predictor is designed as a production-inspired machine learning system rather than a collection of scripts. The goal is to demonstrate software engineering, data engineering, machine learning, quantitative finance, and documentation best practices within a single cohesive project.

The system is intentionally modular so that each component has a single responsibility and can evolve independently as the project grows.

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

Separating responsibilities makes the project easier to test, maintain, and extend.

---

## Reproducibility

Every stage of the pipeline should be reproducible.

Rather than manually editing datasets, each stage consumes a well-defined input and produces a well-defined output.

This allows the pipeline to be rerun whenever improvements are made.

---

## Separation of Data and Logic

Raw data is never modified directly.

Instead, each processing stage creates a new representation of the data while preserving previous stages.

This makes debugging significantly easier and preserves the original source data.

---

## Configuration Management

Secrets and environment-specific configuration are never hardcoded.

Configuration is centralized through `.env` and `src/config.py`, allowing credentials and settings to be managed independently of the application logic.

---

# System Architecture

The planned high-level architecture is shown below.

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

# Repository Organization

The repository is organized around functional responsibilities.

```text
src/
│
├── data/
├── features/
├── models/
├── evaluation/
├── visualization/
└── utils/
```

Additional packages will be introduced as the project evolves, including a dedicated database layer.

---

# Data Flow

The intended data flow is:

1. Download historical market data from Alpaca.
2. Store raw data without modification.
3. Validate and clean the downloaded data.
4. Store validated data in a SQLite database.
5. Generate engineered features.
6. Generate prediction labels.
7. Assemble a machine learning dataset.
8. Train and evaluate models.
9. Record experiment results for comparison.

---

# Why SQLite?

The project uses SQLite because it provides:

* A lightweight relational database
* Strong SQL support
* Easy reproducibility
* No server installation
* Excellent integration with Python and pandas

SQLite is sufficient for a portfolio-scale project while still demonstrating practical database design and SQL skills.

---

# Future Evolution

The architecture is intentionally modular so that future improvements can be introduced without major redesign.

Potential enhancements include:

* Additional market data providers
* Automated data refresh
* More advanced feature engineering
* MLflow integration
* Explainable AI (SHAP)
* Interactive dashboards
* Cloud deployment

The objective is to evolve the project incrementally while maintaining clean architecture and reproducibility.
