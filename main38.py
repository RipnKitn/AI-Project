import os
import time
import hmac
import hashlib
import base64
import requests
from dotenv import load_dotenv
from flask import Flask, request, jsonify

# Load environment variables from .env file
load_dotenv()

# Coinbase API credentials
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
BASE_URL = "https://api.coinbase.com/api/v3/brokerage"

# Flask app setup
app = Flask(__name__)

def generate_signature(request_path, body, timestamp, method):
    message = f"{timestamp}{method}{request_path}{body or ''}"
    hmac_key = base64.b64decode(API_SECRET)
    signature = hmac.new(hmac_key, message.encode(), hashlib.sha256)
    return base64.b64encode(signature.digest()).decode()

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

        # Debugging: Print the status code and the response body
        print("Status Code:", response.status_code)
        print("Response Body:", response.json())

        response.raise_for_status()  # Raise error for bad status codes

        accounts = response.json().get("accounts", [])
        for account in accounts:
            if account["currency"] == currency:
                return float(account["available_balance"]["value"])
        return 0.0
    except Exception as e:
        print(f"Error fetching balance: {e}")
        return 0.0

def place_trade(symbol, side, amount):
    try:
        base_currency = "USDC" if side == "buy" else symbol.split("-")[0]
        balance = fetch_balance(base_currency)
        
        if balance <= 0:
            print("Insufficient balance for trade")
            return {"error": "Insufficient balance"}
        
        # Calculate trade amount based on available balance (if percentage)
        trade_amount = amount if isinstance(amount, (int, float)) else balance * 0.20  # Default to 20%
        trade_amount = round(trade_amount, 2)
        
        # Prepare the trade order details
        order = {
            "symbol": symbol,
            "side": side,
            "trade_amount": trade_amount
        }
        
        print(f"Placing trade - Symbol: {symbol}, Side: {side}, Amount: {trade_amount}")
        
        # If you were to use an API to place the trade, you would call it here.
        # e.g., requests.post(COINBASE_TRADE_API, json=order)
        
        return {"message": f"Order placed: {order}"}
    
    except Exception as e:
        print(f"Error placing trade: {e}")
        return {"error": "Trade failed"}

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.json
        symbol = data.get("symbol")
        side = data.get("side")
        amount = data.get("amount", 1)  # Default to 1 if not provided

        if not symbol or not side:
            return jsonify({"status": "error", "message": "Invalid parameters"}), 400

        result = place_trade(symbol, side, amount)
        return jsonify({"status": "success", "result": result}), 200

    except Exception as e:
        print(f"Webhook error: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=80)
