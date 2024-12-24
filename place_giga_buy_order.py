import time
import json
import hmac
import hashlib
import requests

# Your Coinbase Pro API details
API_KEY = 'YOUR_API_KEY'
API_SECRET = 'YOUR_API_SECRET'
API_PASSPHRASE = 'YOUR_API_PASSPHRASE'
BASE_URL = 'https://api.pro.coinbase.com'

# Generate the signature for the request
def generate_signature(endpoint, body_json, timestamp):
    message = timestamp + 'POST' + endpoint + body_json
    return hmac.new(API_SECRET.encode(), message.encode(), hashlib.sha256).hexdigest()

def place_giga_buy_order(size):
    try:
        # API endpoint for placing an order
        endpoint = "/orders"
        url = f"{BASE_URL}{endpoint}"
        timestamp = str(int(time.time()))

        # GIGA-USDC order payload
        body = {
            "product_id": "GIGA-USDC",  # The trading pair
            "side": "buy",              # Buy order
            "order_configuration": {
                "market_market_ioc": {
                    "quote_size": size  # Trade size in USDC
                }
            },
            "client_order_id": f"order-{timestamp}"  # Unique ID for this order
        }
        body_json = json.dumps(body)

        # Generate signature
        signature = generate_signature(endpoint, body_json, timestamp)

        # API request headers
        headers = {
            "CB-ACCESS-KEY": API_KEY,
            "CB-ACCESS-SIGN": signature,
            "CB-ACCESS-TIMESTAMP": timestamp,
            "CB-ACCESS-PASSPHRASE": API_PASSPHRASE,
            "Content-Type": "application/json"
        }

        # Make the API request
        response = requests.post(url, headers=headers, data=body_json)

        # Print the response for debugging
        print("Response Status Code:", response.status_code)
        print("Response Body:", response.text)

        return response.json()

    except Exception as e:
        return {"error": f"Failed to place order: {str(e)}"}

# Example usage
place_giga_buy_order(1.00)  # Example order size of 1 USDC
