from coinbase_advanced_trader.enhanced_rest_client import EnhancedRESTClient
from flask import Flask, request
import uuid
import json
import os
from dotenv import load_dotenv
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Load API credentials from .env
load_dotenv()
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")

# Initialize the EnhancedRESTClient
client = EnhancedRESTClient(api_key=API_KEY, api_secret=API_SECRET)

# Define Flask app
app = Flask(__name__)

# Load supported pairs from pairs.json
with open("pairs.json", "r") as pairs_file:
    pairs_data = json.load(pairs_file)
    supported_pairs = pairs_data.get("pairs", [])

def validate_pair(pair):
    """Validate that the pair exists in the supported pairs list."""
    if pair not in supported_pairs:
        raise ValueError(f"Invalid trading pair: {pair}. Please choose a valid pair.")

def get_balance(currency):
    """Retrieve the available balance for a specific currency."""
    try:
        accounts = client.list_accounts()
        for account in accounts:
            if account["currency"] == currency:
                return float(account["available_balance"]["value"])
        return 0.0
    except Exception as e:
        logging.error(f"Error fetching balance for {currency}: {str(e)}")
        return 0.0

def execute_trade(action, product_id, percentage=None, flat_amount=None):
    """Execute a trade (buy or sell) based on action and parameters."""
    try:
        if action == "buy":
            if percentage:
                buy_crypto_percentage(product_id, percentage)
            elif flat_amount:
                buy_crypto_flat(product_id, flat_amount)
        elif action == "sell":
            if percentage:
                sell_crypto_percentage(product_id, percentage)
            elif flat_amount:
                sell_crypto_flat(product_id, flat_amount)
        else:
            raise ValueError("Invalid trade action.")
    except Exception as e:
        logging.error(f"Trade execution failed for {action} on {product_id}: {str(e)}")

def buy_crypto_percentage(product_id, percentage):
    """Execute a market buy order using a percentage of available funds."""
    base_currency = product_id.split('/')[1]
    balance = get_balance(base_currency)
    trade_size = round(balance * (percentage / 100), 2)
    if balance <= 0 or trade_size < 1:
        logging.warning("Insufficient balance or trade size too small!")
        return
    logging.info(f"Placing a buy order for {trade_size} of {product_id}...")
    client_order_id = str(uuid.uuid4())
    client.market_order_buy(product_id=product_id, quote_size=str(trade_size), client_order_id=client_order_id)

def buy_crypto_flat(product_id, flat_amount):
    """Execute a market buy order for a flat amount of the base currency."""
    logging.info(f"Placing a buy order for ${flat_amount} worth of {product_id}...")
    client_order_id = str(uuid.uuid4())
    client.market_order_buy(product_id=product_id, quote_size=str(flat_amount), client_order_id=client_order_id)

def sell_crypto_percentage(product_id, percentage):
    """Execute a market sell order using a percentage of the crypto balance."""
    base_currency = product_id.split('/')[0]
    balance = get_balance(base_currency)
    trade_size = round(balance * (percentage / 100), 8)
    if balance <= 0 or trade_size < 0.0001:
        logging.warning("Insufficient balance or trade size too small!")
        return
    logging.info(f"Placing a sell order for {trade_size} of {product_id}...")
    client_order_id = str(uuid.uuid4())
    client.market_order_sell(product_id=product_id, base_size=str(trade_size), client_order_id=client_order_id)

def sell_crypto_flat(product_id, flat_amount):
    """Execute a market sell order for a flat amount of the cryptocurrency."""
    logging.info(f"Placing a sell order for {flat_amount} of {product_id}...")
    client_order_id = str(uuid.uuid4())
    client.market_order_sell(product_id=product_id, base_size=str(flat_amount), client_order_id=client_order_id)

@app.route("/webhook", methods=["POST"])
def webhook():
    """Handle incoming webhook requests and trigger buy/sell actions."""
    try:
        data = request.get_json()
        with open("parameters.json", "r") as param_file:
            params = json.load(param_file)

        coin = params.get("coin", "BTC").upper()
        pair = params.get("pair", "USDC").upper()
        product_id = f"{coin}/{pair}"

        mode = params.get("mode", "%")
        buy_percentage = params.get("buy_%", 0)
        sell_percentage = params.get("sell_%", 0)
        buy_flat = params.get("buy_$", 0)
        sell_flat = params.get("sell_$", 0)

        validate_pair(product_id)

        action = data.get("action", "").lower()
        if action == "buy":
            execute_trade("buy", product_id, percentage=buy_percentage if mode == "%" else None, flat_amount=buy_flat if mode == "$" else None)
        elif action == "sell":
            execute_trade("sell", product_id, percentage=sell_percentage if mode == "%" else None, flat_amount=sell_flat if mode == "$" else None)
        else:
            return "Invalid action.", 400

        return f"{action.capitalize()} order executed!", 200
    except Exception as e:
        logging.error(f"Webhook processing failed: {str(e)}")
        return f"Error: {str(e)}", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
