from sync_service_prototype.sync_service_integrated import process_webhook


if __name__ == "__main__":
    secret = b"my-webhook-secret"

    tampered_payload = b'{"sku":"MOUSE001","quantity":1000}'

    original_signature = (
        "f8643d9849640df3411646b1748dc9999e85bf0553bd8e0bbd19f2be63c8927c"
    )

    process_webhook(
        tampered_payload,
        secret,
        original_signature
    )