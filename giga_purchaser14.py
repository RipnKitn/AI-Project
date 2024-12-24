import time
import json
import hmac
import hashlib
import requests
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Set the API Key and Secret from environment variables
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
BASE_URL = "https://api.pro.coinbase.com"  # Coinbase Pro API URL

def generate_signature(endpoint, body, timestamp):
    # Generate the signature for the request
    message = timestamp + 'POST' + endpoint + body
    signature = hmac.new(
        bytes(API_SECRET, 'utf-8'), 
        msg=bytes(message, 'utf-8'), 
        digestmod=hashlib.sha256
    ).hexdigest()
    return signature

def place_giga_buy_order(size):
    try:
        endpoint = "/orders"
        url = f"{BASE_URL}{endpoint}"
        timestamp = str(int(time.time()))

        # GIGA-USDC order payload
        body = {
            "product_id": "GIGA-USDC",
            "side": "buy",
            "price": "1.00",  # Price per GIGA in USDC
            "size": str(size),  # Amount of GIGA to buy
            "client_order_id": f"order-{timestamp}",  # Unique ID
            "type": "market"  # Ensure market order
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
        return {"error": f"Failed to place order: {str(e)}"}

if __name__ == "__main__":
    # Test placing a 1 USD order for GIGA
    response = place_giga_buy_order(1.00)
    print(response)
