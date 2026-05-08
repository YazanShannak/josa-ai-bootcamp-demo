# Othman Demo

A simple expense tracker — base app for an AI bootcamp demo.

## Setup

```bash
# Install uv if you don't have it: https://docs.astral.sh/uv/
uv sync
cp .env.example .env   # fill in API keys (only needed for AI levels)
```

## Run

```bash
uv run uvicorn main:app --reload
```

Open http://localhost:8000

## Branch Progression

| Branch | AI Feature | pydantic-ai Concept |
|--------|-----------|---------------------|
| `main` | None — vanilla CRUD | — |
| `level-1-chatbot` | Chat assistant | Agent with tools, streaming |
| `level-2-receipt-agent` | Receipt/audio → expense | Multimodal input, structured output |
| `level-3-analysis` | Spending analysis report | Long-running agent, prose output |
| `level-4-forecasting` | 3-month forecast | Typed list structured output |

Switch between levels: `git checkout level-1-chatbot`
See what changed: `git diff main level-1-chatbot`
