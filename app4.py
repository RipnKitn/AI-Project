from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
import requests
import time
import hmac
import hashlib

# Load environment variables from .env
load_dotenv()

# Get API key and secret from environment variables
API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')

# Create Flask app
app = Flask(__name__)

# Function to generate HMAC signature (for authentication)
def generate_signature(secret, timestamp, method, request_path, body=""):
    message = f"{timestamp}{method}{request_path}{body}".encode()
    secret = secret.encode()
    return hmac.new(secret, message, hashlib.sha256).hexdigest()

@app.route('/')
def index():
    return "Coinbase API Integration Running"

@app.route('/buy', methods=['POST'])
def buy():
    data = request.json
    print(f"Received data: {data}")

    # Coinbase API endpoint for placing orders
    url = 'https://api.coinbase.com/v2/orders'
    
    # Generating the signature
    timestamp = str(int(time.time()))
    body = {
        'product_id': data['symbol'],
        'side': data['action'],
        'size': data['amount'],
        'price': data['price'],
        'order_type': data['order_type']
    }
    
    # Generate the signature
    signature = generate_signature(API_SECRET, timestamp, 'POST', '/v2/orders', str(body))
    
    # Coinbase API headers
    headers = {
        'CB-ACCESS-KEY': API_KEY,
        'CB-ACCESS-SIGN': signature,
        'CB-ACCESS-TIMESTAMP': timestamp,
        'Content-Type': 'application/json'
    }

    # Make the POST request to Coinbase
    response = requests.post(url, json=body, headers=headers)

    if response.status_code == 200:
        return jsonify({"message": "Order placed successfully", "data": response.json()}), 200
    else:
        return jsonify({"message": "Failed to place order", "error": response.text}), 400

if __name__ == '__main__':
    app.run(debug=True)
