from src.dataset.builder import build_training_dataset


def main() -> None:
    dataset = build_training_dataset()

    print("Training dataset shape:")
    print(dataset.shape)

    print("\nColumns:")
    print(dataset.columns.tolist())

    print("\nSample:")
    print(dataset.head())

    print("\nMissing values:")
    print(dataset.isna().sum())

    print("\nLabel distribution:")
    print(dataset["outperformed_qqq"].value_counts())


if __name__ == "__main__":
    main()