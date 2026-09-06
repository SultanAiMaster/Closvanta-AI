from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.db import get_db
from app.db_models import LeadDB, MessageDB, ProductDB

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/summary")
def summary(db: Session = Depends(get_db)):
    total_leads = db.scalar(select(func.count(LeadDB.id))) or 0
    qualified = db.scalar(select(func.count(LeadDB.id)).where(LeadDB.status == "qualified")) or 0
    spam = db.scalar(select(func.count(LeadDB.id)).where(LeadDB.status == "spam")) or 0
    drafts = db.scalar(select(func.count(MessageDB.id))) or 0
    products = db.scalar(select(func.count(ProductDB.id))) or 0
    return {
        "total_leads": total_leads,
        "qualified_leads": qualified,
        "spam_leads": spam,
        "outreach_drafts": drafts,
        "products": products,
    }


@router.get("/leads")
def recent_leads(limit: int = 50, db: Session = Depends(get_db)):
    limit = max(1, min(limit, 200))
    return db.scalars(select(LeadDB).order_by(LeadDB.id.desc()).limit(limit)).all()
