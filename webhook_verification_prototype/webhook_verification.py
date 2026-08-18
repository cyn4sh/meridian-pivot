import hashlib
import hmac


secret = b"my-webhook-secret"

payload = b'{"sku":"MOUSE001","quantity":10}'


signature = hmac.new(
    secret,
    payload,
    hashlib.sha256
).hexdigest()


print("Payload:", payload.decode())
print("Signature:", signature)