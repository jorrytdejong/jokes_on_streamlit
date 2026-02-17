# Joke Studio

Single Streamlit app with built-in joke logic and persistence.

## Database modes
- Local default: SQLite at `data/jokes.db`
- Cloud option: Supabase Postgres using `DATABASE_URL` (or `SUPABASE_DB_URL`)

If no database URL is set, the app automatically uses local SQLite.

## Install
```bash
pip install -r requirements.txt
```

## OpenAI setup (required for joke generation)
Set:
- `OPENAI_API_KEY`
- optional `OPENAI_MODEL` (default: `gpt-4o-mini`)

You can put these in:
- `.streamlit/secrets.toml`
- environment variables

## Run locally
```bash
streamlit run Home.py
```

## Use Supabase (local or Streamlit Cloud)
Set one of these:
- `DATABASE_URL`
- `SUPABASE_DB_URL`

Example value:
```text
postgresql://postgres:[PASSWORD]@[HOST]:5432/postgres?sslmode=require
```

You can add this in:
- Streamlit Cloud secrets (`.streamlit/secrets.toml`)
- local environment variables

## App structure
- `Home.py`: overview and template guide
- `pages/1_Generate_Joke.py`: generate + save jokes
- `pages/2_Joke_Library.py`: search, browse, and export CSV
- `app/joke_engine.py`: OpenAI prompt + few-shot joke generation
- `app/database.py`: SQLAlchemy storage layer (SQLite/Supabase)
