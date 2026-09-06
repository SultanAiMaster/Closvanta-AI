from pydantic import BaseModel, Field


class CloserRequest(BaseModel):
    customer_message: str = Field(min_length=1, max_length=4000)
    product_name: str = ""
    product_description: str = ""
    checkout_url: str = ""


class CloserResponse(BaseModel):
    reply: str
    intent: str
    should_offer_checkout: bool
    should_handoff: bool


def build_closer_response(request: CloserRequest) -> CloserResponse:
    text = request.customer_message.lower()
    wants_to_buy = any(x in text for x in ("buy", "purchase", "price", "payment", "checkout", "cost"))
    wants_human = any(x in text for x in ("human", "agent", "support", "call me", "talk to someone"))
    if wants_human:
        return CloserResponse(reply="Bilkul. Main aapko human support ke paas handoff kar raha hoon.", intent="human_handoff", should_offer_checkout=False, should_handoff=True)
    if wants_to_buy and request.checkout_url:
        return CloserResponse(reply=f"Bilkul. Aap yahan secure checkout complete kar sakte hain: {request.checkout_url}", intent="purchase_intent", should_offer_checkout=True, should_handoff=False)
    return CloserResponse(reply="Samajh gaya. Agar aap chahein to main product, pricing aur next steps clear kar deta hoon.", intent="information", should_offer_checkout=False, should_handoff=False)
