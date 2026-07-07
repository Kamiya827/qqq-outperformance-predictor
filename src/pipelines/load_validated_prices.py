from src.database.loaders import load_validated_prices
from src.database.schema import initialize_database


def main() -> None:
    initialize_database()
    row_count = load_validated_prices()
    print(f"Loaded {row_count} rows into validated_prices.")


if __name__ == "__main__":
    main()