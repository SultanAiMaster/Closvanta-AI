# Security baseline

- Keep `OPENAI_API_KEY`, Razorpay secrets, WhatsApp access tokens and `INTERNAL_API_KEY` outside Git.
- Use HTTPS in production.
- Protect internal/admin endpoints with API authentication before exposing them publicly.
- Apply rate limiting at the reverse proxy/API gateway in multi-instance deployments; the included limiter is an in-process baseline only.
- Validate third-party webhook signatures before changing order/payment state.
- Make payment and delivery transitions idempotent.
- Rotate credentials immediately if they are exposed.
