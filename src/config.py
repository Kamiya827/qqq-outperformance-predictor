from dataclasses import dataclass
from pathlib import Path
import os

from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parents[1]
load_dotenv(PROJECT_ROOT / ".env")


@dataclass(frozen=True)
class Settings:
    alpaca_api_key: str
    alpaca_secret_key: str
    alpaca_base_url: str
    project_root: Path
    raw_data_dir: Path
    processed_data_dir: Path
    database_path: Path


def get_settings() -> Settings:
    api_key = os.getenv("ALPACA_API_KEY")
    secret_key = os.getenv("ALPACA_SECRET_KEY")
    base_url = os.getenv("ALPACA_BASE_URL", "https://paper-api.alpaca.markets")

    if not api_key:
        raise ValueError("Missing ALPACA_API_KEY in .env")

    if not secret_key:
        raise ValueError("Missing ALPACA_SECRET_KEY in .env")

    return Settings(
        alpaca_api_key=api_key,
        alpaca_secret_key=secret_key,
        alpaca_base_url=base_url,
        project_root=PROJECT_ROOT,
        raw_data_dir=PROJECT_ROOT / "data" / "raw",
        processed_data_dir=PROJECT_ROOT / "data" / "processed",
        database_path=PROJECT_ROOT / "data" / "qqq_predictor.db",
    )


settings = get_settings()