from fastapi import FastAPI, HTTPException

from app.config import settings
from app.evaluator import LeadEvaluator
from app.models import EvaluateRequest
from app.scrapers.reddit import RedditScraper

app = FastAPI(title="Closvanta AI", version="0.1.0")


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "service": "closvanta-ai"}


@app.get("/leads/reddit")
async def reddit_leads(limit: int = 25):
    scraper = RedditScraper(settings.reddit_user_agent)
    return await scraper.fetch_many(settings.subreddits, limit=limit)


@app.post("/leads/evaluate")
async def evaluate_lead(request: EvaluateRequest):
    if not settings.openai_api_key:
        raise HTTPException(status_code=503, detail="OPENAI_API_KEY is not configured")
    return await LeadEvaluator().evaluate(request)
