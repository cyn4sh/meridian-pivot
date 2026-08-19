attempts = 0


def update_stock_quantity(sku, quantity):
    global attempts

    attempts += 1

    print(f"Stock update attempt {attempts}")

    if attempts < 3:
        raise ConnectionError("Temporary warehouse sync failure")

    print(f"Updating {sku} stock to {quantity}")
    return True


if __name__ == "__main__":
    sku = "MOUSE001"
    quantity = 100

    update_stock_quantity(sku, quantity)