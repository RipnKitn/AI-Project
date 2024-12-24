import os
import time
import hmac
import hashlib
import base64
import requests
from dotenv import load_dotenv
from flask import Flask, request, jsonify

# Load environment variables
load_dotenv()
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
BASE_URL = "https://api.coinbase.com/api/v3/brokerage"

# Initialize Flask
app = Flask(__name__)

# Ensure API credentials are loaded
if not API_KEY or not API_SECRET:
    raise ValueError("API_KEY or API_SECRET missing in .env file.")

# Generate Coinbase API signature
def generate_signature(request_path, body, timestamp, method):
    message = f"{timestamp}{method}{request_path}{body or ''}"
    hmac_key = base64.b64decode(API_SECRET)
    signature = hmac.new(hmac_key, message.encode(), hashlib.sha256)
    return base64.b64encode(signature.digest()).decode()

# Place trade order: $1 USDC for GIGA
def place_trade():
    endpoint = "/orders"
    url = f"{BASE_URL}{endpoint}"
    timestamp = str(int(time.time()))
    body = {
        "product_id": "GIGA-USDC",
        "side": "BUY",
        "order_configuration": {
            "market_market_ioc": {
                "quote_size": "1.00"  # Fixed $1 USDC
            }
        },
        "client_order_id": str(int(time.time()))
    }
    headers = {
        "CB-ACCESS-KEY": API_KEY,
        "CB-ACCESS-SIGN": generate_signature(endpoint, str(body), timestamp, "POST"),
        "CB-ACCESS-TIMESTAMP": timestamp,
        "Content-Type": "application/json"
    }
    response = requests.post(url, json=body, headers=headers)
    return response.json()

# Webhook endpoint
@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        print("Webhook received!")
        data = request.json
        if not data:
            return jsonify({"error": "No data received"}), 400
        
        result = place_trade()
        print(f"Trade result: {result}")
        return jsonify({"status": "success", "result": result}), 200
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

# Run Flask
if __name__ == "__main__":
    app.run(debug=True, port=80)
