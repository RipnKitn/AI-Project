import requests

# Coinbase API credentials
API_KEY = "7e23b2c4-f91d-47db-bc56-35775be759aa"
COINBASE_API_URL = "https://api.coinbase.com/api/v3/brokerage/orders"

# Headers for authentication
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# Define the order details
order_data = {
    "product_id": "BTC-USD",  # Change to your desired trading pair
    "side": "BUY",           # BUY or SELL
    "order_configuration": {
        "market_market_ioc": {
            "quote_size": "10.00"  # Amount in USD to buy
        }
    },
    "client_order_id": "test_order_001"  # Unique identifier for the order
}

# Send the request to place an order
response = requests.post(COINBASE_API_URL, json=order_data, headers=headers)

# Output the response
print("Status Code:", response.status_code)
print("Response:", response.json())
