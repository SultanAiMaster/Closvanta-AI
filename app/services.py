import json

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db_models import LeadDB, LeadEvaluationDB, MessageDB, ProductDB
from app.models import Lead, LeadEvaluation, Product


def upsert_lead(db: Session, lead: Lead) -> LeadDB:
    item = db.scalar(select(LeadDB).where(LeadDB.external_id == lead.external_id))
    if item is None:
        item = LeadDB(
            source=lead.source, external_id=lead.external_id, url=str(lead.url) if lead.url else None,
            author=lead.author, title=lead.title, body=lead.body,
        )
        db.add(item)
    else:
        item.title, item.body, item.url, item.author = lead.title, lead.body, str(lead.url) if lead.url else None, lead.author
    db.commit()
    db.refresh(item)
    return item


def create_product(db: Session, product: Product) -> ProductDB:
    item = ProductDB(name=product.name, description=product.description, checkout_url=str(product.checkout_url) if product.checkout_url else None)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def save_evaluation(db: Session, lead_id: int, evaluation: LeadEvaluation) -> LeadEvaluationDB:
    item = LeadEvaluationDB(
        lead_id=lead_id, intent_score=evaluation.intent_score, is_spam=evaluation.is_spam,
        pain_points_json=json.dumps(evaluation.pain_points), matched_products_json=json.dumps(evaluation.matched_products),
        reasoning=evaluation.reasoning, recommended_action=evaluation.recommended_action,
    )
    db.add(item)
    lead = db.get(LeadDB, lead_id)
    if lead:
        lead.intent_score = evaluation.intent_score
        lead.is_spam = evaluation.is_spam
        lead.reasoning = evaluation.reasoning
        lead.status = "spam" if evaluation.is_spam else ("qualified" if evaluation.intent_score >= 7 else "review")
    db.commit()
    db.refresh(item)
    return item


def create_draft(db: Session, lead_id: int, body: str, channel: str = "draft") -> MessageDB:
    item = MessageDB(lead_id=lead_id, body=body, channel=channel, approved=False, sent=False)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
