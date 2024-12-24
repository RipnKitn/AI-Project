import time
import hmac
import hashlib
import base64
import requests

# Replace these values with your API key and secret
API_KEY = "ac613607-d810-41d4-9196-48c14ab0f8d0"
API_SECRET = """-----BEGIN EC PRIVATE KEY-----
MHcCAQEEID8afQ5/asXPaRoupSmKxu71KzAAs5xjGsvQ3HoF2xdUoAoGCCqGSM49
AwEHoUQDQgAEUjZHnfp6pU4hFnf6SEm89Q8SiIF9aAldefKNdKrHbpzTIpe8uROG
1vcvhdnAFC7IA5otSktGGAje1XPWj2hcLg==
-----END EC PRIVATE KEY-----"""
BASE_URL = "https://api.coinbase.com/api/v3/brokerage"

# Generate a signature for Coinbase API requests
def generate_signature(request_path, body, timestamp, method):
    message = f"{timestamp}{method}{request_path}{body or ''}"
    hmac_key = base64.b64decode(API_SECRET)
    signature = hmac.new(hmac_key, message.encode(), hashlib.sha256)
    return base64.b64encode(signature.digest()).decode()

# Test the /accounts endpoint
def test_accounts():
    endpoint = "/accounts"
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

    # Send request to Coinbase
    try:
        response = requests.get(url, headers=headers)
        print(f"Response Status: {response.status_code}")
        print(f"Response Body: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

# Run the test
if __name__ == "__main__":
    test_accounts()
