from flask import Flask, request, jsonify
import time
import hmac
import hashlib
import base64
import requests
import json

app = Flask(__name__)

# Coinbase API credentials
API_KEY = "your_api_key"
API_SECRET = """-----BEGIN EC PRIVATE KEY-----
your_api_secret
-----END EC PRIVATE KEY-----"""
BASE_URL = "https://api.coinbase.com/api/v3/brokerage"

# Function to generate signature
def generate_signature(request_path, body, timestamp, method):
    message = f"{timestamp}{method}{request_path}{body or ''}"
    hmac_key = base64.b64decode(API_SECRET)
    signature = hmac.new(hmac_key, message.encode(), hashlib.sha256)
    return base64.b64encode(signature.digest()).decode()

# Endpoint to receive TradingView webhook
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid data"}), 400

    try:
        symbol = data.get("symbol", "GIGA-USDC")
        side = data.get("side", "buy")
        quantity = data.get("quantity", "1")

        # Send trade to Coinbase
        response = place_coinbase_order(symbol, side, quantity)
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Function to place a Coinbase order
def place_coinbase_order(symbol, side, quantity):
    endpoint = "/orders"
    url = f"{BASE_URL}{endpoint}"
    timestamp = str(int(time.time()))

    body = {
        "product_id": symbol,
        "side": side,
        "order_type": "market",
        "size": quantity
    }
    body_json = json.dumps(body)

    signature = generate_signature(endpoint, body_json, timestamp, "POST")
    headers = {
        "CB-ACCESS-KEY": API_KEY,
        "CB-ACCESS-SIGN": signature,
        "CB-ACCESS-TIMESTAMP": timestamp,
        "Content-Type": "application/json"
    }

    response = requests.post(url, headers=headers, data=body_json)
    return {
        "status_code": response.status_code,
        "response_body": response.json()
    }

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
