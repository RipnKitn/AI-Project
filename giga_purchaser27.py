import os
import hmac
import hashlib
import time
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Load environment variables
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
BASE_URL = os.getenv("BASE_URL", "https://api.coinbase.com/api/v3/brokerage/orders")

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        # Parse incoming webhook data
        data = request.get_json()
        print("Received webhook data:", data)

        # Extract relevant parameters
        product_id = data.get('product_id', 'GIGA-USDC')
        side = data.get('side', 'buy')
        size = data.get('size', 1.0)
        client_order_id = data.get('client_order_id', f'order-{int(time.time())}')

        # Place the order
        response = place_order(product_id, side, size, client_order_id)
        return jsonify(response), 200

    except Exception as e:
        print(f"Error in webhook: {e}")
        return jsonify({"error": str(e)}), 400

def place_order(product_id, side, size, client_order_id):
    try:
        # Create timestamp and message for HMAC signature
        timestamp = str(int(time.time()))
        request_path = "/api/v3/brokerage/orders"
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
        message = timestamp + "POST" + request_path + str(body).replace("'", '"')
        signature = hmac.new(API_SECRET.encode(), message.encode(), hashlib.sha256).hexdigest()

        # Prepare headers
        headers = {
            "CB-ACCESS-KEY": API_KEY,
            "CB-ACCESS-SIGN": signature,
            "CB-ACCESS-TIMESTAMP": timestamp,
            "Content-Type": "application/json"
        }

        # Make API request to Coinbase
        response = requests.post(BASE_URL, headers=headers, json=body)
        response_data = response.json()

        if response.status_code == 200:
            return response_data
        else:
            return {"error": f"Failed to place order: {response.status_code} - {response.text}"}

    except Exception as e:
        print(f"Error placing order: {e}")
        return {"error": str(e)}

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)