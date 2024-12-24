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

# Generate API signature
def generate_signature(request_path, body, timestamp, method):
    message = f"{timestamp}{method}{request_path}{body or ''}"
    hmac_key = base64.b64decode(API_SECRET)
    signature = hmac.new(hmac_key, message.encode(), hashlib.sha256)
    return base64.b64encode(signature.digest()).decode()

# Function to test a simple buy order
def place_buy_order():
    endpoint = "/orders"
    url = f"{BASE_URL}{endpoint}"
    timestamp = str(int(time.time()))

    # Order payload
    body = {
        "product_id": "GIGA-USDC",
        "side": "buy",
        "order_type": "market",
        "size": "1"
    }
    body_json = json.dumps(body)

    # Generate signature
    signature = generate_signature(endpoint, body_json, timestamp, "POST")

    # Prepare headers
    headers = {
        "CB-ACCESS-KEY": API_KEY,
        "CB-ACCESS-SIGN": signature,
        "CB-ACCESS-TIMESTAMP": timestamp,
        "Content-Type": "application/json"
    }

    # Send the request
    response = requests.post(url, headers=headers, data=body_json)
    print(f"Status Code: {response.status_code}")
    print(f"Response Body: {response.json()}")

if __name__ == "__main__":
    place_buy_order()
