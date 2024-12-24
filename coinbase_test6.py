import time
import hmac
import hashlib
import requests

# Coinbase API credentials
API_KEY = "7e23b2c4-f91d-47db-bc56-35775be759aa"
API_SECRET = "MHcCAQEEIEajBK7ysPzoNM3v79sYdyzcaN9VH9eWi7PUeZF1k5CdoAoGCCqGSM49AwEHoUQDQgAEo8k64SDokeG8dlwpuyTCJau0AhxAWfh/hML9UEdrEAxmD5WEYp+BO89GXmvpw598CtdSSZmp02IQyMp3cOa5YA=="
COINBASE_API_URL = "https://api.coinbase.com/api/v3/brokerage/accounts"

# Generate HMAC signature
def generate_signature(secret, timestamp, method, request_path, body=""):
    message = f"{timestamp}{method}{request_path}{body}".encode()
    secret = secret.encode()
    return hmac.new(secret, message, hashlib.sha256).hexdigest()

timestamp = str(int(time.time()))
method = "GET"
request_path = "/api/v3/brokerage/accounts"
signature = generate_signature(API_SECRET, timestamp, method, request_path)

headers = {
    "CB-ACCESS-KEY": API_KEY,
    "CB-ACCESS-SIGN": signature,
    "CB-ACCESS-TIMESTAMP": timestamp,
    "Content-Type": "application/json"
}

response = requests.get(COINBASE_API_URL, headers=headers)

print("Status Code:", response.status_code)
print("Response:", response.text)
