import requests
import time
import hmac
import hashlib
import json
from dotenv import load_dotenv
import os

load_dotenv()  # This loads environment variables from .env file

# Retrieve API keys and other info from .env
API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')
BASE_URL = "https://api.pro.coinbase.com"  # Correct API endpoint for Coinbase Pro

def generate_signature(request_path, body, timestamp):
    """Generate the signature for Coinbase Pro requests."""
    body = json.dumps(body)  # Convert body to JSON string
    message = timestamp + request_path + body
    signature = hmac.new(
        bytes(API_SECRET, 'latin-1'),
        msg=bytes(message, 'latin-1'),
        digestmod=hashlib.sha256
    ).hexdigest()
    return signature

def place_giga_buy_order(size):
    """Place a buy order on Coinbase Pro for the GIGA-USDC pair."""
    try:
        # Endpoint to place orders on Coinbase Pro
        endpoint = "/orders"
        url = f"{BASE_URL}{endpoint}"
        timestamp = str(int(time.time()))

        # Build the request payload (body)
        body = {
            "product_id": "GIGA-USDC",  # The product you want to buy
            "side": "buy",  # Buy or sell (buy in this case)
            "price": "1.00",  # The price (can be omitted for market orders)
            "size": size,  # The amount of GIGA to buy
            "client_order_id": f"order-{timestamp}"  # Unique client order ID
        }

        # Generate signature for the request
        signature = generate_signature(endpoint, body, timestamp)

        # Request headers
        headers = {
            "CB-ACCESS-KEY": API_KEY,
            "CB-ACCESS-SIGN": signature,
            "CB-ACCESS-TIMESTAMP": timestamp,
            "Content-Type": "application/json"
        }

        # Make the API request
        response = requests.post(url, headers=headers, data=json.dumps(body))

        # Check response status
        if response.status_code == 200:
            print("Order placed successfully.")
            print(response.json())
        else:
            print(f"Failed to place order. Status code: {response.status_code}")
            print(response.text)

    except Exception as e:
        print(f"Error placing order: {e}")

# Test the order by calling the function with a size
place_giga_buy_order(1.0)
