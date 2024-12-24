import os
from dotenv import load_dotenv
import time
import hmac
import hashlib
import base64
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
BASE_URL = "https://api.coinbase.com/api/v3/brokerage"

# Generate signature
def generate_signature(request_path, body, timestamp, method):
    message = f"{timestamp}{method}{request_path}{body or ''}"
    hmac_key = base64.b64decode(API_SECRET)
    signature = hmac.new(hmac_key, message.encode(), hashlib.sha256)
    return base64.b64encode(signature.digest()).decode()

# Fetch account balance for a currency with debug
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
        print("Full Response from Coinbase API:", response.json())  # Debug: print full response
        accounts = response.json().get("accounts", [])
        for account in accounts:
            if account["currency"] == currency:
                print(f"Balance for {currency}: {account['available_balance']['value']}")  # Debug
                return float(account["available_balance"]["value"])
        print(f"Currency {currency} not found.")  # Debug
        return 0.0
    except Exception as e:
        print(f"Error fetching balance: {e}")  # Debug
        return {"error": f"Balance fetch failed: {e}"}

# Place a buy/sell order
def place_trade(symbol, side):
    try:
        base_currency = symbol.split("-")[0]
        balance = fetch_balance(base_currency)

        if balance <= 0:
            return {"error": f"Insufficient balance for {base_currency}"}

        percentage = 0.20
        trade_amount = balance * percentage

        order = {
            "symbol": symbol,
            "side": side,
            "trade_amount": trade_amount
        }
        return order
    except Exception as e:
        return {"error": f"Trade failed: {str(e)}"}

# Test route to verify server is running
@app.route("/")
def home():
    return "Flask server is running!"

# Webhook route
@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.json
        symbol = data.get("symbol")
        side = data.get("side")

        if not symbol or not side:
            return jsonify({"status": "error", "message": "Invalid parameters"}), 400

        result = place_trade(symbol, side)
        return jsonify({"status": "success", "result": result}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=80)
