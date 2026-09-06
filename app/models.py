from pydantic import BaseModel, Field, HttpUrl


class Lead(BaseModel):
    source: str
    external_id: str
    url: HttpUrl | None = None
    author: str | None = None
    title: str = ""
    body: str = ""
    created_at: str | None = None


class Product(BaseModel):
    name: str
    description: str
    checkout_url: HttpUrl | None = None


class LeadEvaluation(BaseModel):
    intent_score: int = Field(ge=1, le=10)
    is_spam: bool
    pain_points: list[str] = Field(default_factory=list)
    matched_products: list[str] = Field(default_factory=list)
    reasoning: str
    recommended_action: str


class EvaluateRequest(BaseModel):
    lead: Lead
    products: list[Product] = Field(default_factory=list)
