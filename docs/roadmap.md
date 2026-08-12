# Project Roadmap

## Vision

Build a production-inspired machine learning platform that predicts whether an individual stock will outperform the QQQ ETF over the next five trading days.

The project is designed to demonstrate software engineering, data engineering, machine learning, quantitative finance, and SQL skills through a single cohesive portfolio project.

Rather than optimizing for trading performance alone, the emphasis is on building a reproducible, maintainable, leakage-safe, and well-documented machine learning system.

---

# Guiding Principles

The project follows several guiding principles throughout development.

* Build a maintainable software system rather than isolated scripts.
* Prioritize reproducibility and documentation.
* Avoid data leakage and lookahead bias.
* Evaluate financial models chronologically rather than with random data splits.
* Test apparent signals across multiple securities before assuming they generalize.
* Establish predictive signal before aggressively tuning model complexity.
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

**Complete**

---

## Phase 3 — Feature Engineering

### Objectives

* Generate return-based features
* Generate moving-average features
* Generate volatility features
* Generate volume-based features
* Generate normalized trend features
* Generate benchmark-relative features
* Centralize feature definitions
* Persist engineered features
* Support feature-set ablation

### Status

**Complete - Initial Feature Set**

The current system contains 14 engineered features across:

```text
Base
Relative Trend
Benchmark Relative
Stationary
Combined
```

Additional feature engineering remains an ongoing modeling activity.

---

## Phase 4 — Label Engineering

### Objectives

* Generate five-day forward stock returns
* Calculate five-day QQQ benchmark returns
* Build binary outperformance labels
* Persist labels
* Assemble supervised learning dataset

### Status

**Complete**

The prediction target is:

```text
1 = stock outperforms QQQ over the next five trading days
0 = stock does not outperform QQQ over the next five trading days
```

---

## Phase 5 — Exploratory Data Analysis

### Objectives

* Explore feature distributions
* Analyze class balance
* Investigate correlations
* Identify outliers
* Compare securities
* Visualize feature relationships
* Examine feature behavior across market periods

### Status

**Planned**

Exploratory analysis remains useful, but development has prioritized establishing a correct end-to-end modeling and evaluation pipeline first.

---

## Phase 6 — Machine Learning

### Objectives

* Build shared preprocessing utilities
* Implement Logistic Regression baseline
* Implement Decision Tree
* Implement Random Forest
* Implement Gradient Boosting
* Compare baseline models
* Support configurable feature subsets
* Perform feature-ablation experiments

### Status

**Complete - Baseline Stage**

The baseline modeling framework is operational across the expanded stock universe.

Initial results indicate that the current engineered features provide only weak out-of-sample predictive signal.

Hyperparameter optimization has intentionally been deferred until stronger generalizable signal is identified.

---

## Phase 7 — Evaluation

### Objectives

* Build panel-safe chronological train/test splitting
* Build time-series cross-validation
* Maintain all securities from the same trading date in the same partition
* Add a gap appropiate for the prediction horizon
* Evaluate accuracy
* Evaluate precision
* Evaluate recall
* Evaluate F1 Score
* Evaluate ROC-AUC
* Compare performance across folds
* Compare feature sets

### Status

**Core Evaluation Complete**

The current evaluation framework uses:

```text
5 chronological cross-validation folds
5 trading-timestamp gap
Expanding training window
```

The five-timestamp gap accounts for the five-trading-day prediction horizon.

Remaining evaluation work includes:

- Feature importance
- Error analysis
- Final untouched holdout evaluation
- Trading-oriented evaluation metrics

---

## Phase 8 — Experiment Tracking

### Objectives

* Persist training runs
* Record model names
* Record feature sets
* Record hyperparameters
* Record evaluation metrics
* Record cross-validation results
* Track experiment hypotheses
* Record conclusions
* Enable comparison between experiments

### Status

**Next Major Phase**

Current comparison pipelines can run experiments, but results are not yet persisted in a structured experiment-tracking system.

---

## Phase 9 — Signal Development

### Objectives

* Investigate additional predictive feature families
* Evaluate momentum signals
* Evaluate additional volatility signals
* Evaluate market regime features
* Evaluate additional benchmark-relative signals
* Perform feature importance analysis
* Perform controlled feature selection
* Test whether signals generalize across securities and market periods

### Status

**Planned**

The objective of this phase is to improve predictive signal before investing heavily in model optimization.

---

## Phase 10 — Model Optimization

### Objectives

* Tune promising baseline models
* Compare optimized models against baseline results
* Evaluate model stability across time
* Calibrate probability outputs if necessary
* Select a final candidate model

### Status

**Planned**

Model optimization should begin only after feature development produces evidence of meaningful out-of-sample signal.

---

## Phase 11 — Strategy Evaluation

### Objectives

* Convert model probabilities into stock rankings
* Define trading rules
* Build portfolio construction logic
* Backtest model-driven selections
* Compare strategy returns against QQQ
* Measure drawdown
* Measure turnover
* Incorporate transaction-cost assumptions
* Evaluate risk-adjusted performance

### Status

**Planned**

Classification performance alone is not sufficient to determine whether the model has practical investment value.

---

## Phase 12 — Final Documentation

### Objectives

* Final architecture documentation
* Finalize database documentation
* Finalize feature documentation
* Finalize model documentation
* Document experiments
* Document final model selection
* Document strategy evaluation
* Produce final project report

### Status

**Ongoing Throughout Development**

Documentation is updated at major architectural and experimental checkpoints rather than postponed until project completion.

---

# Current Development State

The project currently supports an end-to-end workflow:

```text
Stock Universe
      ↓
Alpaca Market Data
      ↓
Validation & Cleaning
      ↓
SQLite Persistence
      ↓
Feature Engineering
      ↓
Label Engineering
      ↓
Training Dataset
      ↓
Chronological Cross-Validation
      ↓
Baseline Models
      ↓
Feature Ablation
```

The development universe currently contains:

```text
10 modeled stocks
+ QQQ benchmark
```

The database contains:

```text
11,022 validated market observations
11,022 feature rows
11,022 label rows
```

The final model-ready dataset contains:

```text
948 observations per modeled stock
9,480 total observations
```

---

# Current Sprint

## Sprint 7 - Experiment Tracking

### Goal

Build a reproducible experiment-tracking layer so modeling decisions and results can be compared systematically as feature engineering continues.

### Deliverables

* Define experiment record structure
* Persist experiment metadata
* Record model configuration
* Record feature-set configuration
* Record cross-validation metrics
* Record experiment hypotheses and conclusions
* Build reusable experiment comparison utilities
* Connect existing baseline and feature-ablation pipelines to experiment tracking

### Success Criteria

A completed experiment should be reproducible from its recorded configuration and comparable against previous experiments without relying on terminal output or manual notes.

---

# Completed Milestones

* Repository initialized
* Git workflow established
* Python 3.11 environment configured
* Modular project architecture created
* Centralized configuration system
* Alpaca API integration
* Stock universe management
* Historical market data download pipeline
* Raw data preservation
* Data validation and cleaning pipeline
* Initial project documentation
* SQLite database layer
* Database schema initialization
* Validated data loading pipeline
* SQL query utilities
* End-to-end data pipeline from raw CSV to SQLite
* Feature engineering pipeline
* Base technical features
* Relative trend features
* Benchmark-relative features
* Feature persistence
* Feature validation
* Labels table
* Label generation pipeline
* Training dataset builder
* Expansion from initial development data to ten modeled stocks
* 9,480-observation model-ready dataset
* Panel-safe chronological holdout splitting
* Time-series cross-validation
* Five-trading-day cross-validation gap
* Shared model preprocessing
* Logistic Regression baseline
* Decision Tree baseline
* Random Forest baseline
* Gradient Boosting baseline
* Shared model evaluation
* Baseline model comparison
* Feature-set ablation
* Expanded-universe signal evaluation

---

# Key Finding So Far

The project initially identified apparently stronger performance from some feature configurations on the smaller development dataset.

After expanding the stock universe to ten securities, most of that apparent advantage disappeared.

Current baseline ROC-AUC performance remains close to random classification across the expanded universe.

This result changed the development priority from:

```text
Tune the best model
```

to:

```text
Improve experiment infrastructure
        ↓
Develop better features
        ↓
Validate generalizable signal
        ↓
Then optimize models
```

This prevents model complexity and hyperparameter tuning from being used to compensate for weak underlying predictive information.

---

# Next Milestones

1. Build persistent experiment tracking.
2. Record the existing baseline and feature-ablation experiments.
3. Perform exploratory analysis targeted at signal discovery.
4. Develop additional feature families.
5. Evaluate feature importance and feature selection.
6. Re-run controlled feature-ablation experiments.
7. Begin model optimization only if stronger out-of-sample signal emerges.
8. Preserve a final holdout period for final model evaluation.
9. Build probability-based stock ranking.
10. Develop portfolio backtesting and strategy evaluation.

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
* Automated data refresh
* Cloud deployment

---

# Idea Backlog

Ideas that may be valuable in future iterations:

* Dynamic stock universe updates
* Larger prediction universe
* Alternative benchmark ETFs
* Multi-horizon prediction (1, 5, 10, and 20 trading days)
* Portfolio-level optimization
* Sector-relative performance prediction
* Feature importance dashboard
* Automated experiment reports
* Scheduled data refresh pipeline
* Market regime classification
* Cross-sectional ranking models

These ideas remain outside the core implementation until the existing modeling pipeline demonstrates sufficiently reliable signal.

---

# Sprint Workflow

Every sprint follows the same development cycle:

1. Define the objective.
2. Discuss design alternatives and tradeoffs.
3. Implement the solution.
4. Validate correctness.
5. Evaluate results.
6. Document architectural decisions.
7. Commit logical milestones.
8. Conduct a sprint retrospective.

Following a consistent workflow keeps the project reproducible, maintainable, and aligned with professional software engineering practices.
