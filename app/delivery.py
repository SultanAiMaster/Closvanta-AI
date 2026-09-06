from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import get_db
from app.db_models import ProductDB
from app.order_models import OrderDB

router = APIRouter(prefix="/delivery", tags=["delivery"])

class DeliveryRequest(BaseModel):
    order_id: int
    customer_email: str = Field(min_length=3, max_length=320)

@router.post("/prepare")
def prepare_delivery(payload: DeliveryRequest, db: Session = Depends(get_db)):
    order = db.get(OrderDB, payload.order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if order.status != "paid":
        raise HTTPException(status_code=409, detail="Order is not paid")
    product = db.get(ProductDB, order.product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return {
        "status": "ready",
        "order_id": order.id,
        "customer_email": payload.customer_email,
        "product": product.name,
        "delivery_url": product.checkout_url,
        "prepared_at": datetime.utcnow().isoformat(),
    }
