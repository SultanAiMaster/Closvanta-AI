# Paid Order Delivery

The delivery endpoint only prepares delivery for orders whose internal status is `paid`.

Production flow:

1. Razorpay webhook is authenticated.
2. Payment/order is matched to an internal order.
3. Internal order becomes `paid` idempotently.
4. Delivery job is created exactly once.
5. Product entitlement/download URL is issued.
6. Customer receives delivery through the configured channel.

Do not use a public checkout URL as a private digital-product download URL. Store protected entitlement/download information separately before production launch.
