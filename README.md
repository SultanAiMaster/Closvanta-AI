# Closvanta AI

AI-powered social selling and lead-closing engine.

## MVP

The first milestone focuses on compliant public-source lead ingestion and AI lead evaluation.

### Core modules

- Intent Radar: source adapters for public posts, starting with Reddit.
- Lead Evaluator: structured LLM scoring, pain-point extraction, and product matching.
- Outreach: value-first response drafts (human review by default).
- API: FastAPI endpoints for ingestion and evaluation.

## Safety and compliance

Closvanta AI does not attempt to bypass platform anti-abuse controls. Source adapters must respect official APIs, robots/rate limits, platform terms, and applicable privacy/marketing laws. Automated outreach is disabled by default.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/docs` for the API documentation.
