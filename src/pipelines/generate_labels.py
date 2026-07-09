from src.database.loaders import load_labels
from src.database.queries import get_all_prices
from src.database.schema import initialize_database
from src.features.labels import build_outperformance_labels


def main() -> None:
    initialize_database()

    prices = get_all_prices()
    labels = build_outperformance_labels(prices)

    row_count = load_labels(labels)

    print(f"Generated and loaded {row_count} label rows.")


if __name__ == "__main__":
    main()