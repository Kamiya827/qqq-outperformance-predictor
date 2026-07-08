from src.database.loaders import load_features
from src.database.schema import initialize_database
from src.features.builder import build_features


def main() -> None:
    initialize_database()

    features = build_features()
    row_count = load_features(features)

    print(f"Generated and loaded {row_count} feature rows.")


if __name__ == "__main__":
    main()