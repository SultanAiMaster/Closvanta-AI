from app.models import Lead, Product


class OutreachDraftGenerator:
    """Creates value-first drafts. Sending is intentionally outside this service."""

    def build(self, lead: Lead, products: list[Product]) -> str:
        product = products[0] if products else None
        opener = f"Aapke post mein ye point notice kiya: {lead.title or lead.body[:160]}"
        if product:
            return f"{opener}\n\nAgar useful ho, {product.name} aapke mentioned problem ko address kar sakta hai. {product.description[:240]}\n\nAgar aap chaho to main details/shareable demo bhej sakta hoon."
        return f"{opener}\n\nAgar aap abhi bhi solution dekh rahe hain, main relevant options compare karne mein help kar sakta hoon."
