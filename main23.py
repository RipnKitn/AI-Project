import time
import hmac
import hashlib
import base64
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

# Generate signature
def generate_signature(request_path, body, timestamp, method):
    message = f"{timestamp}{method}{request_path}{body or ''}"
    hmac_key = base64.b64decode(API_SECRET)
    signature = hmac.new(hmac_key, message.encode(), hashlib.sha256)
    return base64.b64encode(signature.digest()).decode()

# Fetch account balance for a currency
def fetch_balance(currency):
    try:
        endpoint = "/accounts"
        url = f"{BASE_URL}{endpoint}"
        timestamp = str(int(time.time()))
        headers = {
            "CB-ACCESS-KEY": API_KEY,
            "CB-ACCESS-SIGN": generate_signature(endpoint, "", timestamp, "GET"),
            "CB-ACCESS-TIMESTAMP": timestamp,
            "Content-Type": "application/json"
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        accounts = response.json().get("accounts", [])
        for account in accounts:
            if account["currency"] == currency:
                return float(account["available_balance"]["value"])
        return 0.0
    except Exception as e:
        return {"error": f"Balance fetch failed: {e}"}

# Place a buy/sell order
def place_trade(symbol, side):
    try:
        base_currency = symbol.split("-")[0]  # e.g., "GIGA" from "GIGA-USDC"
        balance = fetch_balance(base_currency)

        if balance <= 0:
            return {"error": "Insufficient balance"}

        # Trade 20% of the balance (adjust percentage as needed)
        percentage = 0.20  # Trade 20% of available balance
        trade_amount = balance * percentage  # Dynamic calculation

        # Execute the trade
        order = {
            "symbol": symbol,
            "side": side,
            "trade_amount": trade_amount
        }

        return order  # This simulates placing a successful trade (can be replaced with real API call)
    except Exception as e:
        return {"error": f"Trade failed: {str(e)}"}

# Webhook route for TradingView
@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.json
        symbol = data.get("symbol")  # e.g., "GIGA-USDC"
        side = data.get("side")      # "buy" or "sell"

        if not symbol or not side:
            return jsonify({"status": "error", "message": "Invalid parameters"}), 400

        result = place_trade(symbol, side)
        return jsonify({"status": "success", "result": result}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=8080)
