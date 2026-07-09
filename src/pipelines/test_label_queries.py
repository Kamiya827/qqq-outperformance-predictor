from src.database.queries import get_all_labels, get_labels_for_ticker


def main() -> None:
    labels = get_all_labels()
    print("All labels shape:")
    print(labels.shape)

    aapl_labels = get_labels_for_ticker("AAPL")
    print("\nAAPL labels shape:")
    print(aapl_labels.shape)

    print("\nAAPL sample:")
    print(aapl_labels.head())

    print("\nMissing values:")
    print(labels.isna().sum())

    print("\nLabel distribution:")
    print(labels["outperformed_qqq"].value_counts(dropna=False))


if __name__ == "__main__":
    main()