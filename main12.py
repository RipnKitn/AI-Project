import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Coinbase Advanced Trade API settings
API_KEY = "organizations/1073f4e6-52f3-49e4-b7e4-e2bd34261c51/apiKeys/ac613607-d810-41d4-9196-48c14ab0f8d0"
API_SECRET = '''-----BEGIN EC PRIVATE KEY-----
MHcCAQEEID8afQ5/asXPaRoupSmKxu71KzAAs5xjGsvQ3HoF2xdUoAoGCCqGSM49
AwEHoUQDQgAEUjZHnfp6pU4hFnf6SEm89Q8SiIF9aAldefKNdKrHbpzTIpe8uROG
1vcvhdnAFC7IA5otSktGGAje1XPWj2hcLg==
-----END EC PRIVATE KEY-----'''
BASE_URL = "https://api.coinbase.com/api/v3/brokerage"

HEADERS = {"Content-Type": "application/json", "Authorization": f"Bearer {API_KEY}"}

# Fetch account balance
def fetch_balance(currency):
    response = requests.get(f"{BASE_URL}/accounts", headers=HEADERS)
    data = response.json()
    for account in data.get("accounts", []):
        if account["currency"] == currency:
            return float(account["available_balance"]["value"])
    return 0.0

# Place a market order
def place_trade(symbol, side, percentage):
    base_currency = symbol.split("-")[0]  # e.g., ETH in ETH-USD
    balance = fetch_balance(base_currency)
    trade_amount = balance * (percentage / 100)

    if trade_amount <= 0:
        return {"error": "Insufficient balance"}

    # Simulate order (no real trade execution here)
    return {"symbol": symbol, "side": side, "trade_amount": trade_amount}

# Flask route for TradingView webhook
@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.json
        symbol = data.get("symbol")  # e.g., ETH-USD
        side = data.get("side")      # "buy" or "sell"
        percentage = float(data.get("percentage", 1))  # Default 1%

        result = place_trade(symbol, side, percentage)
        return jsonify({"status": "success", "result": result}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True, port=8080)
