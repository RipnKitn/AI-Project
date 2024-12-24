import time
import hmac
import hashlib
import base64
import json
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

# Generate API signature
def generate_signature(request_path, body, timestamp, method):
    message = f"{timestamp}{method}{request_path}{body or ''}"
    hmac_key = base64.b64decode(API_SECRET)
    signature = hmac.new(hmac_key, message.encode(), hashlib.sha256)
    return base64.b64encode(signature.digest()).decode()

# Fetch balance for a specific coin
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

# Place a trade or check balance
def place_trade(symbol, side, percentage):
    try:
        if side == "check":  # Safely check balance
            base_currency = symbol.split("-")[0]
            balance = fetch_balance(base_currency)
            return {"balance": balance, "currency": base_currency}

        # Calculate trade amount
        base_currency = symbol.split("-")[0]
        balance = fetch_balance(base_currency)
        trade_amount = balance * (percentage / 100)

        if trade_amount <= 0:
            return {"error": "Insufficient balance"}

        # Simulated trade response
        return {
            "symbol": symbol,
            "side": side,
            "trade_amount": trade_amount,
            "status": "success"
        }
    except Exception as e:
        return {"error": f"Trade failed: {e}"}

# Webhook route
@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.json
        symbol = data.get("symbol")  # e.g., GIGA-USDC
        side = data.get("side")      # buy, sell, or check
        percentage = float(data.get("percentage", 0))

        if not symbol or not side:
            return jsonify({"status": "error", "message": "Invalid parameters"}), 400

        result = place_trade(symbol, side, percentage)
        return jsonify({"status": "success", "result": result}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=8080)
