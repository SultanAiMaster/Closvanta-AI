import hashlib
import hmac
from typing import Any

from fastapi import APIRouter, Depends, Header, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.config import settings
from app.db import get_db

router = APIRouter(prefix="/payments", tags=["payments"])


class RazorpayOrderRequest(BaseModel):
    amount: int = Field(gt=0, description="Amount in smallest currency unit (e.g. paise)")
    currency: str = Field(default="INR", min_length=3, max_length=3)
    receipt: str | None = Field(default=None, max_length=40)
    notes: dict[str, str] = Field(default_factory=dict)


def verify_razorpay_signature(order_id: str, payment_id: str, signature: str) -> bool:
    secret = settings.razorpay_key_secret
    if not secret:
        return False
    message = f"{order_id}|{payment_id}".encode()
    expected = hmac.new(secret.encode(), message, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature)


@router.post("/orders")
def create_order(payload: RazorpayOrderRequest) -> dict[str, Any]:
    if not settings.razorpay_key_id or not settings.razorpay_key_secret:
        raise HTTPException(status_code=503, detail="Razorpay credentials are not configured")
    try:
        import razorpay
    except ImportError as exc:
        raise HTTPException(status_code=503, detail="razorpay package is not installed") from exc

    client = razorpay.Client(auth=(settings.razorpay_key_id, settings.razorpay_key_secret))
    order = client.order.create({
        "amount": payload.amount,
        "currency": payload.currency.upper(),
        "receipt": payload.receipt,
        "notes": payload.notes,
    })
    return {"order": order, "key_id": settings.razorpay_key_id}


@router.post("/verify")
def verify_payment(order_id: str, payment_id: str, signature: str):
    if not verify_razorpay_signature(order_id, payment_id, signature):
        raise HTTPException(status_code=400, detail="Invalid Razorpay payment signature")
    return {"verified": True, "order_id": order_id, "payment_id": payment_id}


@router.post("/webhook")
def razorpay_webhook(payload: dict[str, Any], x_razorpay_signature: str | None = Header(default=None)):
    # Production webhook processing must validate the webhook secret before mutating state.
    if not settings.razorpay_webhook_secret:
        raise HTTPException(status_code=503, detail="Razorpay webhook secret is not configured")
    if not x_razorpay_signature:
        raise HTTPException(status_code=400, detail="Missing Razorpay webhook signature")
    import json
    raw = json.dumps(payload, separators=(",", ":"), ensure_ascii=False).encode()
    expected = hmac.new(settings.razorpay_webhook_secret.encode(), raw, hashlib.sha256).hexdigest()
    if not hmac.compare_digest(expected, x_razorpay_signature):
        raise HTTPException(status_code=400, detail="Invalid Razorpay webhook signature")
    return {"received": True, "event": payload.get("event")}
