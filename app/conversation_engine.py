from app.closer import CloserRequest, build_closer_response
from app.whatsapp_sender import send_whatsapp_text


async def process_customer_message(
    to: str,
    message: str,
    product_name: str = "",
    product_description: str = "",
    checkout_url: str = "",
) -> dict:
    result = build_closer_response(CloserRequest(
        customer_message=message,
        product_name=product_name,
        product_description=product_description,
        checkout_url=checkout_url,
    ))
    # Do not send automatically unless an explicit production integration calls this engine.
    return {
        "reply": result.reply,
        "intent": result.intent,
        "should_offer_checkout": result.should_offer_checkout,
        "should_handoff": result.should_handoff,
        "recipient": to,
    }
