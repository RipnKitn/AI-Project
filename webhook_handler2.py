from flask import Flask, request
import requests

app = Flask(__name__)

# Coinbase API credentials
API_KEY = "7e23b2c4-f91d-47db-bc56-35775be759aa"
API_SECRET = "MHcCAQEEIEajBK7ysPzoNM3v79sYdyzcaN9VH9eWi7PUeZF1k5CdoAoGCCqGSM49AwEHoUQDQgAEo8k64SDokeG8dlwpuyTCJau0AhxAWfh/hML9UEdrEAxmD5WEYp+BO89GXmvpw598CtdSSZmp02IQyMp3cOa5YA=="
COINBASE_API_URL = "https://api.coinbase.com/api/v3/brokerage/orders"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    print("Received alert:", data)

    # Example: Buy GIGA with USDC
    order_data = {
        "product_id": "GIGA-USDC",
        "side": "BUY",
        "order_configuration": {
            "market_market_ioc": {
                "quote_size": "1.00"  # $1 worth
            }
        },
        "client_order_id": "unique_id_123"
    }

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.post(COINBASE_API_URL, json=order_data, headers=headers)
    print("Coinbase Response:", response.status_code, response.text)

    return 'Webhook received', 200

if __name__ == '__main__':
    app.run(port=5000)
