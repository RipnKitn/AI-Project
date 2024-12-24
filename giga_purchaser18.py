import requests
import time
import json
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Coinbase API credentials
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
BASE_URL = "https://api.coinbase.com/v2"  # Correct endpoint for Coinbase

# Function to generate signature for Coinbase API (example method)
def generate_signature(endpoint, body, timestamp):
    # Signature generation logic here (ensure it's correct based on Coinbase documentation)
    pass

# Function to place the order
def place_giga_buy_order(size):
    try:
        endpoint = "/orders"
        url = f"{BASE_URL}{endpoint}"
        timestamp = str(int(time.time()))

        # Correct request body
        body = {
            "product_id": "GIGA-USDC",  # Assuming GIGA-USDC is available
            "side": "buy",
            "price": "1.00",  # Price in USD
            "size": size,  # Quantity of GIGA to buy
            "client_order_id": f"order-{timestamp}"  # Unique order ID
        }
        body_json = json.dumps(body)

        # Generate signature (you need to implement this)
        signature = generate_signature(endpoint, body_json, timestamp)

        # Request headers
        headers = {
            "CB-ACCESS-KEY": API_KEY,
            "CB-ACCESS-SIGN": signature,
            "CB-ACCESS-TIMESTAMP": timestamp,
            "Content-Type": "application/json"
        }

        # Make the POST request
        response = requests.post(url, headers=headers, data=body_json)

        # Print response for debugging
        print("URL:", url)
        print("Headers:", headers)
        print("Body:", body_json)
        print("Response Status Code:", response.status_code)
        print("Response Body:", response.text)

        if response.status_code == 200:
            print("Order placed successfully!")
        else:
            print(f"Error placing order: {response.text}")
        return response.json()

    except Exception as e:
        return {"error": f"Failed to place order: {str(e)}"}

# Example of using the function with a size of 1
response = place_giga_buy_order(1.0)
