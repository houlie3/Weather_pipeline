from __future__ import annotations

from fetch import fetch_weather
from generate_page import generate_page
from generate_poem import generate_poem
from store_sql import init_db, store_weather


def main() -> None:
    print("=" * 60)
    print("Automated Weather Pipeline")
    print("=" * 60)

    print("\n[1/4] Fetching weather forecasts...")
    weather_rows = fetch_weather()
    print(f"Fetched {len(weather_rows)} location forecast(s)")

    print("\n[2/4] Storing data in SQLite...")
    conn = init_db()
    written = store_weather(conn, weather_rows)
    conn.close()
    print(f"Stored {written} weather row(s)")

    print("\n[3/4] Generating bilingual poem with Groq...")
    poem = generate_poem(weather_rows)
    print("Poem generated")

    print("\n[4/4] Writing docs/index.html for GitHub Pages...")
    generate_page(weather_rows, poem)
    print("Dashboard written to docs/index.html")

    print("\nPipeline complete.")


if __name__ == "__main__":
    main()
