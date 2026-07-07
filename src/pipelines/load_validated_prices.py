from src.config import settings
from src.database.loaders import load_validated_prices
from src.database.schema import initialize_database


def main() -> None:
    initialize_database()

    file_path = (
        settings.project_root
        / "data"
        / "interim"
        / "daily_bars_validated.csv"
    )

    row_count = load_validated_prices(file_path)

    print(f"Loaded {row_count} rows into validated_prices.")


if __name__ == "__main__":
    main()