# WhatsApp Cloud API setup

Set these environment variables:

```env
WHATSAPP_VERIFY_TOKEN=choose_a_random_verification_token
WHATSAPP_ACCESS_TOKEN=your_meta_access_token
WHATSAPP_PHONE_NUMBER_ID=your_phone_number_id
```

Configure the Meta WhatsApp webhook to point to the deployed `/whatsapp/webhook` endpoint. The verification token must match `WHATSAPP_VERIFY_TOKEN`.

Inbound messages should be normalized into the conversation API. Outbound sending should remain disabled until the Meta business account, permissions, recipient opt-in requirements, templates where required, and production webhook verification are configured.

Never commit access tokens or webhook secrets to Git.
