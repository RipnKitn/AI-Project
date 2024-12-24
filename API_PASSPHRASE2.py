import requests
import hmac
import hashlib
import time
import json
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')

url = "https://api.coinbase.com/v2/orders"
headers = {
    "CB-ACCESS-KEY": API_KEY,
    "CB-ACCESS-SIGN": "",
    "CB-ACCESS-TIMESTAMP": str(int(time.time())),
    "Content-Type": "application/json"
}

def generate_signature(secret, timestamp, method, request_path, body=""):
    """Generate the HMAC signature for Coinbase API request"""
    message = f"{timestamp}{method}{request_path}{body}".encode()
    secret = secret.encode()
    return hmac.new(secret, message, hashlib.sha256).hexdigest()

# Prepare the order data for purchase (example)
order_data = {
    "product_id": "GIGA-USDC",  # Replace with correct product pair
    "side": "buy",  # Buying
    "size": 1,  # Amount to purchase
    "price": 0.04643,  # Example price (adjust as needed)
    "order_type": "market"  # Market order
}

# Generate the signature
timestamp = str(int(time.time()))
signature = generate_signature(API_SECRET, timestamp, "POST", "/v2/orders", json.dumps(order_data))

headers["CB-ACCESS-SIGN"] = signature

# Make the API request to buy
response = requests.post(url, headers=headers, json=order_data)

# Print the response
print("Status Code:", response.status_code)
print("Response:", response.json())
