from src.database.queries import get_all_prices
from src.features.labels import build_outperformance_labels


def main() -> None:
    prices = get_all_prices()
    labels = build_outperformance_labels(prices)

    print(labels.shape)
    print(labels.head())
    print(labels.tail())
    print(labels.isna().sum())
    print(labels["outperformed_qqq"].value_counts(dropna=False))


if __name__ == "__main__":
    main()