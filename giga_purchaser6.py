import time
import hmac
import hashlib
import base64
import json
import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

# Retrieve API credentials from environment variables
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
BASE_URL = os.getenv("BASE_URL")

# Initialize Flask app
app = Flask(__name__)

# Generate Coinbase API signature
def generate_signature(endpoint, body, timestamp):
    try:
        message = f"{timestamp}POST{endpoint}{body}"
        hmac_key = base64.b64decode(API_SECRET)
        signature = hmac.new(hmac_key, message.encode("utf-8"), hashlib.sha256)
        return base64.b64encode(signature.digest()).decode()
    except Exception as e:
        return f"Error generating signature: {e}"

# Place a buy order for GIGA-USDC
def place_giga_buy_order(size):
    try:
        endpoint = "/orders"
        url = f"{BASE_URL}{endpoint}"
        timestamp = str(int(time.time()))

        # GIGA-USDC order payload
        body = {
            "product_id": "GIGA-USDC",
            "side": "buy",
            "order_configuration": {
                "market_market_ioc": {
                    "quote_size": size  # Trade size in USDC
                }
            },
            "client_order_id": f"order-{int(time.time())}"  # Unique ID
        }
        body_json = json.dumps(body)

        # Generate signature
        signature = generate_signature(endpoint, body_json, timestamp)

        # API request headers
        headers = {
            "CB-ACCESS-KEY": API_KEY,
            "CB-ACCESS-SIGN": signature,
            "CB-ACCESS-TIMESTAMP": timestamp,
            "Content-Type": "application/json"
        }

        # Make the API request
        response = requests.post(url, headers=headers, data=body_json)

        # Log the response
        print("Request URL:", url)
        print("Request Headers:", headers)
        print("Request Body:", body_json)
        print("Response Status Code:", response.status_code)
        print("Response Body:", response.text)

        return response.json()

    except Exception as e:
        return {"error": f"Failed to place order: {str(e)}"}

# Webhook endpoint for placing GIGA-USDC orders
@app.route("/webhook", methods=["POST"])
def webhook_handler():
    try:
        data = request.json
        print(f"Received webhook data: {data}")  # Debugging line

        size = data.get("size", "1.00")  # Default $1 trade
        print(f"Trade size: {size}")  # Debugging line

        # Place the buy order for GIGA-USDC
        result = place_giga_buy_order(size)
        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Start the Flask server
if __name__ == "__main__":
    app.run(debug=True, port=5000)
