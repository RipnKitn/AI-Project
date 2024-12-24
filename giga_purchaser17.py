from flask import Flask, request
import json
import time
import requests
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

# API Credentials
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
BASE_URL = os.getenv("BASE_URL", "https://api.coinbase.com/v2")

app = Flask(__name__)

# Function to generate the signature for Coinbase API
def generate_signature(endpoint, body, timestamp):
    # Replace this with the actual logic to generate the signature
    return "GENERATED_SIGNATURE"  # Placeholder for signature

# Place GIGA buy order using Coinbase API
def place_giga_buy_order(size):
    try:
        endpoint = "/orders"
        url = f"{BASE_URL}{endpoint}"
        timestamp = str(int(time.time()))

        # GIGA-USDC order payload
        body = {
            "product_id": "GIGA-USDC",
            "side": "buy",
            "price": "1.00",  # Set price to $1 for GIGA
            "size": size,     # Size comes from webhook data
            "client_order_id": f"order-{timestamp}"
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

        # Make the API request
        response = requests.post(url, headers=headers, data=body_json)

        # Return the response as JSON
        return response.json()

    except Exception as e:
        return {"error": f"Failed to place order: {str(e)}"}

# Webhook route that receives the trade size
@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.get_json()  # Ensure this is parsing JSON correctly
        print(f"Received webhook data: {data}")
        
        size = data.get('size')
        if not size:
            return {"error": "Missing 'size' in webhook data"}, 400
        
        # Call the function to place the order
        order_response = place_giga_buy_order(size)
        return order_response

    except Exception as e:
        return {"error": f"Failed to process webhook: {str(e)}"}, 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)  # Run Flask app
