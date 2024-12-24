import os
import time
import json
import hmac
import hashlib
import requests
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Coinbase API Credentials
API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')
BASE_URL = os.getenv('BASE_URL')

# Function to generate Coinbase API signature
def generate_signature(endpoint, body, timestamp):
    body_json = json.dumps(body)
    message = timestamp + body_json + endpoint
    return hmac.new(bytes(API_SECRET, 'utf-8'), message.encode('utf-8'), hashlib.sha256).hexdigest()

# Place order function
def place_giga_buy_order(size):
    try:
        endpoint = "/orders"
        url = f"{BASE_URL}{endpoint}"
        timestamp = str(int(time.time()))

        # GIGA-USDC order payload
        body = {
            "product_id": "GIGA-USDC",
            "side": "buy",
            "price": "1.00",  # Price in USD
            "size": size,     # Amount of the asset (GIGA)
            "client_order_id": f"order-{int(time.time())}"  # Unique ID
        }

        # Generate signature
        signature = generate_signature(endpoint, body, timestamp)

        # API request headers
        headers = {
            "CB-ACCESS-KEY": API_KEY,
            "CB-ACCESS-SIGN": signature,
            "CB-ACCESS-TIMESTAMP": timestamp,
            "Content-Type": "application/json"
        }

        # Print the request for debugging
        print("URL:", url)
        print("Headers:", headers)
        print("Body:", body)

        # Make the API request
        response = requests.post(url, headers=headers, json=body)

        # Print the response for debugging
        print("Response Status Code:", response.status_code)
        print("Response Body:", response.text)

        return response.json()

    except Exception as e:
        return {"error": f"Failed to place order: {str(e)}"}

# Webhook handler
from flask import Flask, request

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def handle_webhook():
    data = request.json
    print("Received webhook data:", data)
    
    # Example: Get the size from the incoming request body
    size = data.get("size", None)
    
    if size:
        # Call the function to place the order with the given size
        order_response = place_giga_buy_order(size)
        return json.dumps(order_response)
    else:
        return json.dumps({"error": "Missing 'size' in webhook data"}), 400

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
