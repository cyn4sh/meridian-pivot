import hmac

from webhook_signature_verification import verify_signature


secret = b"my-webhook-secret"

# This is the signature generated from the original payload.
received_signature = (
    "f8643d9849640df3411646b1748dc9999e85bf0553bd8e0bbd19f2be63c8927c"
)

# The payload has been tampered with.
tampered_payload = b'{"sku":"MOUSE001","quantity":1000}'


is_valid = verify_signature(
    tampered_payload,
    secret,
    received_signature
)


print("Received signature:", received_signature)
print("Tampered payload:", tampered_payload.decode())
print("Signature valid:", is_valid)