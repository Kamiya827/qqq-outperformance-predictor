from src.database.queries import (
    get_all_prices,
    get_prices_for_ticker,
    get_price_history,
    list_available_tickers,
)


def main() -> None:
    tickers = list_available_tickers()
    print("Available tickers:")
    print(tickers)

    all_prices = get_all_prices()
    print("\nAll prices shape:")
    print(all_prices.shape)

    aapl_prices = get_prices_for_ticker("AAPL")
    print("\nAAPL prices shape:")
    print(aapl_prices.shape)

    aapl_history = get_price_history(
        ticker="AAPL",
        start_date="2020-01-01",
        end_date="2030-01-01",
    )
    print("\nAAPL history shape:")
    print(aapl_history.shape)

    print("\nSample rows:")
    print(aapl_history.head())


if __name__ == "__main__":
    main()