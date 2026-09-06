from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.db import get_db
from app.db_models import LeadDB, ProductDB

router = APIRouter(prefix="/api/orders", tags=["orders"])

class OrderCreate(BaseModel):
    lead_id: int
    product_id: int
    amount: int = Field(gt=0)

@router.post("")
def create_order_record(payload: OrderCreate, db: Session = Depends(get_db)):
    lead = db.get(LeadDB, payload.lead_id)
    product = db.get(ProductDB, payload.product_id)
    if not lead or not product:
        raise HTTPException(status_code=404, detail="Lead or product not found")
    return {"status": "pending", "lead_id": lead.id, "product_id": product.id, "amount": payload.amount, "created_at": datetime.utcnow().isoformat()}
