from coinbase_advanced_trader.enhanced_rest_client import EnhancedRESTClient
from flask import Flask, request
import uuid
import json
from dotenv import load_dotenv
import os
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
with open('pairs.json', 'r') as pairs_file:
    pairs_data = json.load(pairs_file)
    supported_pairs = pairs_data.get("pairs", [])

def validate_pair(pair):
    """Validate that the pair exists in the supported pairs list."""
    if pair not in supported_pairs:
        logging.error(f"Invalid trading pair: {pair}. Supported pairs: {supported_pairs}")
        raise ValueError(f"Invalid trading pair: {pair}. Please choose a valid pair.")
    logging.info(f"Validated trading pair: {pair}")

def get_balance(currency):
    """Retrieve the available balance for a specific currency."""
    try:
        accounts = client.get_accounts()
        for account in accounts:
            if account["currency"] == currency:
                return float(account["available_balance"]["value"])
        return 0.0
    except Exception as e:
        logging.error(f"Error fetching balance for {currency}: {str(e)}")
        return 0.0

def buy_crypto_flat(product_id, flat_amount):
    """Execute a market buy order for a flat amount of the base currency."""
    try:
        logging.info(f"Placing a buy order for ${flat_amount} worth of {product_id}...")
        client_order_id = str(uuid.uuid4())
        response = client.market_order_buy(
            product_id=product_id,
            quote_size=str(flat_amount),
            client_order_id=client_order_id
        )
        logging.info("Buy order API response: %s", response)
    except Exception as e:
        logging.error("Buy order failed: %s", str(e))

def sell_crypto_flat(product_id, flat_amount):
    """Execute a market sell order for a flat amount of the cryptocurrency."""
    try:
        logging.info(f"Placing a sell order for {flat_amount} of {product_id}...")
        client_order_id = str(uuid.uuid4())
        response = client.market_order_sell(
            product_id=product_id,
            base_size=str(flat_amount),
            client_order_id=client_order_id
        )
        logging.info("Sell order API response: %s", response)
    except Exception as e:
        logging.error("Sell order failed: %s", str(e))

@app.route('/webhook', methods=['POST'])
def webhook():
    """Handle incoming webhook requests and trigger buy/sell actions."""
    try:
        data = request.get_json()

        # Load trading parameters from parameters.json
        with open('parameters.json', 'r') as param_file:
            params = json.load(param_file)

        coin = params.get("coin", "BTC").upper()
        pair = params.get("pair", "USDC").upper()
        product_id = f"{coin}-{pair}"  # Use '-' instead of '/'

        # Validate the trading pair
        validate_pair(product_id)

        mode = params.get("mode", "$")  # Default to flat mode
        buy_flat = params.get("buy_$", 0)
        sell_flat = params.get("sell_$", 0)

        # Determine the action
        action = data.get("action", "").lower()

        if action == "buy":
            buy_crypto_flat(product_id, buy_flat)
            return "Buy order executed!", 200

        elif action == "sell":
            sell_crypto_flat(product_id, sell_flat)
            return "Sell order executed!", 200

        else:
            return "Invalid action", 400

    except Exception as e:
        logging.error(f"Webhook processing failed: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
