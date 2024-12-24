try:
    data = request.json  # Get JSON data
    symbol = data.get("symbol")  # e.g., 'BTC/USD'
    side = data.get("side")  # 'buy' or 'sell'
    amount = float(data.get("amount"))  # Trade amount
    price = float(data.get("price"))  # Add price input

    # Place a market order
    order = exchange.create_order(
        symbol=symbol,
        type="market",
        side=side,
        amount=amount,
        params={"cost": price * amount}  # Include price calculation
    )
    return {"status": "success", "order": order}, 200
