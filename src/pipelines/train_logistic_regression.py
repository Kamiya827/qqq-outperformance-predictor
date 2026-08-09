from src.dataset.builder import build_training_dataset
from src.models.baseline import build_logistic_regression
from src.evaluation.metrics import evaluate_binary_classifier
from src.models.preprocess import (
    prepare_features_and_labels,
    standardize_features,
)
from src.models.split import time_series_split


def main() -> None:
    dataset = build_training_dataset()

    train, test = time_series_split(dataset)

    X_train, y_train = prepare_features_and_labels(train)
    X_test, y_test = prepare_features_and_labels(test)

    X_train_scaled, X_test_scaled, _ = standardize_features(
        X_train,
        X_test,
    )

    model = build_logistic_regression()

    model.fit(X_train_scaled, y_train)

    predictions = model.predict(X_test_scaled)
    probabilities = model.predict_proba(X_test_scaled)[:, 1]

    metrics = evaluate_binary_classifier(
        y_true=y_test,
        y_pred=predictions,
        y_probability=probabilities,
    )

    print("Logistic Regression baseline")
    print("----------------------------")

    for metric_name, metric_value in metrics.items():
        print(f"{metric_name}: {metric_value:.4f}")


if __name__ == "__main__":
    main()