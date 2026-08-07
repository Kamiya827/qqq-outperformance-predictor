from src.dataset.builder import build_training_dataset
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

    print("Training features shape:")
    print(X_train.shape)

    print("\nTesting features shape:")
    print(X_test.shape)

    print("\nTraining labels shape:")
    print(y_train.shape)

    print("\nTesting labels shape:")
    print(y_test.shape)

    print("\nScaled training shape:")
    print(X_train_scaled.shape)

    print("\nScaled testing shape:")
    print(X_test_scaled.shape)

    print("\nFeature columns:")
    print(X_train.columns.tolist())


if __name__ == "__main__":
    main()