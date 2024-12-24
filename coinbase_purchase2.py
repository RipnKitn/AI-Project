import requests
import json
import time

# Coinbase API Credentials
API_KEY = 'your-api-key'
API_SECRET = 'your-api-secret'
API_URL = 'https://api.coinbase.com/v2/accounts'  # Modify if using Coinbase Pro

# Headers for the API request
headers = {
    'Authorization': f'Bearer {API_KEY}',
    'Content-Type': 'application/json'
}

# Example of making a purchase (buy $1 worth of GIGA with USDC)
def make_purchase():
    # Define the trading pair and the amount to buy
    data = {
        "amount": "1",  # Adjust amount for the purchase
        "currency": "USDC",
        "product_id": "GIGA-USDC",  # Ensure this is the correct trading pair
    }
    
    # Send a buy request
    response = requests.post(f'{API_URL}/buys', headers=headers, json=data)

    # Check the response
    if response.status_code == 200:
        print("Purchase successful!")
        print(response.json())  # Prints purchase details
    else:
        print("Failed to make purchase")
        print(response.json())

# Call the function to make the purchase
make_purchase()
