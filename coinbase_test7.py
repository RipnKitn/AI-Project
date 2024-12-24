import time
import hmac
import hashlib
import requests

# Coinbase API credentials
API_KEY = "7e23b2c4-f91d-47db-bc56-35775be759aa"  # Your API Key
API_SECRET = """-----BEGIN EC PRIVATE KEY-----
MHcCAQEEIEajBK7ysPzoNM3v79sYdyzcaN9VH9eWi7PUeZF1k5CdoAoGCCqGSM49
AwEHoUQDQgAEo8k64SDokeG8dlwpuyTCJau0AhxAWfh/hML9UEdrEAxmD5WEYp+B
O89GXmvpw598CtdSSZmp02IQyMp3cOa5YA==
-----END EC PRIVATE KEY-----"""  # Your Exact API Secret
COINBASE_API_URL = "https://api.coinbase.com/api/v3/brokerage/orders"

# Generate HMAC signature for authentication
def generate_signature(secret, timestamp, method, request_path, body=""):
    message = f"{timestamp}{method}{request_path}{body}".encode()
    secret = secret.encode()
    return hmac.new(secret, message, hashlib.sha256).hexdigest()

# Prepare API request details
timestamp = str(int(time.time()))
method = "POST"
request_path = "/api/v3/brokerage/orders"
order_data = {
    "product_id": "GIGA-USDC",  # GIGA/USDC trading pair
    "side": "BUY",  # BUY or SELL
    "order_configuration": {
        "market_market_ioc": {
            "quote_size": "1.00"  # $1 worth of GIGA
        }
    },
    "client_order_id": f"order-{int(time.time())}"  # Unique order ID
}

# Body as JSON string (ensure correct format)
body = str(order_data).replace("'", '"')

# Generate signature
signature = generate_signature(API_SECRET, timestamp, method, request_path, body)

# Prepare headers
headers = {
    "CB-ACCESS-KEY": API_KEY,
    "CB-ACCESS-SIGN": signature,
    "CB-ACCESS-TIMESTAMP": timestamp,
    "Content-Type": "application/json"
}

# Make the API request to place the order
response = requests.post(COINBASE_API_URL, json=order_data, headers=headers)

# Print response status and data
print("Status Code:", response.status_code)
print("Response:", response.text)
