from src.database.connection import get_connection


CREATE_VALIDATED_PRICES_TABLE = """
CREATE TABLE IF NOT EXISTS validated_prices (

    ticker TEXT NOT NULL,

    timestamp TEXT NOT NULL,

    open REAL NOT NULL,

    high REAL NOT NULL,

    low REAL NOT NULL,

    close REAL NOT NULL,

    volume INTEGER NOT NULL,

    trade_count INTEGER,

    vwap REAL,

    PRIMARY KEY (ticker, timestamp)

);
"""


def initialize_database() -> None:
    """
    Create every table required by the project.
    """

    with get_connection() as connection:

        connection.execute(CREATE_VALIDATED_PRICES_TABLE)

        connection.commit()