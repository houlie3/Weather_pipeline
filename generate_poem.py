from __future__ import annotations

import os
from typing import Any

from dotenv import load_dotenv
from groq import Groq

from config import POEM_TXT_PATH, SECOND_LANGUAGE

load_dotenv()


def _build_prompt(weather_rows: list[dict[str, Any]]) -> str:
    bullet_lines = []
    for row in weather_rows:
        bullet_lines.append(
            f"- {row['location']}: {row['temperature']}°C max, "
            f"{row['precipitation']} mm precipitation, "
            f"{row['wind_speed']} km/h max wind, "
            f"date {row['forecast_date']}"
        )

    joined = "\n".join(bullet_lines)
    return (
        "Write a short weather poem in exactly two sections.\n"
        "Section 1 must be in English.\n"
        f"Section 2 must be in {SECOND_LANGUAGE}.\n"
        "Compare the weather in the three listed locations for tomorrow.\n"
        "Mention the differences in temperature, precipitation, and wind.\n"
        "End by clearly saying where it would be nicest to be tomorrow.\n"
        "Keep the whole poem under 16 lines total.\n\n"
        "Weather data:\n"
        f"{joined}"
    )


def generate_poem(weather_rows: list[dict[str, Any]]) -> str:
    """
    Generate a bilingual poem with Groq and save a copy to data/poem.txt.
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError(
            "Missing GROQ_API_KEY. Add it to your local .env or GitHub Secrets."
        )

    client = Groq(api_key=api_key)
    prompt = _build_prompt(weather_rows)

    response = client.chat.completions.create(
        model=os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"),
        messages=[
            {
                "role": "system",
                "content": "You write vivid but concise poems from structured data.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.8,
    )

    poem = response.choices[0].message.content.strip()
    POEM_TXT_PATH.write_text(poem, encoding="utf-8")
    return poem
