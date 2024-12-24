import requests
import time
import hmac
import hashlib
import json

# Coinbase API credentials
API_KEY = '7e23b2c4-f91d-47db-bc56-35775be759aa'  # Replace this with your actual API key
API_SECRET = '-----BEGIN EC PRIVATE KEY-----\nMHcCAQEEIEajBK7ysPzoNM3v79sYdyzcaN9VH9eWi7PUeZF1k5CdoAoGCCqGSM49\nAwEHoUQDQgAEo8k64SDokeG8dlwpuyTCJau0AhxAWfh/hML9UEdrEAxmD5WEYp+B\nO89GXmvpw598CtdSSZmp02IQyMp3cOa5YA==\n-----END EC PRIVATE KEY-----\n'  # Replace this with your actual secret key
API_PASSPHRASE = ''  # Optional, if you have it

# Coinbase API endpoint and headers
url = "https://api.coinbase.com/v2/orders"
headers = {
    "CB-ACCESS-KEY": API_KEY,
    "CB-ACCESS-SIGN": "",  # Will be generated below
    "CB-ACCESS-TIMESTAMP": str(int(time.time())),
    "CB-ACCESS-PASSPHRASE": API_PASSPHRASE,
    "Content-Type": "application/json"
}

# Function to generate HMAC signature
def generate_signature(secret, timestamp, method, request_path, body=""):
    message = f"{timestamp}{method}{request_path}{body}".encode()
    secret = secret.encode()
    return hmac.new(secret, message, hashlib.sha256).hexdigest()

# Prepare purchase data
order_data = {
    "product_id": "GIGA-USDC",  # Ensure this is the correct pair you want to buy
    "side": "buy",  # We are buying
    "size": 1,  # Amount to purchase
    "price": 0.04643,  # Example price, adjust this based on current price
    "order_type": "market"  # A market order will execute immediately at the best available price
}

# Generate signature for the API request
timestamp = str(int(time.time()))
signature = generate_signature(API_SECRET, timestamp, "POST", "/v2/orders", json.dumps(order_data))

# Add the signature to the headers
headers["CB-ACCESS-SIGN"] = signature

# Make the API request to place the buy order
response = requests.post(url, headers=headers, json=order_data)

# Print the response status and content
print("Status Code:", response.status_code)
print("Response:", response.json())
