from app.closer import CloserRequest, build_closer_response


def test_purchase_intent_offers_checkout():
    result = build_closer_response(CloserRequest(customer_message="What is the price?", checkout_url="https://checkout.example/1"))
    assert result.intent == "purchase_intent"
    assert result.should_offer_checkout is True


def test_human_request_handoffs():
    result = build_closer_response(CloserRequest(customer_message="I want to talk to a human"))
    assert result.should_handoff is True


def test_information_does_not_push_checkout():
    result = build_closer_response(CloserRequest(customer_message="Tell me what this does", checkout_url="https://checkout.example/1"))
    assert result.should_offer_checkout is False
