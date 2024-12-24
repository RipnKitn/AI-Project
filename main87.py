from flask import Flask, request
from coinbase_advanced_trader.enhanced_rest_client import EnhancedRESTClient
import json
import uuid
import os
from dotenv import load_dotenv

# Load API credentials from .env
load_dotenv()
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")

# Initialize the EnhancedRESTClient
client = EnhancedRESTClient(api_key=API_KEY, api_secret=API_SECRET)

# Define Flask app
app = Flask(__name__)

# Load supported pairs from pairs.json
with open('pairs.json', 'r') as pairs_file:
    pairs_data = json.load(pairs_file)
    supported_pairs = pairs_data.get("pairs", [])

def validate_pair(pair):
    if pair not in supported_pairs:
        raise ValueError(f"Invalid trading pair: {pair}. Please choose a valid pair.")

def get_balance(currency):
    try:
        accounts = client.list_accounts()
        for account in accounts:
            if account["currency"] == currency:
                return float(account["available_balance"]["value"])
        return 0.0
    except Exception as e:
        print(f"Error fetching balance for {currency}: {str(e)}")
        return 0.0

def buy_crypto_percentage(product_id, percentage):
    try:
        base_currency = product_id.split('/')[1]
        balance = get_balance(base_currency)
        if balance <= 0:
            print(f"Insufficient {base_currency} balance!")
            return

        trade_size = round(balance * (percentage / 100), 2)
        if trade_size < 1:
            print("Trade size too small!")
            return

        print(f"Placing a buy order for {trade_size} of {product_id}...")
        client_order_id = str(uuid.uuid4())
        response = client.market_order_buy(
            product_id=product_id,
            quote_size=str(trade_size),
            client_order_id=client_order_id
        )
        print("Buy order placed:", response)
    except Exception as e:
        print("Buy order failed:", str(e))

def sell_crypto_percentage(product_id, percentage):
    try:
        base_currency = product_id.split('/')[0]
        balance = get_balance(base_currency)
        if balance <= 0:
            print(f"Insufficient {base_currency} balance!")
            return

        trade_size = round(balance * (percentage / 100), 8)
        if trade_size < 0.0001:
            print("Trade size too small!")
            return

        print(f"Placing a sell order for {trade_size} of {product_id}...")
        client_order_id = str(uuid.uuid4())
        response = client.market_order_sell(
            product_id=product_id,
            base_size=str(trade_size),
            client_order_id=client_order_id
        )
        print("Sell order placed:", response)
    except Exception as e:
        print("Sell order failed:", str(e))

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.get_json()

        # Extract action from alert
        action = data.get("action", "").lower()

        # Load trading parameters from parameters.json
        with open('parameters.json', 'r') as param_file:
            params = json.load(param_file)

        coin = params.get("coin", "BTC").upper()
        pair = params.get("pair", "USDC").upper()
        product_id = f"{coin}/{pair}"

        mode = params.get("mode", "%")
        buy_percentage = params.get("buy_%", 0)
        sell_percentage = params.get("sell_%", 0)

        # Validate the trading pair
        try:
            validate_pair(product_id)
        except ValueError as e:
            return str(e), 400

        # Handle actions
        if action == "buy" and mode == "%":
            buy_crypto_percentage(product_id, buy_percentage)
        elif action == "sell" and mode == "%":
            sell_crypto_percentage(product_id, sell_percentage)
        else:
            return "Invalid action or mode specified.", 400

        return f"{action.capitalize()} order executed!", 200
    except Exception as e:
        return f"Error processing webhook: {str(e)}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
