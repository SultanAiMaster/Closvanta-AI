# Closvanta AI

AI-powered social selling and lead-closing engine.

## Current capabilities

- Public-source lead ingestion and AI evaluation foundation
- Product and campaign APIs
- Dashboard metrics and lead pipeline
- Razorpay order/payment foundation
- WhatsApp Cloud API webhook and outbound sender
- Conversation history and AI closer layer
- Paid-order delivery preparation
- API authentication and rate-limit foundations
- Docker deployment
- GitHub Actions CI and automated tests

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/docs` for API documentation.

## Production

Use PostgreSQL, HTTPS, a reverse proxy/API gateway, external rate limiting, backups, monitoring, and verified third-party webhook signatures. Keep all credentials in environment variables and never commit `.env`.

WhatsApp outbound messaging must respect recipient consent and applicable platform rules. Payment state must only change after verified Razorpay events. Automated outreach remains disabled by default.
