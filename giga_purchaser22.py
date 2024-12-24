import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Load environment variables
API_KEY = os.getenv('COINBASE_API_KEY')
API_SECRET = os.getenv('COINBASE_API_SECRET')
API_PASSPHRASE = os.getenv('COINBASE_API_PASSPHRASE')
API_URL = 'https://api.coinbase.com/api/v3/brokerage/orders'

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.get_json()
        print("Received data:", data)

        # Extract required fields
        product_id = data.get('product_id', 'GIGA-USDC')
        side = data.get('side', 'buy')
        size = data.get('size', 1.0)
        client_order_id = data.get('client_order_id', 'order-1234567890')

        # Place order via Coinbase API
        response = place_order(product_id, side, size, client_order_id)
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

def place_order(product_id, side, size, client_order_id):
    # Construct the order payload
    order = {
        'product_id': product_id,
        'side': side,
        'size': size,
        'client_order_id': client_order_id,
        # Add other necessary parameters as required by the API
    }

    # Make the API request
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {API_KEY}',
        # Include any other headers required by Coinbase
    }

    response = requests.post(API_URL, json=order, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to place order: {response.text}")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
