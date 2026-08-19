import time


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


if __name__ == "__main__":
    sku = "MOUSE001"
    quantity = 100

    result = update_stock_with_retry(
        sku,
        quantity
    )

    print("Stock update successful:", result)