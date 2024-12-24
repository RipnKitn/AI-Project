import time
import hmac
import hashlib
import base64
import requests

# Replace these values with your current API key and secret
API_KEY = "ac613607-d810-41d4-9196-48c14ab0f8d0"  # Replace with your actual key
API_SECRET = """-----BEGIN EC PRIVATE KEY-----
MHcCAQEEIEajBK7ysPzoNM3v79sYdyzcaN9VH9eWi7PUeZF1k5CdoAoGCCqGSM49
AwEHoUQDQgAEo8k64SDokeG8dlwpuyTCJau0AhxAWfh/hML9UEdrEAxmD5WEYp+B
O89GXmvpw598CtdSSZmp02IQyMp3cOa5YA==
-----END EC PRIVATE KEY-----"""
BASE_URL = "https://api.coinbase.com/api/v3/brokerage"

# Generate a signature for Coinbase API requests
def generate_signature(request_path, body, timestamp, method):
    message = f"{timestamp}{method}{request_path}{body or ''}"
    print(f"Message for Signature: {message}")  # Debugging the message
    hmac_key = base64.b64decode(API_SECRET)
    signature = hmac.new(hmac_key, message.encode(), hashlib.sha256)
    generated_signature = base64.b64encode(signature.digest()).decode()
    print(f"Generated Signature: {generated_signature}")  # Debugging the signature
    return generated_signature

# Test the /products endpoint
def test_products():
    endpoint = "/products"
    url = f"{BASE_URL}{endpoint}"
    timestamp = str(int(time.time()))

    # Generate signature
    signature = generate_signature(endpoint, "", timestamp, "GET")

    # Prepare headers
    headers = {
        "CB-ACCESS-KEY": API_KEY,
        "CB-ACCESS-SIGN": signature,
        "CB-ACCESS-TIMESTAMP": timestamp,
        "Content-Type": "application/json"
    }

    # Debugging output
    print(f"Request URL: {url}")
    print(f"Request Headers: {headers}")
    print(f"Timestamp Sent: {timestamp}")  # Debugging the timestamp

    # Send request to Coinbase
    try:
        response = requests.get(url, headers=headers)
        print(f"Response Status: {response.status_code}")
        print(f"Response Body: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

# Run the test
if __name__ == "__main__":
    test_products()
