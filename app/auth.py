import hashlib
import hmac

from fastapi import Header, HTTPException

from app.config import settings


def require_api_key(x_api_key: str | None = Header(default=None)) -> None:
    configured = settings.internal_api_key
    if not configured:
        raise HTTPException(status_code=503, detail="INTERNAL_API_KEY is not configured")
    if not x_api_key or not hmac.compare_digest(x_api_key, configured):
        raise HTTPException(status_code=401, detail="Invalid API key")
