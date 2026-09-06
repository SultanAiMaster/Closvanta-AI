import json
from datetime import datetime

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.closer import CloserRequest, build_closer_response
from app.db import get_db
from app.db_models import LeadDB, MessageDB

router = APIRouter(prefix="/conversations", tags=["conversations"])


class ConversationMessage(BaseModel):
    lead_id: int
    text: str = Field(min_length=1, max_length=4000)
    channel: str = "whatsapp"
    product_name: str = ""
    product_description: str = ""
    checkout_url: str = ""


@router.post("/reply")
def reply(payload: ConversationMessage, db: Session = Depends(get_db)):
    lead = db.get(LeadDB, payload.lead_id)
    if not lead:
        return {"error": "lead not found"}
    incoming = MessageDB(lead_id=lead.id, channel=payload.channel, body=payload.text, approved=True, sent=True)
    db.add(incoming)
    result = build_closer_response(CloserRequest(
        customer_message=payload.text,
        product_name=payload.product_name,
        product_description=payload.product_description,
        checkout_url=payload.checkout_url,
    ))
    outgoing = MessageDB(lead_id=lead.id, channel=payload.channel, body=result.reply, approved=False, sent=False)
    db.add(outgoing)
    db.commit()
    return {"reply": result, "message_id": outgoing.id}


@router.get("/{lead_id}")
def history(lead_id: int, db: Session = Depends(get_db)):
    return db.scalars(select(MessageDB).where(MessageDB.lead_id == lead_id).order_by(MessageDB.id)).all()
