from pydantic import BaseModel, Field

from app.ai_closer import generate_ai_reply
from app.whatsapp_sender import send_whatsapp_text


class CheckoutFlowRequest(BaseModel):
    recipient: str = Field(min_length=3, max_length=40)
    message: str = Field(min_length=1, max_length=4000)
    product_name: str = ""
    product_description: str = ""
    checkout_url: str = ""
    history: list[dict[str, str]] = Field(default_factory=list)
    send: bool = False


async def run_checkout_flow(request: CheckoutFlowRequest) -> dict:
    result = await generate_ai_reply(
        customer_message=request.message,
        history=request.history,
        product_name=request.product_name,
        product_description=request.product_description,
        checkout_url=request.checkout_url,
    )
    sent = False
    provider_response = None
    if request.send:
        if result.should_handoff:
            return {"result": result, "sent": False, "reason": "human_handoff"}
        provider_response = await send_whatsapp_text(request.recipient, result.reply)
        sent = True
    return {"result": result, "sent": sent, "provider_response": provider_response}
