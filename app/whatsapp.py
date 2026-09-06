from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel, Field

from app.config import settings

router = APIRouter(prefix="/whatsapp", tags=["whatsapp"])


class IncomingMessage(BaseModel):
    from_number: str = Field(min_length=3, max_length=40)
    text: str = Field(min_length=1, max_length=4000)
    lead_id: int | None = None


@router.get("/webhook")
def verify_webhook(hub_mode: str | None = None, hub_verify_token: str | None = None, hub_challenge: str | None = None):
    if hub_mode == "subscribe" and hub_verify_token == settings.whatsapp_verify_token and hub_challenge:
        return int(hub_challenge)
    raise HTTPException(status_code=403, detail="Webhook verification failed")


@router.post("/inbound")
def inbound(message: IncomingMessage):
    # Provider-specific delivery is intentionally separated from the AI conversation engine.
    return {"accepted": True, "lead_id": message.lead_id, "from_number": message.from_number}
