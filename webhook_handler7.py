import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
import requests

# Load environment variables from .env
load_dotenv()

# Flask app initialization
app = Flask(__name__)

# API credentials loaded from .env file
API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')

# Coinbase API endpoint (replace this with actual API URL)
COINBASE_API_URL = "https://api.coinbase.com/v2/orders"

@app.route('/', methods=['POST'])
def webhook():
    # Get the JSON data from TradingView
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data received"}), 400

    symbol = data.get('symbol')
    action = data.get('action')
    amount = data.get('amount')
    price = data.get('price')
    order_type = data.get('order_type')

    # You can add further logic to trigger actual buy/sell API requests here.

    print(f"Received data: {data}")

    # Sample response (you can modify as per your requirement)
    response = {
        'symbol': symbol,
        'action': action,
        'amount': amount,
        'price': price,
        'order_type': order_type
    }
    
    # Return response to TradingView
    return jsonify(response), 200

# Start Flask app
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
