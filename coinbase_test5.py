import requests

# Coinbase API credentials (Directly included)
API_KEY = "7e23b2c4-f91d-47db-bc56-35775be759aa"
COINBASE_API_URL = "https://api.coinbase.com/v2/accounts"

# Headers for authentication
headers = {"Authorization": f"Bearer {API_KEY}"}

# Test connection by retrieving account information
response = requests.get(COINBASE_API_URL, headers=headers)

if response.status_code == 200:
    print("Success! Here is your account info:")
    print(response.json())
else:
    print("Failed to connect. Error:")
    print(response.json())
