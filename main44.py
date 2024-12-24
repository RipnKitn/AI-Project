import os
import time
import hmac
import hashlib
import base64
import requests
from dotenv import load_dotenv
from flask import Flask, request, jsonify

# Initialize Flask app
app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
BASE_URL = "https://api.coinbase.com/api/v3/brokerage"

# Ensure that the API_KEY and API_SECRET are loaded correctly
if not API_KEY or not API_SECRET:
    raise ValueError("Missing API_KEY or API_SECRET in .env file")

# Generate a signature to authenticate API requests
def generate_signature(request_path, body, timestamp, method):
    message = f"{timestamp}{method}{request_path}{body or ''}"
    hmac_key = base64.b64decode(API_SECRET)
    signature = hmac.new(hmac_key, message.encode(), hashlib.sha256)
    return base64.b64encode(signature.digest()).decode()

# Fetch account balance for a given currency
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
        response.raise_for_status()  # Raises an exception for HTTP errors
        accounts = response.json().get("accounts", [])
        for account in accounts:
            if account["currency"] == currency:
                return float(account["available_balance"]["value"])
        return 0.0
    except Exception as e:
        print(f"Balance fetch failed: {e}")
        return {"error": f"Balance fetch failed: {e}"}

# Place a buy/sell order (Fixed $1 of USDC for GIGA)
def place_trade(symbol, side):
    try:
        print(f"Placing trade - Symbol: {symbol}, Side: {side}")

        # For now, always trade $1 of USDC for GIGA
        trade_amount = 1.00  # Fixed $1 trade amount
        print(f"Fixed trade amount: {trade_amount} USDC")

        # Check balance before making the trade
        balance = fetch_balance("USDC")
        print(f"Balance for USDC: {balance}")

        if balance < trade_amount:
            print("Insufficient balance")
            return {"error": "Insufficient balance"}

        # Prepare the trade order details
        order = {
            "symbol": symbol,
            "side": side,
            "trade_amount": trade_amount
        }
        print(f"Order details: {order}")

        # Here you would execute the order via the API, but it's commented out for now
        # response = requests.post(order_endpoint, json=order)
        return {"message": f"Order placed: {order}"}

    except Exception as e:
        print(f"Trade failed: {str(e)}")
        return {"error": f"Trade failed: {str(e)}"}

# Webhook route to handle incoming TradingView alerts
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
        print(f"Webhook error: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=80)
