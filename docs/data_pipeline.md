# Data Pipeline

## Overview

The QQQ Outperformance Predictor follows a modular data engineering pipeline in which each stage has a single responsibility.

```text
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
SQLite Database
      │
      ▼
Feature Engineering
      │
      ▼
Label Generation
      │
      ▼
Training Dataset
      │
      ▼
Machine Learning
      │
      ▼
Experiment Tracking
```

## Current Status

Implemented:

- Historical market data download
- Data validation and cleaning
- SQLite database initialization
- Validated data loading into SQLite
- Reusable SQL query utilities

Planned:

- Feature engineering
- Label generation
- Model training
- Experiment tracking

Each pipeline stage is intentionally independent so that datasets can be regenerated without modifying previous stages, supporting reproducibility and maintainability.