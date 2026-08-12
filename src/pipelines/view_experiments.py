"""
Display stored machine learning experiment results.
"""

from src.database.experiments import (
    get_best_experiments,
    get_experiments,
)


DISPLAY_COLUMNS = [
    "experiment_id",
    "experiment_type",
    "feature_set",
    "model_name",
    "feature_count",
    "dataset_rows",
    "dataset_tickers",
    "roc_auc_mean",
    "roc_auc_std",
]


def main() -> None:
    """
    Display experiment history and the highest-performing experiments.
    """
    experiments = get_experiments()

    print("\nExperiment tracking summary")
    print("-" * 80)

    print(f"Total experiments: {len(experiments)}")

    if experiments.empty:
        print("No experiments have been recorded.")
        return

    print("\nExperiments by type:")
    print(
        experiments["experiment_type"]
        .value_counts()
        .to_string()
    )

    best_experiments = get_best_experiments(limit=10)

    display = best_experiments[DISPLAY_COLUMNS].copy()

    display["roc_auc_mean"] = display["roc_auc_mean"].round(4)
    display["roc_auc_std"] = display["roc_auc_std"].round(4)

    print("\nTop experiments by ROC-AUC")
    print("-" * 80)

    print(
        display.to_string(
            index=False,
        )
    )


if __name__ == "__main__":
    main()