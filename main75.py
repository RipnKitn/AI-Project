import os
import hmac
import hashlib
import time
import requests
from flask import Flask, request, jsonify

# Load environment variables
API_KEY = os.getenv("API_KEY")
API_SECRET_FILE = os.getenv("API_SECRET_FILE", "api_secret.txt")  # Default file if not set
BASE_URL = "https://api.coinbase.com/api/v3/brokerage"
TRADE_PERCENTAGE = 2  # Use 2% of your balance for each trade

# Load API Secret
try:
    with open(API_SECRET_FILE, "r") as file:
        API_SECRET = file.read().strip()
except FileNotFoundError:
    raise RuntimeError(f"API secret file not found at: {API_SECRET_FILE}")
except Exception as e:
    raise RuntimeError(f"Failed to load API secret: {e}")

# Initialize Flask app
app = Flask(__name__)

# Helper function: Get balance
def get_balance(currency):
    """Fetch the balance of a specific currency."""
    try:
        timestamp = str(int(time.time()))
        request_path = "/accounts"
        message = f"{timestamp}GET{request_path}"
        signature = hmac.new(API_SECRET.encode(), message.encode(), hashlib.sha256).hexdigest()

        headers = {
            "CB-ACCESS-KEY": API_KEY,
            "CB-ACCESS-SIGN": signature,
            "CB-ACCESS-TIMESTAMP": timestamp,
        }

        response = requests.get(BASE_URL + request_path, headers=headers)
        if response.status_code == 200:
            accounts = response.json().get("accounts", [])
            for account in accounts:
                if account["currency"] == currency:
                    return float(account["available_balance"]["value"])
        return 0.0
    except Exception as e:
        print(f"Error fetching balance for {currency}: {e}")
        return 0.0

# Helper function: Place an order
def place_order(product_id, side, size, client_order_id):
    """Place a buy or sell order."""
    try:
        timestamp = str(int(time.time()))
        request_path = "/orders"
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
        body_json = str(body).replace("'", '"')  # Convert to JSON string
        message = f"{timestamp}POST{request_path}{body_json}"
        signature = hmac.new(API_SECRET.encode(), message.encode(), hashlib.sha256).hexdigest()

        headers = {
            "CB-ACCESS-KEY": API_KEY,
            "CB-ACCESS-SIGN": signature,
            "CB-ACCESS-TIMESTAMP": timestamp,
            "Content-Type": "application/json"
        }

        response = requests.post(BASE_URL + request_path, headers=headers, json=body)
        return response.json() if response.status_code == 200 else {"error": response.text}
    except Exception as e:
        return {"error": f"Order placement failed: {str(e)}"}

# Webhook endpoint
@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid webhook payload"}), 400

        # Extract details from webhook
        product_id = data.get("product_id")  # Must be specified (e.g., "GIGA-USDC")
        side = data.get("side")  # Must be "buy" or "sell"
        if not product_id or not side:
            return jsonify({"error": "Missing required fields: product_id or side"}), 400

        # Determine the trade size
        base_currency, quote_currency = product_id.split("-")
        balance_currency = quote_currency if side == "buy" else base_currency  # USDC for buy, GIGA for sell
        total_balance = get_balance(balance_currency)
        if total_balance <= 0:
            return jsonify({"error": f"Insufficient balance in {balance_currency}"}), 400

        trade_size = round((total_balance * TRADE_PERCENTAGE) / 100, 2)  # 2% of balance
        if trade_size < 1:
            return jsonify({"error": "Trade size too small"}), 400

        client_order_id = data.get("client_order_id", f"order-{int(time.time())}")

        # Log incoming request
        print(f"Webhook received: {data}, Calculated Trade Size: {trade_size}")

        # Place the order
        response = place_order(product_id, side, trade_size, client_order_id)
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"error": f"Webhook handling failed: {str(e)}"}), 500

# Start the app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
