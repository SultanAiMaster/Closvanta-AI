from datetime import datetime

from sqlalchemy.orm import Session

from app.db_models import LeadDB, ProductDB
from app.order_models import OrderDB


def create_internal_order(db: Session, lead_id: int, product_id: int, amount: int, currency: str = "INR") -> OrderDB:
    if not db.get(LeadDB, lead_id):
        raise ValueError("lead not found")
    if not db.get(ProductDB, product_id):
        raise ValueError("product not found")
    order = OrderDB(lead_id=lead_id, product_id=product_id, amount=amount, currency=currency.upper(), status="pending")
    db.add(order)
    db.commit()
    db.refresh(order)
    return order


def mark_paid(db: Session, order: OrderDB, payment_id: str) -> OrderDB:
    order.razorpay_payment_id = payment_id
    order.status = "paid"
    order.paid_at = datetime.utcnow()
    db.commit()
    db.refresh(order)
    return order
