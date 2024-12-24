import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import coinbase
from coinbase.wallet.client import Client
import time

# Load environment variables from .env
load_dotenv()

# Set up Flask
app = Flask(__name__)

# Retrieve your API key and secret from .env
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")

# Set up Coinbase client
client = Client(API_KEY, API_SECRET)

# Helper function to fetch balance
def fetch_balance(currency):
    try:
        accounts = client.get_accounts()
        for account in accounts.data:
            if account['currency'] == currency:
                return float(account['balance']['amount'])
        return 0.0
    except Exception as e:
        print(f"Error fetching balance: {e}")
        return 0.0

# Place a buy/sell order
def place_trade(symbol, side, amount):
    try:
        if side == 'buy':
            client.buy(account_id='primary', amount=str(amount), currency='USD')
        elif side == 'sell':
            client.sell(account_id='primary', amount=str(amount), currency='USD')
        print(f"Trade placed: {side} {amount} of {symbol}")
    except Exception as e:
        print(f"Error placing trade: {e}")

# Webhook to handle TradingView alerts
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    symbol = data.get("symbol")
    side = data.get("side")
    amount = data.get("amount")
    
    # Check if we have valid values
    if symbol and side and amount:
        # Fetch available balance
        balance = fetch_balance("USD")
        
        # Ensure sufficient balance for trade
        if balance >= amount:
            # Place trade if conditions are met
            place_trade(symbol, side, amount)
            return jsonify({"status": "success", "message": f"Trade executed: {side} {amount} {symbol}"}), 200
        else:
            return jsonify({"status": "error", "message": "Insufficient balance for trade"}), 400
    else:
        return jsonify({"status": "error", "message": "Invalid data received"}), 400

if __name__ == "__main__":
    app.run(debug=True, port=80)
