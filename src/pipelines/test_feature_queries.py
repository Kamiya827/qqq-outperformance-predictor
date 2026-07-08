from src.database.queries import get_all_features, get_features_for_ticker


def main() -> None:
    all_features = get_all_features()
    print("All features shape:")
    print(all_features.shape)

    aapl_features = get_features_for_ticker("AAPL")
    print("\nAAPL features shape:")
    print(aapl_features.shape)

    print("\nAAPL sample:")
    print(aapl_features.head())

    print("\nMissing values:")
    print(aapl_features.isna().sum())


if __name__ == "__main__":
    main()