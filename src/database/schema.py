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

CREATE_FEATURES_TABLE = """
CREATE TABLE IF NOT EXISTS features (

    ticker TEXT NOT NULL,

    timestamp TEXT NOT NULL,

    return_1d REAL,

    return_5d REAL,

    sma_20 REAL,

    sma_50 REAL,

    ema_20 REAL,

    volatility_20 REAL,

    volume_ratio_20 REAL,

    PRIMARY KEY (ticker, timestamp),

    FOREIGN KEY (ticker, timestamp)
        REFERENCES validated_prices (ticker, timestamp)

);
"""

CREATE_LABELS_TABLE = """
CREATE TABLE IF NOT EXISTS labels (

    ticker TEXT NOT NULL,

    timestamp TEXT NOT NULL,

    forward_return_5d REAL,

    qqq_forward_return_5d REAL,

    outperformed_qqq INTEGER,

    PRIMARY KEY (ticker, timestamp),

    FOREIGN KEY (ticker, timestamp)
        REFERENCES validated_prices (ticker, timestamp)

);
"""


def initialize_database() -> None:
    """
    Create every table required by the project.
    """

    with get_connection() as connection:

        connection.execute(CREATE_VALIDATED_PRICES_TABLE)
        connection.execute(CREATE_FEATURES_TABLE)
        connection.execute(CREATE_LABELS_TABLE)
        
        connection.commit()