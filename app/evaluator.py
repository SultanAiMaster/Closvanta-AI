import json

from openai import AsyncOpenAI

from app.config import settings
from app.models import EvaluateRequest, LeadEvaluation


SYSTEM_PROMPT = """You are Closvanta AI's lead-intent evaluator.
Evaluate a public social post for genuine purchase intent.
Score 1-10. Detect spam. Extract concrete pain points. Match only products that plausibly solve the stated problem.
Do not infer sensitive personal traits. Do not recommend deceptive, coercive, or unsolicited bulk outreach.
Return only valid JSON matching the requested schema."""


class LeadEvaluator:
    def __init__(self, client: AsyncOpenAI | None = None):
        self.client = client or AsyncOpenAI(api_key=settings.openai_api_key)

    async def evaluate(self, request: EvaluateRequest) -> LeadEvaluation:
        products = [p.model_dump(mode="json") for p in request.products]
        lead = request.lead.model_dump(mode="json")
        schema = {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "intent_score": {"type": "integer", "minimum": 1, "maximum": 10},
                "is_spam": {"type": "boolean"},
                "pain_points": {"type": "array", "items": {"type": "string"}},
                "matched_products": {"type": "array", "items": {"type": "string"}},
                "reasoning": {"type": "string"},
                "recommended_action": {"type": "string"},
            },
            "required": ["intent_score", "is_spam", "pain_points", "matched_products", "reasoning", "recommended_action"],
        }
        response = await self.client.responses.create(
            model=settings.openai_model,
            input=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": json.dumps({"lead": lead, "products": products})},
            ],
            text={"format": {"type": "json_schema", "name": "lead_evaluation", "strict": True, "schema": schema}},
        )
        return LeadEvaluation.model_validate_json(response.output_text)
