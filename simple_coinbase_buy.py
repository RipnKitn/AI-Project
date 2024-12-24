import time
import hmac
import hashlib
import base64
import requests
import json

# Hardcoded API Key and Secret
API_KEY = "organizations/1073f4e6-52f3-49e4-b7e4-e2bd34261c51/apiKeys/7e23b2c4-f91d-47db-bc56-35775be759aa"
API_SECRET = """-----BEGIN EC PRIVATE KEY-----
MHcCAQEEIEajBK7ysPzoNM3v79sYdyzcaN9VH9eWi7PUeZF1k5CdoAoGCCqGSM49
AwEHoUQDQgAEo8k64SDokeG8dlwpuyTCJau0AhxAWfh/hML9UEdrEAxmD5WEYp+B
O89GXmvpw598CtdSSZmp02IQyMp3cOa5YA==
-----END EC PRIVATE KEY-----
"""
BASE_URL = "https://api.coinbase.com/api/v3/brokerage"

# Function to generate signature
def generate_signature(endpoint, body, timestamp):
    message = f"{timestamp}POST{endpoint}{body}"
    hmac_key = base64.b64decode(API_SECRET)
    signature = hmac.new(hmac_key, message.encode('utf-8'), hashlib.sha256)
    return base64.b64encode(signature.digest()).decode()

# Place a $1 GIGA-USDC buy order
def place_buy_order():
    endpoint = "/orders"
    url = f"{BASE_URL}{endpoint}"
    timestamp = str(int(time.time()))

    # Payload for the order
    body = {
        "product_id": "GIGA-USDC",
        "side": "buy",
        "order_type": "market",
        "size": "1"  # $1 worth of GIGA
    }
    body_json = json.dumps(body)

    # Create headers
    headers = {
        "CB-ACCESS-KEY": API_KEY,
        "CB-ACCESS-SIGN": generate_signature(endpoint, body_json, timestamp),
        "CB-ACCESS-TIMESTAMP": timestamp,
        "Content-Type": "application/json"
    }

    # Send POST request to Coinbase API
    response = requests.post(url, headers=headers, data=body_json)

    # Print response
    print(f"Status Code: {response.status_code}")
    try:
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error decoding response: {e}")
        print(f"Raw Response: {response.text}")

if __name__ == "__main__":
    place_buy_order()
