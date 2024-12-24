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

# Signature generation for Coinbase API
def generate_signature(timestamp, method, request_path, body):
    message = f"{timestamp}{method}{request_path}{body or ''}"
    secret = base64.b64decode(API_SECRET)
    signature = hmac.new(secret, message.encode(), hashlib.sha256).digest()
    return base64.b64encode(signature).decode()

# Fetch balance
def fetch_balance(currency):
    try:
        timestamp = str(int(time.time()))
        endpoint = "/accounts"
        headers = {
            "CB-ACCESS-KEY": API_KEY,
            "CB-ACCESS-SIGN": generate_signature(timestamp, "GET", endpoint, ""),
            "CB-ACCESS-TIMESTAMP": timestamp,
            "Content-Type": "application/json"
        }
        response = requests.get(BASE_URL + endpoint, headers=headers)
        response.raise_for_status()
        accounts = response.json().get("accounts", [])
        for account in accounts:
            if account["currency"] == currency:
                return float(account["available_balance"]["value"])
        return 0.0
    except Exception as e:
        return {"error": f"Balance fetch failed: {e}"}

# Place a trade
def place_trade(symbol, side, percentage):
    try:
        base_currency = symbol.split("-")[0]
        balance = fetch_balance(base_currency)
        trade_amount = balance * (percentage / 100)
        if trade_amount <= 0:
            return {"error": "Insufficient balance"}

        timestamp = str(int(time.time()))
        endpoint = "/orders"
        body = json.dumps({
            "product_id": symbol,
            "side": side.lower(),
            "order_configuration": {
                "market_market_ioc": {
                    "quote_size": str(trade_amount)
                }
            }
        })
        headers = {
            "CB-ACCESS-KEY": API_KEY,
            "CB-ACCESS-SIGN": generate_signature(timestamp, "POST", endpoint, body),
            "CB-ACCESS-TIMESTAMP": timestamp,
            "Content-Type": "application/json"
        }
        response = requests.post(BASE_URL + endpoint, headers=headers, data=body)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": f"Trade failed: {e}"}

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.json
        symbol = data.get("symbol")
        side = data.get("side")
        percentage = float(data.get("percentage", 0))
        if not symbol or not side or percentage <= 0:
            return jsonify({"status": "error", "message": "Invalid payload parameters"}), 400

        result = place_trade(symbol, side, percentage)
        return jsonify({"status": "success", "result": result}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=8080)
