import requests

# Webhook URL for your Flask app
url = "http://127.0.0.1:8080/webhook"

# Headers for JSON content
headers = {
    "Content-Type": "application/json"
}

# Payload with USDC trading pair
payload = {
    "symbol": "USDC-USD",  # Use USDC-USD as the trading pair
    "side": "buy",         # Action: "buy" or "sell"
    "percentage": 10       # Test percentage for the trade
}

# Send the POST request to the Flask app
response = requests.post(url, json=payload, headers=headers)

# Print response for debugging
print("Response Status:", response.status_code)
print("Response Body:", response.json())
