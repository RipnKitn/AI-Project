import os
from flask import Flask, request, jsonify
from coinbase.wallet.client import Client
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)

# Coinbase API setup
API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')
client = Client(API_KEY, API_SECRET)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()  # Get JSON data from the POST request
    if data:
        symbol = data.get('symbol')
        price = data.get('price')
        action = data.get('action')
        amount = data.get('amount')

        print(f"Received data: Symbol: {symbol}, Price: {price}, Action: {action}, Amount: {amount}")
        
        # Process the data here (buy/sell logic)
        if action == 'buy':
            # Example buy logic: Adjust as needed
            place_buy_order(symbol, price, amount)
        elif action == 'sell':
            # Example sell logic: Adjust as needed
            place_sell_order(symbol, price, amount)

        return jsonify({"message": "Success", "status": "200"}), 200
    return jsonify({"message": "Bad Request", "status": "400"}), 400


def place_buy_order(symbol, price, amount):
    """Place a buy order on Coinbase."""
    try:
        # Assuming 'symbol' corresponds to a Coinbase market pair like 'BTC-USD'
        order = client.buy(
            'BTC-USD',  # Adjust this according to the symbol you need
            amount=amount,  # Amount to buy
            currency="USD",  # Adjust the currency if necessary
            payment_method="your_payment_method_id"  # Provide the payment method ID
        )
        print(f"Buy order placed: {order}")
    except Exception as e:
        print(f"Error placing buy order: {e}")


def place_sell_order(symbol, price, amount):
    """Place a sell order on Coinbase."""
    try:
        # Assuming 'symbol' corresponds to a Coinbase market pair like 'BTC-USD'
        order = client.sell(
            'BTC-USD',  # Adjust this according to the symbol you need
            amount=amount,  # Amount to sell
            currency="USD",  # Adjust the currency if necessary
        )
        print(f"Sell order placed: {order}")
    except Exception as e:
        print(f"Error placing sell order: {e}")


if __name__ == "__main__":
    app.run(debug=True)
