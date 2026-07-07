# Database Design

## Objective

The SQLite database serves as the single source of truth for the QQQ Outperformance Predictor project.

Rather than relying on multiple CSV files throughout the machine learning pipeline, all validated and derived data will ultimately be stored in a relational database. This improves reproducibility, enables efficient SQL queries, and creates a clean separation between each stage of the pipeline.

The database stores:

* Stock universe metadata
* Raw market data
* Validated market data
* Engineered features
* Prediction labels
* Machine learning experiment results

The overall goal is to build a maintainable, reproducible, production-inspired data architecture while demonstrating practical SQL and database design skills.

---

# Design Principles

The database architecture follows several guiding principles.

## Single Source of Truth

SQLite serves as the authoritative source for all validated project data.

CSV files are treated as ingestion artifacts rather than permanent working datasets.

---

## Separation of Concerns

Each table has one clearly defined responsibility.

Market data, engineered features, labels, and experiment results are intentionally separated to make the pipeline easier to maintain and regenerate.

---

## Reproducibility

Every stage of the machine learning pipeline should be reproducible.

If feature engineering changes, features should be regenerated without modifying historical prices.

If validation rules improve, validated data should be regenerated from raw data rather than downloading data again.

---

## Normalization

The database avoids unnecessary duplication of information.

Company metadata is stored once.

Market prices are stored once.

Derived information is stored separately.

---

# Planned Database Tables

The database will contain the following primary tables.

```text
stock_universe
raw_prices
validated_prices
features
labels
experiments
```

A SQL view will later combine features and labels into a model-ready training dataset.

---

# Entity Relationship Diagram

```text
                     stock_universe
                    ────────────────
                    ticker (PK)
                    company_name
                    sector
                           │
                           │ ticker
                           ▼
                 validated_prices
          ┌────────────────────────────────┐
          │ ticker + timestamp (PK)        │
          │ open                           │
          │ high                           │
          │ low                            │
          │ close                          │
          │ volume                         │
          │ trade_count                    │
          │ vwap                           │
          └───────────────┬────────────────┘
                          │
              ┌───────────┴────────────┐
              ▼                        ▼
         features                  labels
    ┌────────────────┐      ┌────────────────────┐
    │ ticker         │      │ ticker             │
    │ timestamp      │      │ timestamp          │
    │ engineered     │      │ forward_return_5d │
    │ features...    │      │ qqq_return_5d      │
    └────────┬───────┘      │ outperformed_qqq   │
             │              └─────────┬──────────┘
             └──────────────┬─────────┘
                            ▼
                 training_dataset (VIEW)

                   experiments
```

---

# Table Specifications

## stock_universe

### Purpose

Stores metadata describing every security included in the project.

This table defines the machine learning universe independently from historical market data.

### Planned Columns

| Column       | Type             | Description         |
| ------------ | ---------------- | ------------------- |
| ticker       | TEXT PRIMARY KEY | Stock ticker symbol |
| company_name | TEXT             | Company name        |
| sector       | TEXT             | Market sector       |

### Example

| ticker | company_name          | sector     |
| ------ | --------------------- | ---------- |
| AAPL   | Apple Inc.            | Technology |
| MSFT   | Microsoft Corporation | Technology |
| QQQ    | Invesco QQQ Trust     | Benchmark  |

---

## raw_prices

### Purpose

Stores historical market data exactly as returned by Alpaca.

This table should never be manually modified.

If validation logic changes, this table remains unchanged.

### Planned Columns

| Column      | Type    |
| ----------- | ------- |
| ticker      | TEXT    |
| timestamp   | TEXT    |
| open        | REAL    |
| high        | REAL    |
| low         | REAL    |
| close       | REAL    |
| volume      | INTEGER |
| trade_count | INTEGER |
| vwap        | REAL    |

### Primary Key

```text
(ticker, timestamp)
```

---

## validated_prices

### Purpose

Stores cleaned and validated historical market data.

Validation may include:

* Removing duplicates
* Removing invalid prices
* Removing incomplete rows
* Standardizing timestamps
* Sorting observations

The schema intentionally mirrors `raw_prices` so validated data can easily replace raw data in downstream processing.

### Planned Columns

| Column      | Type    |
| ----------- | ------- |
| ticker      | TEXT    |
| timestamp   | TEXT    |
| open        | REAL    |
| high        | REAL    |
| low         | REAL    |
| close       | REAL    |
| volume      | INTEGER |
| trade_count | INTEGER |
| vwap        | REAL    |

### Primary Key

```text
(ticker, timestamp)
```

---

## features

### Purpose

Stores engineered features used by machine learning models.

Separating engineered features from historical prices allows feature generation to evolve without modifying validated market data.

### Example Features

| Feature                  |
| ------------------------ |
| return_1d                |
| return_5d                |
| SMA_20                   |
| SMA_50                   |
| EMA_20                   |
| RSI_14                   |
| MACD                     |
| ATR                      |
| Bollinger Bands          |
| Volatility               |
| Volume Ratio             |
| Relative Strength vs QQQ |

### Planned Columns

```text
ticker
timestamp
feature_name...
```

The exact feature schema will evolve as additional indicators are implemented.

### Primary Key

```text
(ticker, timestamp)
```

---

## labels

### Purpose

Stores the supervised learning target.

The label indicates whether a stock outperformed QQQ over the following five trading days.

### Planned Columns

| Column                | Type    |
| --------------------- | ------- |
| ticker                | TEXT    |
| timestamp             | TEXT    |
| forward_return_5d     | REAL    |
| qqq_forward_return_5d | REAL    |
| outperformed_qqq      | INTEGER |

### Primary Key

```text
(ticker, timestamp)
```

---

## experiments

### Purpose

Tracks every machine learning experiment.

This table functions as an experiment log rather than a software development log.

Each row represents one model training run.

### Planned Columns

| Column           | Type                              |
| ---------------- | --------------------------------- |
| experiment_id    | INTEGER PRIMARY KEY AUTOINCREMENT |
| run_timestamp    | TEXT                              |
| model_name       | TEXT                              |
| feature_set      | TEXT                              |
| train_start_date | TEXT                              |
| train_end_date   | TEXT                              |
| test_start_date  | TEXT                              |
| test_end_date    | TEXT                              |
| accuracy         | REAL                              |
| precision        | REAL                              |
| recall           | REAL                              |
| f1_score         | REAL                              |
| roc_auc          | REAL                              |
| hypothesis       | TEXT                              |
| conclusion       | TEXT                              |

---

# Planned Training Dataset View

Rather than physically storing the final machine learning dataset, the project will create a SQL view that joins engineered features with prediction labels.

Conceptually:

```sql
SELECT
    f.*,
    l.outperformed_qqq
FROM features AS f
JOIN labels AS l
    ON f.ticker = l.ticker
   AND f.timestamp = l.timestamp;
```

This approach avoids duplicating data while providing a model-ready dataset.

---

# Future Indexes

As the dataset grows, indexes will improve query performance.

Planned indexes include:

```text
validated_prices(ticker, timestamp)

features(ticker, timestamp)

labels(ticker, timestamp)

experiments(run_timestamp)
```

These indexes support efficient joins and time-series filtering.

---

# Key Design Decisions

## Decision

Use SQLite as the project's primary database.

### Alternatives Considered

* CSV files only
* PostgreSQL

### Reasoning

SQLite provides a lightweight relational database that requires no separate server, integrates seamlessly with Python, and demonstrates practical SQL skills. It is an excellent fit for a portfolio-scale machine learning project.

### Tradeoffs

SQLite is not intended for concurrent multi-user workloads. For this project's scope, simplicity and portability outweigh those limitations.

---

## Decision

Separate raw and validated market data.

### Alternatives Considered

* Store only validated data
* Overwrite raw data after cleaning

### Reasoning

Keeping raw data immutable allows validation logic to evolve without requiring new downloads from the data provider.

---

## Decision

Separate engineered features from price history.

### Alternatives Considered

* Store engineered features directly in the price table

### Reasoning

Engineered features are derived data. Keeping them separate makes feature regeneration straightforward and prevents accidental modification of validated market data.

---

## Decision

Store labels independently from engineered features.

### Alternatives Considered

* Append labels directly to the features table

### Reasoning

Features represent information available at prediction time, while labels depend on future information. Separating them reinforces the distinction between model inputs and targets and reduces the risk of introducing lookahead bias.

---

## Decision

Track machine learning experiments in the database.

### Alternatives Considered

* Manual notes
* Spreadsheet tracking
* No experiment logging

### Reasoning

Recording every experiment encourages reproducibility, simplifies model comparison, and demonstrates disciplined machine learning practices. A future iteration of the project may integrate MLflow while preserving this database-backed experiment history.

---

# Current Implementation Status (Sprint 4)

Sprint 4 introduces the initial SQLite database layer for the project.

## Implemented Components

The following modules have been added under `src/database/`:

```text
connection.py
schema.py
loaders.py
queries.py
```

### connection.py

Provides a centralized SQLite connection utility.

Responsibilities include:

- Creating database connections
- Enabling SQLite foreign key support
- Ensuring the database directory exists before connecting

---

### schema.py

Responsible for initializing the project database schema.

The initial implementation creates the `validated_prices` table, which stores cleaned historical market data produced by the validation pipeline.

Future sprints will extend this module to create additional tables including:

- stock_universe
- raw_prices
- features
- labels
- experiments

---

### loaders.py

Provides utilities for importing validated CSV files into SQLite.

Current functionality:

- Read validated CSV files
- Validate required columns
- Insert records into `validated_prices`
- Prevent duplicate records through primary key constraints

Future versions may support incremental updates and bulk loading optimizations.

---

### queries.py

Reserved for reusable SQL queries used by later stages of the machine learning pipeline.

Examples include:

- Retrieve historical prices
- Load feature generation windows
- Build training datasets
- Generate experiment summaries

---

## Database Location

The SQLite database is stored at:

```text
data/qqq_predictor.db
```

The location is configured centrally through `src/config.py`.

---

## Current Pipeline

The data pipeline currently follows this architecture:

```text
Alpaca API
      │
      ▼
Raw CSV Files
      │
      ▼
Validation Pipeline
      │
      ▼
Validated CSV Files
      │
      ▼
SQLite Database
      │
      ▼
Feature Engineering (next)
```

The database now serves as the persistence layer between data validation and feature engineering, reducing reliance on CSV files during downstream processing.


# Future Evolution

The database is intentionally designed to evolve over time.

Potential future additions include:

* Fundamental company data
* Macroeconomic indicators (FRED)
* Earnings information
* News sentiment
* Multiple benchmark ETFs
* Alternative prediction horizons
* Portfolio optimization tables
* MLflow integration
* Automated experiment reporting

The schema will continue to evolve while maintaining the guiding principles of modularity, reproducibility, and maintainability.
