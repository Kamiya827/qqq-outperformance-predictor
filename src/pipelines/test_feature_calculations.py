from src.database.queries import get_all_prices
from src.features.technical import build_technical_features


def main() -> None:
    prices = get_all_prices()
    features = build_technical_features(prices)

    print(features.shape)
    print(features.head(25))
    print(features.isna().sum())


if __name__ == "__main__":
    main()