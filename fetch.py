from __future__ import annotations

from datetime import date, timedelta
from typing import Any

import requests

from config import LOCATIONS

BASE_URL = "https://api.open-meteo.com/v1/forecast"


def fetch_weather() -> list[dict[str, Any]]:
    """
    Fetch tomorrow's forecast for all configured locations from Open-Meteo.
    Returns a list of dictionaries ready for SQLite insertion and page rendering.
    """
    tomorrow = date.today() + timedelta(days=1)
    all_rows: list[dict[str, Any]] = []

    for location_name, (latitude, longitude) in LOCATIONS.items():
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "daily": "temperature_2m_max,precipitation_sum,wind_speed_10m_max",
            "forecast_days": 2,
            "timezone": "auto",
        }

        response = requests.get(BASE_URL, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()

        daily = data.get("daily", {})
        dates = daily.get("time", [])
        temperatures = daily.get("temperature_2m_max", [])
        precipitations = daily.get("precipitation_sum", [])
        wind_speeds = daily.get("wind_speed_10m_max", [])

        target_date = tomorrow.isoformat()
        if target_date in dates:
            idx = dates.index(target_date)
        elif len(dates) >= 2:
            idx = 1
            target_date = dates[idx]
        elif dates:
            idx = 0
            target_date = dates[idx]
        else:
            raise RuntimeError(f"No daily forecast data returned for {location_name}.")

        all_rows.append(
            {
                "location": location_name,
                "forecast_date": target_date,
                "temperature": float(temperatures[idx]),
                "precipitation": float(precipitations[idx]),
                "wind_speed": float(wind_speeds[idx]),
            }
        )

    return all_rows


if __name__ == "__main__":
    rows = fetch_weather()
    print(f"Fetched {len(rows)} weather row(s)")
    for row in rows:
        print(row)
