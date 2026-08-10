"""
Compare feature sets across baseline machine learning models.
"""

import pandas as pd

from src.dataset.builder import build_training_dataset
from src.evaluation.cross_validation import (
    cross_validate_model,
    summarize_cross_validation,
)
from src.features.schema import (
    BASE_FEATURE_COLUMNS,
    FEATURE_COLUMNS,
    RELATIVE_TREND_FEATURE_COLUMNS,
)
from src.models.baseline import (
    build_decision_tree,
    build_gradient_boosting,
    build_logistic_regression,
    build_random_forest,
)


def main() -> None:
    dataset = build_training_dataset()

    feature_sets = [
        {
            "name": "Base",
            "columns": BASE_FEATURE_COLUMNS,
        },
        {
            "name": "Relative Trend",
            "columns": RELATIVE_TREND_FEATURE_COLUMNS,
        },
        {
            "name": "Combined",
            "columns": FEATURE_COLUMNS,
        },
    ]

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

    for feature_set in feature_sets:
        for model_config in model_configs:
            results = cross_validate_model(
                dataset=dataset,
                model_builder=model_config["builder"],
                model_name=model_config["name"],
                feature_columns=feature_set["columns"],
                scale_features=model_config["scale_features"],
            )

            summary = summarize_cross_validation(results)

            comparison_rows.append(
                {
                    "feature_set": feature_set["name"],
                    "model": model_config["name"],
                    "feature_count": len(feature_set["columns"]),
                    "accuracy_mean": summary.loc["accuracy", "mean"],
                    "f1_mean": summary.loc["f1_score", "mean"],
                    "roc_auc_mean": summary.loc["roc_auc", "mean"],
                    "roc_auc_std": summary.loc["roc_auc", "std"],
                }
            )

    comparison = pd.DataFrame(comparison_rows)

    print("\nFeature ablation comparison")
    print("-" * 80)

    print(
        comparison.sort_values(
            "roc_auc_mean",
            ascending=False,
        ).to_string(index=False)
    )


if __name__ == "__main__":
    main()