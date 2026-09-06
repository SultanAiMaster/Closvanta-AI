from openai import AsyncOpenAI

from app.closer import CloserResponse
from app.config import settings

SYSTEM_PROMPT = """You are Closvanta AI, a concise sales assistant. Be helpful, truthful and non-pushy. Use only the supplied product facts. Never invent pricing, features, guarantees, refunds, availability or policies. If the customer asks for a human, recommend handoff. If they show clear purchase intent and a valid checkout URL is supplied, you may present it. Do not pressure or repeatedly message the customer."""


async def generate_ai_reply(
    customer_message: str,
    history: list[dict[str, str]],
    product_name: str = "",
    product_description: str = "",
    checkout_url: str = "",
) -> CloserResponse:
    if not settings.openai_api_key:
        raise RuntimeError("OPENAI_API_KEY is not configured")

    client = AsyncOpenAI(api_key=settings.openai_api_key)
    context = f"Product: {product_name}\nDescription: {product_description}\nCheckout URL: {checkout_url}"
    messages = [{"role": "system", "content": SYSTEM_PROMPT}, {"role": "system", "content": context}]
    messages.extend(history[-12:])
    messages.append({"role": "user", "content": customer_message})

    response = await client.chat.completions.create(
        model=settings.openai_model,
        messages=messages,
        temperature=0.4,
        response_format={"type": "json_object"},
    )
    import json
    data = json.loads(response.choices[0].message.content or "{}")
    return CloserResponse(
        reply=str(data.get("reply", "Main aapki help kar sakta hoon.")),
        intent=str(data.get("intent", "information")),
        should_offer_checkout=bool(data.get("should_offer_checkout", False)) and bool(checkout_url),
        should_handoff=bool(data.get("should_handoff", False)),
    )
