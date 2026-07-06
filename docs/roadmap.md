Documentation will be added as this component of the project is implemented.# Project Roadmap

## Vision

Build a production-inspired machine learning platform that predicts whether an individual stock will outperform the QQQ ETF over the next five trading days.

The project is designed to demonstrate software engineering, data engineering, machine learning, quantitative finance, and SQL skills through a single cohesive portfolio project.

Rather than optimizing for trading performance alone, the emphasis is on building a reproducible, maintainable, and well-documented machine learning system.

---

# Guiding Principles

The project follows several guiding principles throughout development.

* Build a maintainable software system rather than isolated scripts.
* Prioritize reproducibility and documentation.
* Avoid data leakage and lookahead bias.
* Validate every stage before building the next.
* Prefer modular, reusable components.
* Learn and apply concepts from coursework in a realistic setting.
* Make every design decision explainable in a technical interview.

---

# Development Phases

## Phase 1 — Foundation [x]

### Objectives

* Establish repository structure
* Configure Python development environment
* Implement Git workflow
* Create modular project architecture
* Configure Alpaca API
* Build data ingestion pipeline
* Build validation pipeline
* Establish documentation structure

### Status

**Complete**

---

## Phase 2 — Data Engineering

### Objectives

* Design SQLite database schema
* Build database connection layer
* Create database initialization scripts
* Load validated market data into SQLite
* Build SQL query layer
* Create reusable data access utilities

### Status

**Current Phase**

---

## Phase 3 — Feature Engineering

### Objectives

* Generate return-based features
* Moving averages
* Momentum indicators
* Volatility indicators
* Volume-based features
* Relative strength features
* Rolling window features

### Status

Planned

---

## Phase 4 — Label Engineering

### Objectives

* Generate forward returns
* Calculate QQQ benchmark returns
* Build binary classification labels
* Assemble supervised learning dataset

### Status

Planned

---

## Phase 5 — Exploratory Data Analysis

### Objectives

* Explore distributions
* Analyze class balance
* Investigate correlations
* Identify outliers
* Visualize feature relationships

### Status

Planned

---

## Phase 6 — Machine Learning

### Objectives

* Logistic Regression baseline
* Decision Tree
* Random Forest
* Gradient Boosting
* Hyperparameter tuning
* Feature selection

### Status

Planned

---

## Phase 7 — Evaluation

### Objectives

* Time-series train/test split
* Walk-forward validation
* Precision
* Recall
* F1 Score
* ROC-AUC
* Feature importance
* Error analysis

### Status

Planned

---

## Phase 8 — Experiment Tracking

### Objectives

* Log every training run
* Record feature sets
* Record hyperparameters
* Record evaluation metrics
* Track hypotheses
* Record conclusions

### Status

Planned

---

## Phase 9 — Documentation

### Objectives

* Final architecture documentation
* Database documentation
* Feature documentation
* Model documentation
* Final project report

### Status

Ongoing throughout the project

---

# Current Sprint

## Sprint 4 — Database Design

### Goal

Design and implement a SQLite database that becomes the single source of truth for the entire machine learning pipeline.

### Deliverables

* Database schema
* Database package
* Database initialization script
* Data loading pipeline
* SQL query layer

---

# Completed Milestones

* Repository initialized
* Git workflow established
* Python 3.11 environment configured
* Modular project architecture created
* Centralized configuration system
* Alpaca API integration
* Stock universe management
* Historical data download pipeline
* Data validation pipeline
* Initial project documentation

---

# Next Milestones

1. Design SQLite schema
2. Create database layer
3. Load validated market data
4. Build SQL query interface
5. Generate prediction labels
6. Engineer features
7. Perform exploratory data analysis
8. Train baseline models

---

# Stretch Goals

After the core project is complete, potential extensions include:

* Additional data providers
* Macroeconomic indicators (FRED)
* Earnings data
* News sentiment
* Explainable AI (SHAP)
* MLflow integration
* Docker support
* Interactive dashboard
* Cloud deployment

---

# Idea Backlog

Ideas that may be valuable in future iterations:

* Dynamic stock universe updates
* Alternative benchmark ETFs
* Multi-horizon prediction (1, 5, 10, and 20 trading days)
* Portfolio-level optimization
* Sector-relative performance prediction
* Feature importance dashboard
* Automated experiment reports
* Scheduled data refresh pipeline

---

# Sprint Workflow

Every sprint follows the same development cycle:

1. Define the objective.
2. Discuss design alternatives and tradeoffs.
3. Implement the solution.
4. Validate correctness.
5. Document architectural decisions.
6. Commit logical milestones.
7. Conduct a sprint retrospective.

Following a consistent workflow keeps the project reproducible, maintainable, and aligned with professional software engineering practices.
