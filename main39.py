import os
import time
import hmac
import hashlib
import base64
import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Coinbase API credentials
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
BASE_URL = "https://api.coinbase.com/api/v3/brokerage"

# Generate signature for Coinbase API requests
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
        print(f"Error fetching balance: {e}")
        return 0.0

# Place a buy/sell order on Coinbase
def place_trade(symbol, side):
    try:
        print(f"Placing trade - Symbol: {symbol}, Side: {side}")
        base_currency = "USDC" if side == "buy" else symbol.split("-")[0]
        balance = fetch_balance(base_currency)
        
        # Validate the balance
        if balance <= 0:
            return {"error": "Insufficient or invalid balance"}
        
        # Calculate the trade amount (20% of the balance)
        percentage = 0.20
        trade_amount = round(balance * percentage, 2)
        
        # Ensure the trade amount doesn't exceed the balance
        trade_amount = min(trade_amount, balance)
        
        # Prepare the order details
        order = {
            "symbol": symbol,
            "side": side,
            "trade_amount": trade_amount
        }
        print(f"Order details: {order}")
        
        # Place the order (add your API call here to place the order)
        return {"message": f"Order placed: {order}"}
    except Exception as e:
        print(f"Trade failed: {e}")
        return {"error": f"Trade failed: {e}"}

# Webhook route to receive TradingView alerts
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
    app.run(debug=True, host="0.0.0.0", port=80)
