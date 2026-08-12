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

# Database Tables

The database architecture includes the following primary tables.

```text
stock_universe
raw_prices
validated_prices
features
labels
experiments
```

The current implementation includes `validated_prices`, `features`, and `labels`.

The model-ready training dataset is constructed dynamically by joining features and labels in the application layer rather than being stored as a separate database table or SQL view.

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
    ┌────────────────┐      ┌───────────────────────┐
    │ ticker         │      │ ticker                │
    │ timestamp      │      │ timestamp             │
    │ 14 engineered  │      │ forward_return_5d     │
    │ features       │      │ qqq_forward_return_5d │
    └────────┬───────┘      │ outperformed_qqq      │
             │              └───────────┬───────────┘
             └──────────────┬───────────┘
                            ▼
                   training_dataset
                   ──────────────────
                   Derived dynamically
                   from features + labels
                            │
                            ▼
                    Machine Learning
                            │
                            ▼
                       experiments
                      ─────────────
                      experiment_id
                      model_name
                      feature_set
                      hyperparameters
                      evaluation metrics
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

### Current Columns

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

The current validated market dataset contains 11 symbols: ten modeled stocks and QQQ as the benchmark.

The table contains 11,022 validated price observations covering 2022 through 2025.

---

## features

### Purpose

Stores engineered features used by machine learning models.

Separating engineered features from historical prices allows feature generation to evolve without modifying validated market data.

### Current Features

The current feature set contains 14 engineered features across three feature families.

#### Base Features

```text
return_1d
return_5d
sma_20
sma_50
ema_20
volatility_20
volume_ratio_20
```

#### Relative Trend Features

```text
price_to_sma_20
price_to_sma_50
price_to_ema_20
sma_20_to_sma_50
```

#### Benchmark-Relative Features

```text
relative_return_1d
relative_return_5d
relative_volatility_20
```

Benchmark-relative features compare each stock's behavior with QQQ, aligning the feature set more directly with the project's objective of predicting benchmark outperformance.

Feature definitions are centralized in:

```text
src/features/schema.py
```

### Primary Key

```text
(ticker, timestamp)
```

---

## labels

### Purpose

Stores the supervised learning target.

The label indicates whether a stock outperformed QQQ over the following five trading days.

### Current Columns

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

The binary target is defined as:

```text
outperformed_qqq = 1 if the stock's five-day forward return
                   exceeds QQQ's five-day forward return

outperformed_qqq = 0 otherwise
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

The exact experiment schema may evolve as the experiment tracking layer is implemented.

---

# Training Dataset Construction

Rather than physically storing the final machine learning dataset, the project dynamically joins engineered features with prediction labels.

Conceptually:

```sql
SELECT
    f.*,
    l.forward_return_5d,
    l.qqq_forward_return_5d,
    l.outperformed_qqq
FROM features AS f
JOIN labels AS l
    ON f.ticker = l.ticker
   AND f.timestamp = l.timestamp;
```

The current dataset builder performs this join in the application layer, removes observations with incomplete features or labels, and excludes QQQ from the prediction universe.

With the current ten-stock modeling universe, the resulting model-ready dataset contains:

```text
10 modeled stocks
948 observations per stock
9,480 total observations
```

This approach avoids duplicating data while providing a reproducible model-ready dataset.

A SQL view could be introduced later if it provides a practical advantage.

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

Construct the training dataset dynamically.

### Alternatives Considered

- Persist the training dataset as a separate table
- Create a permanent SQL view

### Reasoning

The training dataset is derived entirely from the `features` and `labels` tables. Constructing it dynamically avoids unnecessary data duplication and allows changes to feature engineering or label generation to flow naturally into model training.

A SQL view remains a possible future improvement if it simplifies downstream workflows.

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

# Current Implementation Status

The SQLite database layer is implemented and now supports feature engineering, label generation, training dataset construction, and downstream machine learning workflows.

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

Current implementation creates the following tables:

- `validated_prices`
- `features`
- `labels`

The feature schema has been extended as feature engineering has evolved, including support for relative trend and benchmark-relative features.

Future development may extend the schema with additional tables including:

- `stock_universe`
- `raw_prices`
- `experiments`

---

### loaders.py

Provides utilities for importing validated and derived datasets into SQLite.

Current functionality:

- Load validated market data into `validated_prices`
- Load engineered features into `features`
- Load prediction labels into `labels`
- Validate required columns before insertion
- Prevent duplicate records through primary key constraints

Future versions may support incremental updates and bulk loading optimizations.

---

### queries.py

Provides reusable SQL query functions for downstream pipeline stages including feature engineering, label generation, and model training.

Current functionality includes:

- Retrieve validated price history
- Retrieve engineered features
- Retrieve prediction labels
- Filter by ticker
- Filter by date range
- List available tickers

These reusable query functions are shared across the feature engineering, label generation, dataset builder, and machine learning pipelines.

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
  ┌───┴───────┐
  ▼           ▼
Features     Labels
  └─────┬──────┘
        ▼
Training Dataset Builder
        │
        ▼
Time-Series Validation
        │
        ▼
Machine Learning Models
```

The database now serves as the persistence layer between data validation and downstream machine learning workflows, reducing reliance on CSV files after ingestion.

---

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
