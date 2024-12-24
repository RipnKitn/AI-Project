import os
import cbpro
from flask import Flask, request
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Get API keys from .env
API_KEY = os.getenv("COINBASE_API_KEY")
API_SECRET = os.getenv("COINBASE_API_SECRET")
API_PASSPHRASE = os.getenv("COINBASE_PASSPHRASE")

# Coinbase Pro client setup
client = cbpro.AuthenticatedClient(API_KEY, API_SECRET, API_PASSPHRASE)

@app.route('/')
def home():
    return 'Flask app is running!'

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    print(f"Received data: {data}")

    # Example: Place a market order
    if data.get('action') == 'buy':
        place_order(data)

    return 'Webhook received!', 200

def place_order(data):
    # Example market order (buy)
    symbol = data['symbol']
    price = data['price']
    amount = data['amount']
    order_type = data['order_type']

    try:
        if order_type == 'market':
            print(f"Placing a {order_type} order for {amount} of {symbol} at price {price}")
            order = client.place_market_order(
                product_id=symbol,  # e.g., 'BTC-USD'
                side='buy',  # Or 'sell' depending on action
                funds=amount  # Use funds instead of quantity if it's a market order
            )
            print(f"Order placed: {order}")
    except Exception as e:
        print(f"Error placing order: {e}")

if __name__ == '__main__':
    app.run(debug=True)
