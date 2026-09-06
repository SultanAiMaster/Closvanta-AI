# Closvanta AI — Deployment

## 1. Build and run

```bash
docker compose up --build -d
```

The API listens on port `8000`.

## 2. Environment

Create `.env` from `.env.example` and set production values for OpenAI, Razorpay, WhatsApp, and the database. Never commit `.env`.

## 3. Health check

```bash
curl https://YOUR_DOMAIN/health
```

Expected response contains `"status":"ok"`.

## 4. Razorpay webhook

Configure Razorpay to send payment events to:

```text
https://YOUR_DOMAIN/payments/webhook
```

Set the same webhook secret in `RAZORPAY_WEBHOOK_SECRET`.

## 5. WhatsApp webhook

Configure the Meta WhatsApp Cloud API callback URL:

```text
https://YOUR_DOMAIN/whatsapp/webhook
```

Use the exact `WHATSAPP_VERIFY_TOKEN` configured in the application.

## Production checklist

- Put the app behind HTTPS/reverse proxy.
- Use PostgreSQL instead of SQLite for multi-instance production.
- Restrict inbound webhook endpoints at the infrastructure layer where possible.
- Rotate credentials if exposed.
- Configure backups and monitoring.
- Keep outbound WhatsApp messaging consent-aware and human-reviewable until the business flow is validated.
