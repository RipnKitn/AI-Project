import os
import time
import hmac
import hashlib
import base64
import json
import requests
from flask import Flask, request, jsonify

# Initialize Flask app
app = Flask(__name__)

# Load API credentials from .env file
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
BASE_URL = "https://api.coinbase.com/api/v3/brokerage"

# Ensure API_KEY and API_SECRET are loaded
if not API_KEY or not API_SECRET:
    raise ValueError("Missing API_KEY or API_SECRET in .env file")

# Load ngrok URL from config.json
with open("config.json") as config_file:
    config = json.load(config_file)
    NGROK_URL = config.get("ngrok_url")

# Debug log
print(f"Loaded API_KEY: {API_KEY}, Loaded API_SECRET: {API_SECRET}")
print(f"Loaded NGROK_URL: {NGROK_URL}")

# Generate a signature for Coinbase API requests
def generate_signature(request_path, body, timestamp, method):
    message = f"{timestamp}{method}{request_path}{body or ''}"
    hmac_key = base64.b64decode(API_SECRET)
    signature = hmac.new(hmac_key, message.encode(), hashlib.sha256)
    return base64.b64encode(signature.digest()).decode()

# Function to execute a trade on Coinbase
def place_trade(symbol, side, quantity):
    try:
        endpoint = "/orders"
        url = f"{BASE_URL}{endpoint}"
        timestamp = str(int(time.time()))

        # Prepare trade details
        body = {
            "product_id": symbol,
            "side": side,
            "order_type": "market",
            "size": quantity
        }
        body_json = json.dumps(body)

        # Generate signature
        signature = generate_signature(endpoint, body_json, timestamp, "POST")

        # Prepare headers
        headers = {
            "CB-ACCESS-KEY": API_KEY,
            "CB-ACCESS-SIGN": signature,
            "CB-ACCESS-TIMESTAMP": timestamp,
            "Content-Type": "application/json"
        }

        # Debug request details
        print(f"Request URL: {url}")
        print(f"Request Headers: {headers}")
        print(f"Request Body: {body_json}")

        # Send POST request to Coinbase API
        response = requests.post(url, headers=headers, data=body_json)
        print(f"Response Status: {response.status_code}")
        print(f"Response Body: {response.text}")
        response.raise_for_status()
        return {"message": "Trade executed successfully", "response": response.json()}
    except Exception as e:
        print(f"Trade execution failed: {str(e)}")
        return {"error": f"Trade execution failed: {str(e)}"}

# Webhook route to handle TradingView alerts
@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.json
        print(f"Received data: {data}")  # Log the received data
        symbol = data.get("symbol")
        side = data.get("side")
        quantity = data.get("quantity")

        if not symbol or not side or not quantity:
            return jsonify({"status": "error", "message": "Missing parameters!"}), 400

        # Execute trade
        result = place_trade(symbol, side, quantity)
        return jsonify({"status": "success", "message": "Webhook processed successfully", "result": result}), 200
    except Exception as e:
        print(f"Webhook error: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True, port=80)
