import os
import hmac
import hashlib
import uuid  # For generating unique order IDs
import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Coinbase API credentials
API_KEY = os.getenv("API_KEY")
API_SECRET_FILE = os.getenv("API_SECRET_FILE")
BASE_URL = "https://api.coinbase.com/api/v3/brokerage/orders"

# Load API secret
try:
    with open(API_SECRET_FILE, "r") as file:
        API_SECRET = file.read().strip()
except Exception as e:
    raise RuntimeError(f"Failed to load API secret: {e}")

# Webhook secret key (ensure security)
WEBHOOK_SECRET_KEY = os.getenv("WEBHOOK_SECRET_KEY", "your_secret_key_here")

# Flask app initialization
app = Flask(__name__)

# Helper function: HMAC signature generator
def generate_signature(timestamp, method, request_path, body):
    message = f"{timestamp}{method.upper()}{request_path}{body}"
    return hmac.new(API_SECRET.encode(), message.encode(), hashlib.sha256).hexdigest()

# Helper function: Place an order
def place_order(product_id, side, size, client_order_id):
    try:
        timestamp = str(int(time.time()))
        body = {
            "product_id": product_id,
            "side": side,
            "order_configuration": {
                "market_market_ioc": {
                    "quote_size": str(size)
                }
            },
            "client_order_id": client_order_id
        }
        body_json = str(body).replace("'", '"')  # JSON-like string
        signature = generate_signature(timestamp, "POST", "/api/v3/brokerage/orders", body_json)

        headers = {
            "CB-ACCESS-KEY": API_KEY,
            "CB-ACCESS-SIGN": signature,
            "CB-ACCESS-TIMESTAMP": timestamp,
            "Content-Type": "application/json"
        }

        response = requests.post(BASE_URL, headers=headers, json=body)

        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Order failed: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Exception during order placement: {str(e)}"}

# Webhook endpoint
@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        # Parse and validate webhook payload
        data = request.get_json()
        if data.get("secret") != WEBHOOK_SECRET_KEY:
            return jsonify({"error": "Unauthorized"}), 401

        print("Authorized webhook received:", data)

        # Extract trading parameters
        product_id = data.get("product_id", "BTC-USD")  # Default to BTC-USD
        side = data.get("side", "buy")  # "buy" or "sell"
        size = data.get("size", 1.0)  # Default trade size
        client_order_id = data.get("client_order_id", str(uuid.uuid4()))  # Unique ID

        # Place the order
        response = place_order(product_id, side, size, client_order_id)
        return jsonify(response), 200
    except Exception as e:
        print("Error handling webhook:", e)
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5000)
