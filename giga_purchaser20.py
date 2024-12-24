import os
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.get_json()  # Parse incoming JSON
        print("Received data:", data)

        # Extract required fields
        product_id = data.get('product_id', 'GIGA-USDC')
        side = data.get('side', 'buy')
        size = data.get('size', 1.0)
        client_order_id = data.get('client_order_id', 'order-1234567890')

        # Simulate Coinbase order placement
        response = place_order(product_id, side, size, client_order_id)
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

def place_order(product_id, side, size, client_order_id):
    # Mock order placement logic
    print(f"Placing order: {product_id}, {side}, {size}, {client_order_id}")
    return {"status": "success", "order_id": client_order_id}

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
