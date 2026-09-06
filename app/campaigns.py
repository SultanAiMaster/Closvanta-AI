from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field

from app.db import get_db
from app.db_models import CampaignDB

router = APIRouter(prefix="/campaigns", tags=["campaigns"])


class CampaignCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    description: str = ""
    active: bool = False


@router.post("")
def create_campaign(payload: CampaignCreate, db: Session = Depends(get_db)):
    campaign = CampaignDB(**payload.model_dump())
    db.add(campaign)
    db.commit()
    db.refresh(campaign)
    return campaign


@router.get("")
def list_campaigns(db: Session = Depends(get_db)):
    return db.scalars(select(CampaignDB).order_by(CampaignDB.id.desc())).all()
