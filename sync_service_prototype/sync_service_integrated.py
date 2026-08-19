import time

from webhook_verification_prototype.webhook_signature_verification import verify_signature


attempts = 0


def update_stock_quantity(sku, quantity):
    global attempts

    attempts += 1

    print(f"Stock update attempt {attempts}")

    if attempts < 3:
        raise ConnectionError("Temporary warehouse sync failure")

    print(f"Updating {sku} stock to {quantity}")
    return True


def update_stock_with_retry(sku, quantity, max_retries=3):
    for attempt in range(1, max_retries + 1):
        try:
            return update_stock_quantity(sku, quantity)

        except ConnectionError as error:
            print(f"Attempt {attempt} failed: {error}")

            if attempt == max_retries:
                raise

            delay = 2 ** (attempt - 1)

            print(f"Waiting {delay} seconds before retrying...")
            time.sleep(delay)


def process_webhook(payload, secret, received_signature):
    is_valid = verify_signature(
        payload,
        secret,
        received_signature
    )

    if not is_valid:
        print("Webhook rejected")
        return False

    print("Webhook signature verified")

    sku = "MOUSE001"
    quantity = 100

    update_stock_with_retry(
        sku,
        quantity
    )

    print("Webhook processed successfully")
    return True


if __name__ == "__main__":
    secret = b"my-webhook-secret"

    payload = b'{"sku":"MOUSE001","quantity":10}'

    received_signature = (
        "f8643d9849640df3411646b1748dc9999e85bf0553bd8e0bbd19f2be63c8927c"
    )

    process_webhook(
        payload,
        secret,
        received_signature
    )