from coinbase_advanced_trader.enhanced_rest_client import EnhancedRESTClient
from flask import Flask, request, jsonify
import uuid
import json
import logging
import os
from dotenv import load_dotenv

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Load environment variables from .env file
load_dotenv()

# Retrieve API key and secret from environment variables
api_key = os.getenv("API_KEY")
api_secret = os.getenv("API_SECRET")

# Initialize the EnhancedRESTClient
client = EnhancedRESTClient(api_key=api_key, api_secret=api_secret)

# Define Flask app
app = Flask(__name__)

# Function to validate if the pair exists in your supported pairs
def validate_pair(pair):
    """Validate that the pair exists in the supported pairs list."""
    supported_pairs = [
        "GIGA-USDC", "BTC-USD", "ETH-USD", "XRP-USD"  # Add all the pairs you support
    ]
    if pair not in supported_pairs:
        logging.error(f"Invalid trading pair: {pair}")
        raise ValueError(f"Invalid trading pair: {pair}. Please choose a valid pair.")
    logging.info(f"Validated trading pair: {pair}")

# Function to place a buy order for a specific amount (flat amount in USD)
def buy_crypto(product_id, amount):
    """Place a buy order for a specific amount of the product."""
    try:
        logging.info(f"Placing a buy order for {amount} worth of {product_id}...")
        client_order_id = str(uuid.uuid4())
        response = client.market_order_buy(
            product_id=product_id,
            quote_size=str(amount),
            client_order_id=client_order_id
        )
        logging.info("Buy order API response: %s", response)
    except Exception as e:
        logging.error(f"Buy order failed: {str(e)}")

# Function to place a sell order for a specific amount
def sell_crypto(product_id, amount):
    """Place a sell order for a specific amount of the product."""
    try:
        logging.info(f"Placing a sell order for {amount} of {product_id}...")
        client_order_id = str(uuid.uuid4())
        response = client.market_order_sell(
            product_id=product_id,
            base_size=str(amount),
            client_order_id=client_order_id
        )
        logging.info("Sell order API response: %s", response)
    except Exception as e:
        logging.error(f"Sell order failed: {str(e)}")

# Webhook endpoint for TradingView or other alerts to trigger buy/sell
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
        product_id = f"{coin}-{pair}"  # Correct pair format

        # Validate the trading pair
        validate_pair(product_id)

        mode = params.get("mode", "$")  # Default to $ mode
        buy_percentage = params.get("buy_%", 0)
        sell_percentage = params.get("sell_%", 0)
        buy_flat = params.get("buy_$", 0)
        sell_flat = params.get("sell_$", 0)

        # Determine the action from webhook
        action = data.get("action", "").lower()

        if action == "buy":
            if mode == "%":
                # Implement percentage buy logic
                pass
            elif mode == "$":
                buy_crypto(product_id, buy_flat)
            else:
                return "Invalid mode specified.", 400
            return "Buy order executed!", 200

        elif action == "sell":
            if mode == "%":
                # Implement percentage sell logic
                pass
            elif mode == "$":
                sell_crypto(product_id, sell_flat)
            else:
                return "Invalid mode specified.", 400
            return "Sell order executed!", 200

        else:
            return "Invalid action", 400

    except Exception as e:
        logging.error(f"Webhook processing failed: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Start the Flask server
