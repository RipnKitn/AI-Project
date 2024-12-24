from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
import hmac
import hashlib
import base64
import time
import requests

# Initialize Flask app
app = Flask(__name__)
load_dotenv()  # Load API keys from .env file

# API Keys and Secrets (ensure these are set in your .env file)
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
BASE_URL = "https://api.coinbase.com/api/v3/brokerage"  # Coinbase API endpoint

# Generate signature for secure requests
def generate_signature(request_path, body, timestamp, method):
    message = f"{timestamp}{method}{request_path}{body or ''}"
    hmac_key = base64.b64decode(API_SECRET)
    signature = hmac.new(hmac_key, message.encode(), hashlib.sha256)
    return base64.b64encode(signature.digest()).decode()

# Fetch balance of a specific currency
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
        print(f"Error fetching balance: {e}")
        return 0.0

# Place a trade order (buy or sell)
def place_trade(symbol, side):
    try:
        base_currency = "USDC" if side == "buy" else symbol.split("-")[0]
        balance = fetch_balance(base_currency)

        if not balance or balance <= 0:
            print("Insufficient balance for trade")
            return {"error": "Insufficient balance"}

        trade_amount = min(balance * 0.2, balance)  # Trade with 20% of available balance
        order = {
            "symbol": symbol,
            "side": side,
            "trade_amount": trade_amount
        }

        # Prepare the order and send it to Coinbase
        # (Mocked API call; replace with actual Coinbase API call if necessary)
        print(f"Placing order: {order}")
        return {"status": "success", "order": order}

    except Exception as e:
        print(f"Trade failed: {e}")
        return {"error": str(e)}

# Webhook route to receive alerts from TradingView
@app.route('/webhook', methods=['POST'])
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
        print(f"Webhook error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

# Start Flask app
if __name__ == "__main__":
    app.run(debug=True, port=80)
