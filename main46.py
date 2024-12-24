import os
import hmac
import hashlib
import base64
import time
from flask import Flask, request, jsonify
from dotenv import load_dotenv

# Initialize Flask app
app = Flask(__name__)

# Load API keys from .env file
load_dotenv()
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")

# Coinbase API Base URL
BASE_URL = "https://api.coinbase.com/api/v3/brokerage"

# Function to create Coinbase signature
def generate_signature(request_path, body, timestamp, method):
    message = f"{timestamp}{method}{request_path}{body or ''}"
    hmac_key = base64.b64decode(API_SECRET)
    signature = hmac.new(hmac_key, message.encode(), hashlib.sha256)
    return base64.b64encode(signature.digest()).decode()

# Handle TradingView Webhook
@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.json
        symbol = data.get("symbol")
        side = data.get("side")

        # Validate input
        if not symbol or not side:
            return jsonify({"status": "error", "message": "Invalid parameters"}), 400

        # Print request for debugging
        print(f"Webhook received: Symbol={symbol}, Side={side}")

        # Simulate order placement
        return jsonify({"status": "success", "message": f"Order {side} for {symbol} received"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# Run Flask server
if __name__ == "__main__":
    app.run(debug=True, port=80)
