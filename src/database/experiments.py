"""
Utilities for storing and retrieving machine learning experiment results.
"""

from datetime import datetime, timezone

import pandas as pd

from src.database.connection import get_connection


def log_experiment(
    *,
    experiment_type: str,
    model_name: str,
    feature_set: str,
    feature_count: int,
    dataset_rows: int,
    dataset_tickers: int,
    n_splits: int,
    gap: int,
    summary: pd.DataFrame,
    hypothesis: str | None = None,
    conclusion: str | None = None,
) -> int:
    """
    Persist a cross-validation experiment summary.

    Parameters
    ----------
    experiment_type : str
        Category of experiment, such as baseline comparison or feature ablation.
    model_name : str
        Human-readable model name.
    feature_set : str
        Name of the evaluated feature set.
    feature_count : int
        Number of model features used.
    dataset_rows : int
        Number of observations in the model-ready dataset.
    dataset_tickers : int
        Number of modeled securities in the dataset.
    n_splits : int
        Number of chronological cross-validation folds.
    gap : int
        Number of trading timestamps excluded between training and validation.
    summary : pd.DataFrame
        Cross-validation summary containing mean and std columns.
    hypothesis : str | None
        Optional experiment hypothesis.
    conclusion : str | None
        Optional experiment conclusion.

    Returns
    -------
    int
        Database ID of the inserted experiment.
    """
    required_metrics = {
        "accuracy",
        "precision",
        "recall",
        "f1_score",
        "roc_auc",
    }

    missing_metrics = required_metrics - set(summary.index)
    if missing_metrics:
        raise ValueError(
            f"Cross-validation summary is missing metrics: {missing_metrics}"
        )

    required_columns = {"mean", "std"}
    missing_columns = required_columns - set(summary.columns)
    if missing_columns:
        raise ValueError(
            f"Cross-validation summary is missing columns: {missing_columns}"
        )

    run_timestamp = datetime.now(timezone.utc).isoformat()

    insert_sql = """
    INSERT INTO experiments (
        run_timestamp,
        experiment_type,
        model_name,
        feature_set,
        feature_count,
        dataset_rows,
        dataset_tickers,
        n_splits,
        gap,
        accuracy_mean,
        accuracy_std,
        precision_mean,
        precision_std,
        recall_mean,
        recall_std,
        f1_mean,
        f1_std,
        roc_auc_mean,
        roc_auc_std,
        hypothesis,
        conclusion
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """

    values = (
        run_timestamp,
        experiment_type,
        model_name,
        feature_set,
        feature_count,
        dataset_rows,
        dataset_tickers,
        n_splits,
        gap,
        float(summary.loc["accuracy", "mean"]),
        float(summary.loc["accuracy", "std"]),
        float(summary.loc["precision", "mean"]),
        float(summary.loc["precision", "std"]),
        float(summary.loc["recall", "mean"]),
        float(summary.loc["recall", "std"]),
        float(summary.loc["f1_score", "mean"]),
        float(summary.loc["f1_score", "std"]),
        float(summary.loc["roc_auc", "mean"]),
        float(summary.loc["roc_auc", "std"]),
        hypothesis,
        conclusion,
    )

    with get_connection() as connection:
        cursor = connection.execute(insert_sql, values)
        connection.commit()

        return cursor.lastrowid


def get_experiments() -> pd.DataFrame:
    """
    Return all stored experiments ordered by most recent run.
    """
    query = """
    SELECT *
    FROM experiments
    ORDER BY experiment_id DESC;
    """

    with get_connection() as connection:
        return pd.read_sql_query(query, connection)

def get_best_experiments(
    limit: int = 10,
    experiment_type: str | None = None,
) -> pd.DataFrame:
    """
    Return the highest-performing experiments ranked by mean ROC-AUC.

    Parameters
    ----------
    limit : int
        Maximum number of experiment rows to return.
    experiment_type : str | None
        Optional experiment category used to filter results.

    Returns
    -------
    pd.DataFrame
        Experiment records ordered by descending mean ROC-AUC.
    """
    if limit <= 0:
        raise ValueError("limit must be greater than 0.")

    if experiment_type is None:
        query = """
        SELECT *
        FROM experiments
        ORDER BY roc_auc_mean DESC
        LIMIT ?;
        """

        parameters = (limit,)

    else:
        query = """
        SELECT *
        FROM experiments
        WHERE experiment_type = ?
        ORDER BY roc_auc_mean DESC
        LIMIT ?;
        """

        parameters = (
            experiment_type,
            limit,
        )

    with get_connection() as connection:
        return pd.read_sql_query(
            query,
            connection,
            params=parameters,
        )