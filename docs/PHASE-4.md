# Phase 4 — Payments & Conversion

Closvanta AI now has the foundation for Razorpay checkout and a payment/order pipeline.

## Environment

```env
RAZORPAY_KEY_ID=your_key_id
RAZORPAY_KEY_SECRET=your_key_secret
RAZORPAY_WEBHOOK_SECRET=your_webhook_secret
```

Never commit these values.

## Flow

1. Create an internal order record.
2. Create a Razorpay order using the amount in paise.
3. Render Razorpay Checkout on the client using the returned `key_id` and `order.id`.
4. Verify `razorpay_order_id|razorpay_payment_id` with the API secret.
5. Validate webhook signatures before changing payment state.
6. Mark the internal order paid only after verified payment/webhook events.

Automated outreach remains disabled by default.
