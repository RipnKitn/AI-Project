import time
import hmac
import hashlib
import base64
import requests

# Replace with your API key and secret
API_KEY = "your_new_api_key"
API_SECRET = """-----BEGIN EC PRIVATE KEY-----
your_new_api_secret
-----END EC PRIVATE KEY-----"""
BASE_URL = "https://api.coinbase.com/api/v3/brokerage"

def generate_signature(request_path, body, timestamp, method):
    message = f"{timestamp}{method}{request_path}{body or ''}"
    hmac_key = base64.b64decode(API_SECRET)
    signature = hmac.new(hmac_key, message.encode(), hashlib.sha256)
    return base64.b64encode(signature.digest()).decode()

def place_buy_order():
    endpoint = "/orders"
    url = f"{BASE_URL}{endpoint}"
    timestamp = str(int(time.time()))

    # Order details
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

    # Send POST request to Coinbase
    try:
        response = requests.post(url, headers=headers, data=body_json)
        print(f"Request URL: {url}")
        print(f"Request Headers: {headers}")
        print(f"Request Body: {body_json}")
        print(f"Response Status: {response.status_code}")
        print(f"Response Body: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    place_buy_order()
