from pathlib import Path
import sqlite3

from src.config import settings


def get_connection(
    db_path: Path = settings.database_path,
) -> sqlite3.Connection:
    """
    Create and return a SQLite database connection.

    Parameters
    ----------
    db_path : Path
        Location of the SQLite database.

    Returns
    -------
    sqlite3.Connection
        Active database connection.
    """

    db_path.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(db_path)

    # Enable SQLite foreign key constraints
    connection.execute("PRAGMA foreign_keys = ON;")

    return connection