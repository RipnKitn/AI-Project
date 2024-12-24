import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# API Keys and Endpoint for Coinbase Advanced Trade
API_KEY = "organizations/1073f4e6-52f3-49e4-b7e4-e2bd34261c51/apiKeys/ac613607-d810-41d4-9196-48c14ab0f8d0"
API_SECRET = '''-----BEGIN EC PRIVATE KEY-----
MHcCAQEEID8afQ5/asXPaRoupSmKxu71KzAAs5xjGsvQ3HoF2xdUoAoGCCqGSM49
AwEHoUQDQgAEUjZHnfp6pU4hFnf6SEm89Q8SiIF9aAldefKNdKrHbpzTIpe8uROG
1vcvhdnAFC7IA5otSktGGAje1XPWj2hcLg==
-----END EC PRIVATE KEY-----'''
BASE_URL = "https://api.coinbase.com/api/v3/brokerage"

# Headers for authentication
HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}",
}

# Function to fetch balances
def fetch_balance(currency):
    response = requests.get(f"{BASE_URL}/accounts", headers=HEADERS)
    data = response.json()
    for account in data.get("accounts", []):
        if account["currency"] == currency:
            return float(account["available_balance"]["value"])
    return 0.0

# Route to place a trade with percentage-based size
@app.route("/trade", methods=["POST"])
def trade_crypto():
    try:
        data = request.json
        symbol = data.get("symbol")  # e.g., "BTC-USD"
        side = data.get("side")      # "buy" or "sell"
        percentage = float(data.get("percentage", 10)) / 100  # Default 10%

        # Determine the currency and fetch balance
        base_currency = symbol.split("-")[0]  # BTC in BTC-USD
        balance = fetch_balance(base_currency)
        trade_amount = balance * percentage

        if trade_amount <= 0:
            return jsonify({"status": "error", "message": "Insufficient balance for trade"}), 400

        # Placeholder for placing an order (replace with actual order logic)
        return jsonify({
            "status": "success",
            "symbol": symbol,
            "side": side,
            "trade_amount": trade_amount
        }), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True, port=8080)
