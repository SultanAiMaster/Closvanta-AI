# Phase 5.2 — WhatsApp outbound integration

Closvanta now contains a dedicated WhatsApp Cloud API sender and a conversation-engine integration layer.

## Environment

```env
WHATSAPP_ACCESS_TOKEN=...
WHATSAPP_PHONE_NUMBER_ID=...
WHATSAPP_VERIFY_TOKEN=...
```

The sender uses the Meta Graph API and sends plain text only. Recipients must be contacted according to WhatsApp Business policies and applicable consent/marketing requirements.

The conversation engine intentionally returns a proposed response without automatically sending it. A production webhook/controller can call `send_whatsapp_text()` after the appropriate consent, policy, and business-logic checks.
