from coinbase_advanced_trader.enhanced_rest_client import EnhancedRESTClient
from flask import Flask, request
import uuid
import json

# Load API credentials from .env
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")

# Initialize the EnhancedRESTClient
client = EnhancedRESTClient(api_key=API_KEY, api_secret=API_SECRET)

# Define Flask app
app = Flask(__name__)

# Endpoint for webhook
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()

    # Load trading parameters from parameters.json
    with open('parameters.json', 'r') as param_file:
        params = json.load(param_file)

    pair = params.get("pair", "BTC/USDC")
    buy_percentage = params.get("buy_percentage", 90)
    sell_percentage = params.get("sell_percentage", 80)

    # Determine action
    action = data.get("action", "").lower()

    if action == "buy":
        buy_crypto(pair, buy_percentage)
        return "Buy order triggered!", 200
    elif action == "sell":
        sell_crypto(pair, sell_percentage)
        return "Sell order triggered!", 200
    else:
        return "Invalid action", 400

def buy_crypto(pair, percentage):
    """
    Execute a market buy order for the given pair using a percentage of available funds.
    """
    try:
        base_currency = pair.split('/')[1]
        balance = get_balance(base_currency)
        if balance <= 0:
            print(f"Insufficient {base_currency} balance!")
            return

        trade_size = round(balance * (percentage / 100), 2)
        if trade_size < 1:
            print("Trade size too small!")
            return

        print(f"Placing a buy order for {trade_size} of {pair}...")
        client_order_id = str(uuid.uuid4())
        response = client.market_order_buy(
            product_id=pair,
            quote_size=str(trade_size),
            client_order_id=client_order_id
        )
        print("Buy order placed:", response)
    except Exception as e:
        print("Buy order failed:", str(e))

def sell_crypto(pair, percentage):
    """
    Execute a market sell order for the given pair using a percentage of the crypto balance.
    """
    try:
        base_currency = pair.split('/')[0]
        balance = get_balance(base_currency)
        if balance <= 0:
            print(f"Insufficient {base_currency} balance!")
            return

        trade_size = round(balance * (percentage / 100), 8)
        if trade_size < 0.0001:
            print("Trade size too small!")
            return

        print(f"Placing a sell order for {trade_size} of {pair}...")
        client_order_id = str(uuid.uuid4())
        response = client.market_order_sell(
            product_id=pair,
            base_size=str(trade_size),
            client_order_id=client_order_id
        )
        print("Sell order placed:", response)
    except Exception as e:
        print("Sell order failed:", str(e))

def get_balance(currency):
    """
    Retrieve the available balance for a specific currency.
    """
    try:
        accounts = client.list_accounts()
        for account in accounts:
            if account["currency"] == currency:
                return float(account["available_balance"]["value"])
        return 0.0
    except Exception as e:
        print(f"Error fetching balance for {currency}:", str(e))
        return 0.0

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
