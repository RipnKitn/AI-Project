import time
import json
import requests
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Coinbase API Credentials from .env file
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
BASE_URL = os.getenv("BASE_URL")

# Helper to generate the Coinbase API signature (you'll need to implement the signature generation)
def generate_signature(endpoint, body, timestamp):
    message = timestamp + "POST" + endpoint + body
    return "GENERATED_SIGNATURE"  # Placeholder for actual signature logic

# Place buy order for GIGA-USDC
def place_giga_buy_order(size):
    try:
        endpoint = "/orders"
        url = f"{BASE_URL}{endpoint}"
        timestamp = str(int(time.time()))

        # Payload with size from webhook
        body = {
            "product_id": "GIGA-USDC",
            "side": "buy", 
            "order_configuration": {
                "market_market_ioc": {
                    "quote_size": size  # Trade size in USDC
                }
            },
            "client_order_id": f"order-{timestamp}"  # Unique client order ID
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

# Main entry point to make a trade of size $1
if __name__ == "__main__":
    size = "1.00"  # Set the size to 1.00 for $1 GIGA-USDC purchase
    result = place_giga_buy_order(size)
    print(result)
