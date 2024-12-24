import ccxt
from flask import Flask, request, jsonify

app = Flask(__name__)

# Set up Coinbase Advanced Trade connection
exchange = ccxt.coinbase({
    'apiKey': 'organizations/1073f4e6-52f3-49e4-b7e4-e2bd34261c51/apiKeys/ac613607-d810-41d4-9196-48c14ab0f8d0',
    'secret': '''-----BEGIN EC PRIVATE KEY-----
MHcCAQEEID8afQ5/asXPaRoupSmKxu71KzAAs5xjGsvQ3HoF2xdUoAoGCCqGSM49
AwEHoUQDQgAEUjZHnfp6pU4hFnf6SEm89Q8SiIF9aAldefKNdKrHbpzTIpe8uROG
1vcvhdnAFC7IA5otSktGGAje1XPWj2hcLg==
-----END EC PRIVATE KEY-----''',
})

# Route to place a trade
@app.route("/", methods=["POST"])
def trade_crypto():
    try:
        data = request.json  # Get JSON data
        symbol = data.get("symbol")  # e.g., 'DOGE/USD'
        side = data.get("side")  # 'buy' or 'sell'
        amount = float(data.get("amount"))  # Trade amount
        price = float(data.get("price"))  # Add price input

        # Place a market order with price calculation
        order = exchange.create_order(
            symbol=symbol,
            type="market",
            side=side,
            amount=amount,
            params={"cost": price * amount}  # Include required cost parameter
        )
        return {"status": "success", "order": order}, 200
    except Exception as e:
        return {"status": "error", "message": str(e)}, 400

# New route to fetch wallet balances
@app.route("/balances", methods=["GET"])
def get_balances():
    try:
        balance = exchange.fetch_balance()
        return {"status": "success", "balance": balance}, 200
    except Exception as e:
        return {"status": "error", "message": str(e)}, 400

if __name__ == "__main__":
    app.run(debug=True, port=8080)
