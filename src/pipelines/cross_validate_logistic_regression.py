"""
Evaluate the Logistic Regression baseline using time-series cross-validation.
"""

import pandas as pd

from src.dataset.builder import build_training_dataset
from src.models.baseline import build_logistic_regression
from src.models.evaluate import evaluate_binary_classifier
from src.models.preprocess import (
    prepare_features_and_labels,
    standardize_features,
)
from src.models.split import time_series_cross_validation


def main() -> None:
    dataset = build_training_dataset()

    folds = time_series_cross_validation(
        dataset,
        n_splits=5,
        gap=5,
    )

    fold_results = []

    for fold_number, (train, validation) in enumerate(folds, start=1):
        X_train, y_train = prepare_features_and_labels(train)
        X_validation, y_validation = prepare_features_and_labels(validation)

        X_train_scaled, X_validation_scaled, _ = standardize_features(
            X_train,
            X_validation,
        )

        model = build_logistic_regression()
        model.fit(X_train_scaled, y_train)

        predictions = model.predict(X_validation_scaled)
        probabilities = model.predict_proba(X_validation_scaled)[:, 1]

        metrics = evaluate_binary_classifier(
            y_true=y_validation,
            y_pred=predictions,
            y_probability=probabilities,
        )

        metrics["fold"] = fold_number
        fold_results.append(metrics)

        print(f"\nFold {fold_number}")
        print("-" * 30)

        for metric_name, metric_value in metrics.items():
            if metric_name != "fold":
                print(f"{metric_name}: {metric_value:.4f}")

    results = pd.DataFrame(fold_results).set_index("fold")

    print("\nCross-validation summary")
    print("-" * 30)

    summary = pd.DataFrame(
        {
            "mean": results.mean(),
            "std": results.std(),
        }
    )

    print(summary)


if __name__ == "__main__":
    main()