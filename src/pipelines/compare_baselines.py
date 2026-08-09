"""
Compare baseline machine learning models using time-series cross-validation.
"""

import pandas as pd

from src.dataset.builder import build_training_dataset
from src.evaluation.cross_validation import (
    cross_validate_model,
    summarize_cross_validation,
)
from src.models.baseline import (
    build_decision_tree,
    build_gradient_boosting,
    build_logistic_regression,
    build_random_forest,
)


def main() -> None:
    dataset = build_training_dataset()

    model_configs = [
        {
            "name": "Logistic Regression",
            "builder": build_logistic_regression,
            "scale_features": True,
        },
        {
            "name": "Decision Tree",
            "builder": build_decision_tree,
            "scale_features": False,
        },
        {
            "name": "Random Forest",
            "builder": build_random_forest,
            "scale_features": False,
        },
        {
            "name": "Gradient Boosting",
            "builder": build_gradient_boosting,
            "scale_features": False,
        },
    ]

    comparison_rows = []

    for config in model_configs:
        results = cross_validate_model(
            dataset=dataset,
            model_builder=config["builder"],
            model_name=config["name"],
            scale_features=config["scale_features"],
        )

        summary = summarize_cross_validation(results)

        print(f"\n{config['name']}")
        print("-" * 30)
        print(summary)

        comparison_rows.append(
            {
                "model": config["name"],
                "accuracy_mean": summary.loc["accuracy", "mean"],
                "f1_mean": summary.loc["f1_score", "mean"],
                "roc_auc_mean": summary.loc["roc_auc", "mean"],
                "roc_auc_std": summary.loc["roc_auc", "std"],
            }
        )

    comparison = pd.DataFrame(comparison_rows)

    print("\nBaseline model comparison")
    print("-" * 30)

    print(
        comparison.sort_values(
            "roc_auc_mean",
            ascending=False,
        ).to_string(index=False)
    )


if __name__ == "__main__":
    main()