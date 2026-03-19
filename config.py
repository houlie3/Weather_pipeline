from __future__ import annotations

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DOCS_DIR = BASE_DIR / "docs"
DATA_DIR = BASE_DIR / "data"
DOCS_DIR.mkdir(parents=True, exist_ok=True)
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Replace these coordinates with your real places.
# Format: "Label": (latitude, longitude)
LOCATIONS: dict[str, tuple[float, float]] = {
    "Birthplace": (57.0488, 9.9217),
    "Previous Residence": (56.5667, 9.0333),
    "Aalborg": (57.0488, 9.9217),
}

# Used inside the poem prompt. Change SECOND_LANGUAGE to your native language.
SECOND_LANGUAGE = "Danish"

SQL_DB_PATH = str(DATA_DIR / "weather.db")
POEM_TXT_PATH = DATA_DIR / "poem.txt"
HTML_OUTPUT_PATH = DOCS_DIR / "index.html"
