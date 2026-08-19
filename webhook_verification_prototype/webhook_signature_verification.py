import hashlib
import hmac


secret = b"my-webhook-secret"

payload = b'{"sku":"MOUSE001","quantity":10}'

received_signature = (
    "f8643d9849640df3411646b1748dc9999e85bf0553bd8e0bbd19f2be63c8927c"
)


def verify_signature(payload, secret, received_signature):
    expected_signature = hmac.new(
        secret,
        payload,
        hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(
        received_signature,
        expected_signature
    )


if __name__ == "__main__":
    is_valid = verify_signature(
        payload,
        secret,
        received_signature
    )

    print("Signature valid:", is_valid)