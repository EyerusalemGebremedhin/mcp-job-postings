"""Loads the sample postings from data/postings.json."""
import json
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "postings.json"


def load_postings() -> list[dict]:
    """Read the postings file once and return it as a list of dictionaries."""
    return json.loads(DATA_FILE.read_text(encoding="utf-8"))
