import os
import time
import hmac
import hashlib
import base64
import json
import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Coinbase Advanced Trade API settings
API_KEY = os.getenv("COINBASE_API_KEY")
API_SECRET = os.getenv("COINBASE_API_SECRET")
BASE_URL = "https://api.coinbase.com/api/v3/brokerage"

# Generate signature
def generate_signature(request_path, body, timestamp, method):
    message = f"{timestamp}{method}{request_path}{body or ''}"
    hmac_key = base64.b64decode(API_SECRET)
    signature = hmac.new(hmac_key, message.encode(), hashlib.sha256)
    return base64.b64encode(signature.digest()).decode()

# Fetch account balance
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
    except requests.exceptions.RequestException as e:
        return {"error": f"Balance fetch failed: {e}"}

# Place a trade or check balance
def place_trade(symbol, side, percentage):
    try:
        if side == "check":  # New option to check balance
            base_currency = symbol.split("-")[0]
            balance = fetch_balance(base_currency)
            return {"balance": balance, "currency": base_currency}

        # Calculate trade amount
        base_currency = symbol.split("-")[0]
        balance = fetch_balance(base_currency)
        trade_amount = balance * (percentage / 100)

        if trade_amount <= 0:
            return {"error": "Insufficient balance"}

        # Simulated success response for trade
        return {"symbol": symbol, "side": side, "trade_amount": trade_amount, "status": "success"}
    except Exception as e:
        return {"error": f"Trade failed: {str(e)}"}

# Webhook route with basic security
@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        # Simple authentication (you can improve this further)
        secret = os.getenv("WEBHOOK_SECRET")
        signature = request.headers.get("X-Signature")
        if not signature or signature != secret:
            return jsonify({"status": "error", "message": "Unauthorized"}), 403
        
        data = request.json
        symbol = data.get("symbol")
        side = data.get("side")
        percentage = float(data.get("percentage", 0))

        if not symbol or not side:
            return jsonify({"status": "error", "message": "Invalid parameters"}), 400

        result = place_trade(symbol, side, percentage)
        return jsonify({"status": "success", "result": result}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=8080)
