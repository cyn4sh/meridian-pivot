from webhook_verification_prototype.webhook_signature_verification import verify_signature


def process_webhook(payload, secret, received_signature):
    is_valid = verify_signature(
        payload,
        secret,
        received_signature
    )

    if not is_valid:
        return "Webhook rejected"

    return "Webhook processed"


if __name__ == "__main__":
    secret = b"my-webhook-secret"

    payload = b'{"sku":"MOUSE001","quantity":10}'

    received_signature = (
        "f8643d9849640df3411646b1748dc9999e85bf0553bd8e0bbd19f2be63c8927c"
    )

    result = process_webhook(
        payload,
        secret,
        received_signature
    )

    print(result)