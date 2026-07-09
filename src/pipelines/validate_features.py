from src.database.queries import get_all_features
from src.features.validate import validate_features


def main() -> None:
    features = get_all_features()
    report = validate_features(features)

    print("Feature validation report:")
    print(report)

    if report["errors"]:
        raise ValueError(f"Feature validation failed: {report['errors']}")


if __name__ == "__main__":
    main()