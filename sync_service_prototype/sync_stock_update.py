def update_stock_quantity(sku, quantity):
    print(f"Updating {sku} stock to {quantity}")
    return True


if __name__ == "__main__":
    sku = "MOUSE001"
    quantity = 100

    result = update_stock_quantity(
        sku,
        quantity
    )

    print("Stock update successful:", result)