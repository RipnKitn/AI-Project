import os
import json
import time
import requests
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
BASE_URL = os.getenv("BASE_URL", "https://api.coinbase.com/v2")  # Update this URL to use the correct Coinbase One API

def generate_signature(endpoint, body, timestamp):
    # Signature generation logic goes here (depending on Coinbase's requirements)
    pass

def place_giga_buy_order(size):
    try:
        endpoint = "/orders"  # Coinbase One orders endpoint
        url = f"{BASE_URL}{endpoint}"
        timestamp = str(int(time.time()))

        # GIGA-USDC order payload
        body = {
            "product_id": "GIGA-USDC",
            "side": "buy",
            "price": "1.00",  # Adjust the price if needed
            "size": size,  # Trade size in USDC
            "client_order_id": f"order-{timestamp}"  # Unique ID for each order
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

        # Print the request for debugging
        print("URL:", url)
        print("Headers:", headers)
        print("Body:", body_json)

        # Make the API request
        response = requests.post(url, headers=headers, data=body_json)

        # Print the response for debugging
        print("Response Status Code:", response.status_code)
        print("Response Body:", response.text)

        return response.json()

    except Exception as e:
        print(f"Error placing order: {str(e)}")
        return {"error": f"Failed to place order: {str(e)}"}

# Example call to place a buy order
size = 1.00  # This is the size in USDC
place_giga_buy_order(size)
