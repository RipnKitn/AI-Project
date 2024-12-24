import ccxt
from flask import Flask, request

app = Flask(__name__)

# Set up Coinbase Pro connection
exchange = ccxt.coinbasepro({
    'apiKey': 'organizations/1073f4e6-52f3-49e4-b7e4-e2bd34261c51/apiKeys/ac613607-d810-41d4-9196-48c14ab0f8d0',
    'secret': '''-----BEGIN EC PRIVATE KEY-----
MHcCAQEEID8afQ5/asXPaRoupSmKxu71KzAAs5xjGsvQ3HoF2xdUoAoGCCqGSM49
AwEHoUQDQgAEUjZHnfp6pU4hFnf6SEm89Q8SiIF9aAldefKNdKrHbpzTIpe8uROG
1vcvhdnAFC7IA5otSktGGAje1XPWj2hcLg==
-----END EC PRIVATE KEY-----''',
})

# Flask route to place a trade
@app.route("/", methods=["POST"])
def trade_crypto():
    try:
        data = request.json
        symbol = data.get("symbol")  # e.g., 'BTC/USD'
        side = data.get("side")      # 'buy' or 'sell'
        amount = float(data.get("amount"))
        
        # Place a market order
        order = exchange.create_order(
            symbol=symbol,
            type="market",
            side=side,
            amount=amount
        )
        return {"status": "success", "order": order}, 200
    except Exception as e:
        return {"status": "error", "message": str(e)}, 400

# Route to fetch supported trading pairs
@app.route("/pairs", methods=["GET"])
def get_supported_pairs():
    try:
        markets = exchange.load_markets()
        pairs = list(markets.keys())
        return {"status": "success", "pairs": pairs}, 200
    except Exception as e:
        return {"status": "error", "message": str(e)}, 400

# Route to fetch wallet balances
@app.route("/balances", methods=["GET"])
def get_balances():
    try:
        # Fetch balances from Coinbase Pro
        balances = exchange.fetch_balance()
        return {"status": "success", "balances": balances['total']}, 200
    except Exception as e:
        return {"status": "error", "message": str(e)}, 400

if __name__ == "__main__":
    app.run(debug=True, port=8080)
