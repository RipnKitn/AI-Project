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

# Check if the API_KEY and API_SECRET are loaded correctly
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")

# Check if keys are correctly loaded
if not API_KEY or not API_SECRET:
    raise ValueError("API_KEY or API_SECRET is missing in .env file")

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
        print(f"Balance fetch failed: {e}")
        return {"error": f"Balance fetch failed: {e}"}

# Place a buy/sell order
def place_trade(symbol, side):
    try:
        print(f"Placing trade - Symbol: {symbol}, Side: {side}")
        base_currency = "USDC" if side == "buy" else symbol.split("-")[0]
        print(f"Base currency for balance check: {base_currency}")

        balance = fetch_balance(base_currency)
        print(f"Balance for {base_currency}: {balance}")

        if not isinstance(balance, (int, float)) or balance <= 0:
            print("Insufficient or invalid balance")
            return {"error": "Insufficient or invalid balance"}

        # Calculate trade amount (20% of balance)
        percentage = 0.20
        trade_amount = round(balance * percentage, 2)
        print(f"Calculated trade amount: {trade_amount}")

        # Ensure the trade amount does not exceed available balance
        trade_amount = min(trade_amount, balance)

        order = {
            "symbol": symbol,
            "side": side,
            "trade_amount": trade_amount
        }
        print(f"Order details: {order}")
        return {"message": f"Order placed: {order}"}

    except Exception as e:
        print(f"Trade failed: {str(e)}")
        return {"error": f"Trade failed: {str(e)}"}

# Webhook route
@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.json
        print(f"Received webhook data: {data}")  # Debug print
        symbol = data.get("symbol")
        side = data.get("side")

        if not symbol or not side:
            return jsonify({"status": "error", "message": "Invalid parameters"}), 400

        result = place_trade(symbol, side)
        return jsonify({"status": "success", "result": result}), 200
    except Exception as e:
        print(f"Webhook error: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=80)
