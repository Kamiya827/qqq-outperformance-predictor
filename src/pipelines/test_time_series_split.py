from src.dataset.builder import build_training_dataset
from src.models.split import time_series_split


def main() -> None:
    dataset = build_training_dataset()

    train, test = time_series_split(dataset)

    print("Train shape:", train.shape)
    print("Test shape:", test.shape)

    print("\nTrain date range:")
    print(train["timestamp"].min())
    print(train["timestamp"].max())

    print("\nTest date range:")
    print(test["timestamp"].min())
    print(test["timestamp"].max())

    overlap = (
        train["timestamp"].max() >= test["timestamp"].min()
    )

    print("\nChronological overlap:", overlap)


if __name__ == "__main__":
    main()