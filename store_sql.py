from __future__ import annotations

import sqlite3
from pathlib import Path

from config import SQL_DB_PATH


def init_db() -> sqlite3.Connection:
    """
    Initialise SQLite database and ensure the weather table exists.
    """
    db_path = Path(SQL_DB_PATH)
    db_path.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS weather (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            location TEXT NOT NULL,
            forecast_date TEXT NOT NULL,
            temperature REAL NOT NULL,
            precipitation REAL NOT NULL,
            wind_speed REAL NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(location, forecast_date)
        )
        """
    )

    conn.commit()
    return conn


def store_weather(conn: sqlite3.Connection, rows: list[dict]) -> int:
    """
    Insert weather rows. Repeated runs update/replace duplicate location+date rows.
    Returns the number of rows written.
    """
    cursor = conn.cursor()

    sql = """
        INSERT OR REPLACE INTO weather (
            location, forecast_date, temperature, precipitation, wind_speed
        )
        VALUES (?, ?, ?, ?, ?)
    """

    written = 0
    for row in rows:
        cursor.execute(
            sql,
            (
                row["location"],
                row["forecast_date"],
                row["temperature"],
                row["precipitation"],
                row["wind_speed"],
            ),
        )
        written += 1

    conn.commit()
    return written


if __name__ == "__main__":
    sample = [
        {
            "location": "Aalborg",
            "forecast_date": "2026-03-22",
            "temperature": 8.4,
            "precipitation": 1.2,
            "wind_speed": 18.7,
        }
    ]

    conn = init_db()
    count = store_weather(conn, sample)
    print(f"Stored {count} weather row(s)")
    conn.close()
