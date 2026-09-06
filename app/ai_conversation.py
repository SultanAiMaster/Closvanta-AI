from app.ai_closer import generate_ai_reply


async def reply_with_ai(
    customer_message: str,
    history: list[dict[str, str]],
    product_name: str = "",
    product_description: str = "",
    checkout_url: str = "",
):
    return await generate_ai_reply(
        customer_message=customer_message,
        history=history,
        product_name=product_name,
        product_description=product_description,
        checkout_url=checkout_url,
    )
