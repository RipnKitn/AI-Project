from flask import Flask, request, jsonify
import os
import json
import time
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API credentials from environment variables
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
BASE_URL = os.getenv("BASE_URL")

# Initialize Flask app
app = Flask(__name__)

# Function to generate Coinbase signature (use your own method)
def generate_signature(endpoint, body, timestamp):
    # Implement the signature generation logic according to Coinbase API documentation
    return "YOUR_GENERATED_SIGNATURE"

# Function to place GIGA buy order on Coinbase
def place_giga_buy_order(size):
    try:
        # Coinbase API endpoint for placing an order
        endpoint = "/orders"
        url = f"{BASE_URL}{endpoint}"
        timestamp = str(int(time.time()))  # Use current Unix timestamp

        # GIGA-USDC order payload
        body = {
            "product_id": "GIGA-USDC",  # This is your product pair
            "side": "buy",  # Buying the asset
            "order_configuration": {
                "market_market_ioc": {
                    "quote_size": size  # Trade size in USDC
                }
            },
            "client_order_id": f"order-{timestamp}"  # Use timestamp for unique order ID
        }
        body_json = json.dumps(body)

        # Generate signature
        signature = generate_signature(endpoint, body_json, timestamp)

        # API request headers
        headers = {
            "CB-ACCESS-KEY": API_KEY,
            "CB-ACCESS-SIGN": signature,
            "CB-ACCESS-TIMESTAMP": timestamp,
            "Content-Type": "application/json"
        }

        # Make the API request to Coinbase
        response = requests.post(url, headers=headers, data=body_json)

        # Print the response status and body for debugging
        print("Response Status Code:", response.status_code)
        print("Response Body:", response.text)

        return response.json()

    except Exception as e:
        return {"error": f"Failed to place order: {str(e)}"}

# Define the webhook route that will receive data
@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.get_json()  # Get the JSON data sent in the POST request
        print("Received webhook data:", data)

        # Extract size from the webhook data
        size = data.get('size')
        if not size:
            return jsonify({"error": "Missing 'size' in webhook data"}), 400

        # Place GIGA buy order with the specified size
        result = place_giga_buy_order(size)

        # Return the result of the order attempt
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
