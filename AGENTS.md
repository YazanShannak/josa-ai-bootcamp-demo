# Othman Demo — Agent Instructions

A FastAPI + Vue 3 expense tracker used as a base app for an AI bootcamp demo.

## Stack

- **Backend**: FastAPI, SQLite (via SQLAlchemy), Python 3.12, managed with `uv`
- **Frontend**: Vue 3 SPA served as static files from `/static`
- **Entry point**: `main.py` → `uvicorn main:app --reload`

## Commands

```bash
uv sync                          # install dependencies
uv run uvicorn main:app --reload # start dev server (http://localhost:8000)
```

## Project Layout

```
main.py          # FastAPI app entry point
database.py      # SQLite setup
models.py        # SQLAlchemy models
routes/          # API route modules
static/          # Vue 3 SPA (built assets)
uploads/         # file upload storage
```

## Branch Progression

| Branch | Feature |
|--------|---------|
| `main` | Vanilla CRUD — no AI |
| `level-1-chatbot` | Chat assistant |
| `level-2-receipt-agent` | Receipt/audio → expense |
| `level-3-analysis` | Spending analysis report |
| `level-4-forecasting` | 3-month forecast |

## Notes

- `.env.example` documents required env vars; copy to `.env` before adding AI levels.
- No test suite exists yet — verify changes manually via the browser UI.
