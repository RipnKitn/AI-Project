import os
from flask import Flask, request, jsonify
import ccxt
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Load Coinbase API credentials from .env
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
API_PASSPHRASE = os.getenv("API_PASSPHRASE")

# Initialize Coinbase API client (using ccxt library here)
exchange = ccxt.coinbasepro({
    'apiKey': API_KEY,
    'secret': API_SECRET,
    'password': API_PASSPHRASE
})

# Define the webhook endpoint
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    print(f"Received data: {data}")
    
    # Extract details from the webhook payload
    symbol = data.get('symbol')
    price = data.get('price')
    action = data.get('action')
    amount = data.get('amount')
    order_type = data.get('order_type')

    if action == "buy":
        # Create a buy order (market order example)
        try:
            # You can change this logic to use limit orders if needed
            order = exchange.create_market_buy_order(symbol, amount)
            print(f"Order placed successfully: {order}")
            return jsonify({"message": "Order placed", "status": "200", "order": order}), 200
        except Exception as e:
            print(f"Error placing buy order: {e}")
            return jsonify({"message": "Error placing order", "status": "500", "error": str(e)}), 500

    elif action == "sell":
        # Create a sell order (market order example)
        try:
            # You can change this logic to use limit orders if needed
            order = exchange.create_market_sell_order(symbol, amount)
            print(f"Order placed successfully: {order}")
            return jsonify({"message": "Order placed", "status": "200", "order": order}), 200
        except Exception as e:
            print(f"Error placing sell order: {e}")
            return jsonify({"message": "Error placing order", "status": "500", "error": str(e)}), 500

    return jsonify({"message": "Invalid action", "status": "400"}), 400

@app.route('/')
def home():
    return "Flask app is running!"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
