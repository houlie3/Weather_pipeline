# Automated Weather Pipeline with GitHub Pages

This project fetches tomorrow's weather for three locations from Open-Meteo,
stores the forecast in SQLite, generates a bilingual poem with Groq, and
publishes the result as a GitHub Pages site.

## Files

- `fetch.py` - fetches weather from Open-Meteo
- `store_sql.py` - stores weather in SQLite
- `generate_poem.py` - generates the bilingual poem with Groq
- `generate_page.py` - writes `docs/index.html`
- `main.py` - runs the full pipeline
- `.github/workflows/weather_pipeline.yml` - scheduled automation

## Setup

1. Create a public GitHub repository.
2. Copy these files into it.
3. Create a `.env` file locally with:

```env
GROQ_API_KEY=your_key_here
```

4. Replace the coordinates in `config.py` with your real locations.
5. Install dependencies:

```bash
pip install -r requirements.txt
```

6. Run locally:

```bash
python main.py
```

## GitHub Actions

Add `GROQ_API_KEY` as a repository secret:

- Settings -> Secrets and variables -> Actions -> New repository secret

The workflow also supports manual runs through `workflow_dispatch`.

## GitHub Pages

In the repository settings:

- Pages -> Build and deployment -> Source -> Deploy from a branch
- Branch -> `main`
- Folder -> `/docs`

After the workflow runs, the generated site is published from `docs/index.html`.
