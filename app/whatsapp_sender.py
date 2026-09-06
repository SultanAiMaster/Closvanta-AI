import httpx

from app.config import settings


async def send_whatsapp_text(to: str, body: str) -> dict:
    """Send a WhatsApp Cloud API text message to an opted-in recipient."""
    if not settings.whatsapp_access_token or not settings.whatsapp_phone_number_id:
        raise RuntimeError("WhatsApp credentials are not configured")
    url = f"https://graph.facebook.com/v23.0/{settings.whatsapp_phone_number_id}/messages"
    headers = {"Authorization": f"Bearer {settings.whatsapp_access_token}"}
    payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": to,
        "type": "text",
        "text": {"preview_url": True, "body": body},
    }
    async with httpx.AsyncClient(timeout=20) as client:
        response = await client.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
