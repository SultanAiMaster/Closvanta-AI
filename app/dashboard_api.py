from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.db import get_db
from app.db_models import LeadDB, MessageDB, ProductDB

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])

@router.get("/metrics")
def metrics(db: Session = Depends(get_db)):
    total = db.scalar(select(func.count(LeadDB.id))) or 0
    qualified = db.scalar(select(func.count(LeadDB.id)).where(LeadDB.status == "qualified")) or 0
    drafts = db.scalar(select(func.count(MessageDB.id))) or 0
    products = db.scalar(select(func.count(ProductDB.id))) or 0
    return {"leads": total, "qualified": qualified, "drafts": drafts, "products": products}

@router.get("/leads")
def leads(limit: int = 50, db: Session = Depends(get_db)):
    limit = max(1, min(limit, 200))
    return db.scalars(select(LeadDB).order_by(LeadDB.id.desc()).limit(limit)).all()
