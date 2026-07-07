from src.database.schema import initialize_database


def main() -> None:
    initialize_database()
    print("Database initialized successfully.")


if __name__ == "__main__":
    main()