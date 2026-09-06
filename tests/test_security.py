import hashlib
import hmac
import os


def verify(secret: str, body: bytes, signature: str) -> bool:
    expected = hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature)


def test_webhook_signature_valid():
    secret = "test-secret"
    body = b'{"event":"payment.captured"}'
    signature = hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()
    assert verify(secret, body, signature)


def test_webhook_signature_invalid():
    assert not verify("test-secret", b"payload", "invalid")
