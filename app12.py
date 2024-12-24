from flask import Flask, request, jsonify
import json
import requests

app = Flask(__name__)

# Set up logging to capture errors and requests
import logging
logging.basicConfig(level=logging.INFO)

# The webhook route
@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        # Receive data from the webhook
        data = request.get_json()  # Parse incoming JSON data
        if not data:
            return jsonify({"message": "No JSON received"}), 400

        logging.info(f"Received data: {json.dumps(data)}")

        # Extract relevant information from the data
        symbol = data.get('symbol')
        price = data.get('price')
        action = data.get('action')
        amount = data.get('amount')
        order_type = data.get('order_type')

        # Check if all required fields are present
        if not all([symbol, price, action, amount, order_type]):
            return jsonify({"message": "Missing required data"}), 400

        # Placeholder for sending the order to Coinbase (or your exchange)
        # Replace this with actual code to send the buy/sell order to the exchange
        order_response = place_order(symbol, price, action, amount, order_type)

        if order_response.status_code == 200:
            return jsonify({"message": "Success", "status": "200"}), 200
        else:
            return jsonify({"message": "Error placing order", "status": "500"}), 500

    except Exception as e:
        logging.error(f"Error processing webhook: {str(e)}")
        return jsonify({"message": f"Internal error: {str(e)}"}), 500


# A placeholder for order placing (to be replaced with actual API call)
def place_order(symbol, price, action, amount, order_type):
    # Here you can replace with real logic to place orders with Coinbase or another exchange
    # For example:
    # response = requests.post('https://api.exchange.com/order', data={})
    # return response
    # For now, just simulate a successful response
    return requests.Response()  # You can mock the response here for testing


# Health check endpoint (to test if the server is up)
@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Flask app is running!"}), 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
