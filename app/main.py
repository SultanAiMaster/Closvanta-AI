from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from app.campaigns import router as campaigns_router
from app.config import settings
from app.dashboard import router as dashboard_router
from app.db import get_db, init_db
from app.evaluator import LeadEvaluator
from app.models import EvaluateRequest, Product
from app.outreach import OutreachDraftGenerator
from app.scrapers.reddit import RedditScraper
from app.services import create_draft, create_product, save_evaluation, upsert_lead

app = FastAPI(title="Closvanta AI", version="0.3.0")
app.include_router(dashboard_router)
app.include_router(campaigns_router)


@app.on_event("startup")
def startup() -> None:
    init_db()


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "service": "closvanta-ai", "version": "0.3.0"}


@app.get("/leads/reddit")
async def reddit_leads(limit: int = 25, db: Session = Depends(get_db)):
    scraper = RedditScraper(settings.reddit_user_agent)
    leads = await scraper.fetch_many(settings.subreddits, limit=limit)
    for lead in leads:
        upsert_lead(db, lead)
    return leads


@app.post("/products")
def add_product(product: Product, db: Session = Depends(get_db)):
    return create_product(db, product)


@app.post("/leads/evaluate")
async def evaluate_lead(request: EvaluateRequest, db: Session = Depends(get_db)):
    if not settings.openai_api_key:
        raise HTTPException(status_code=503, detail="OPENAI_API_KEY is not configured")
    lead = upsert_lead(db, request.lead)
    evaluation = await LeadEvaluator().evaluate(request)
    save_evaluation(db, lead.id, evaluation)
    return evaluation


@app.post("/leads/{lead_id}/draft")
def draft_message(lead_id: int, request: EvaluateRequest, db: Session = Depends(get_db)):
    lead = upsert_lead(db, request.lead)
    if lead.id != lead_id:
        raise HTTPException(status_code=400, detail="lead_id does not match request.lead")
    body = OutreachDraftGenerator().build(request.lead, request.products)
    return create_draft(db, lead_id, body)
