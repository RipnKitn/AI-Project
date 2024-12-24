import os
import hmac
import hashlib
import time
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.get_json()
        print("Received webhook data:", data)

        product_id = data.get('product_id', 'GIGA-USDC')
        side = data.get('side', 'buy')
        size = data.get('size', 1.0)
        client_order_id = data.get('client_order_id', f'order-{int(time.time())}')

        # Place the order
        response = place_order(product_id, side, size, client_order_id)
        return jsonify(response), 200
    except Exception as e:
        print("Error handling webhook:", e)
        return jsonify({"error": str(e)}), 400

def place_order(product_id, side, size, client_order_id):
    try:
        api_key = os.getenv("API_KEY")
        api_secret = os.getenv("API_SECRET")
        base_url = os.getenv("BASE_URL", "https://api.coinbase.com/v2")

        timestamp = str(int(time.time()))
        request_path = '/orders'
        body = {
            "product_id": product_id,
            "side": side,
            "size": size,
            "client_order_id": client_order_id
        }
        body_json = str(body).replace("'", '"')  # Convert to JSON-like string

        message = timestamp + 'POST' + request_path + body_json
        signature = hmac.new(api_secret.encode(), message.encode(), hashlib.sha256).hexdigest()

        headers = {
            'CB-ACCESS-KEY': api_key,
            'CB-ACCESS-SIGN': signature,
            'CB-ACCESS-TIMESTAMP': timestamp,
            'Content-Type': 'application/json'
        }

        response = requests.post(base_url + request_path, headers=headers, json=body)

        if response.status_code == 200:
            return response.json()
        else:
            return {
                "error": f"Failed to place order: {response.status_code} - {response.text}"
            }

    except Exception as e:
        return {"error": f"Exception during order placement: {str(e)}"}

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
