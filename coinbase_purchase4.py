import requests
import os
import time
import hmac
import hashlib
import json
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')

def generate_signature(secret, timestamp, method, request_path, body=""):
    message = f"{timestamp}{method}{request_path}{body}".encode()
    secret = secret.encode()
    return hmac.new(secret, message, hashlib.sha256).hexdigest()

url = "https://api.coinbase.com/v2/orders"
headers = {
    "CB-ACCESS-KEY": API_KEY,
    "CB-ACCESS-SIGN": "",
    "CB-ACCESS-TIMESTAMP": str(int(time.time())),
    "Content-Type": "application/json"
}

order_data = {
    "product_id": "GIGA-USDC",
    "side": "buy",
    "size": 1,
    "price": 0.04643,
    "order_type": "market"
}

timestamp = str(int(time.time()))
signature = generate_signature(API_SECRET, timestamp, "POST", "/v2/orders", json.dumps(order_data))
headers["CB-ACCESS-SIGN"] = signature

response = requests.post(url, headers=headers, json=order_data)
print("Status Code:", response.status_code)
print("Response:", response.json())
