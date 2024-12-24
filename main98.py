from coinbase_advanced_trader.enhanced_rest_client import EnhancedRESTClient
from dotenv import load_dotenv
import json
import os
import uuid
from flask import Flask, request

# Load environment variables from .env file
load_dotenv()
api_key = os.getenv("API_KEY")
api_secret = os.getenv("API_SECRET")

# Initialize the EnhancedRESTClient
client = EnhancedRESTClient(api_key=api_key, api_secret=api_secret)

# Flask App Setup
app = Flask(__name__)

# Secret key for webhook authentication
SECRET_KEY = os.getenv("WEBHOOK_SECRET", "your_secret_key_here")

# Utility functions
def load_parameters(file_path="parameters.json"):
    """Load trading parameters from parameters.json."""
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: {file_path} not found.")
        return {}
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in {file_path}.")
        return {}

def calculate_amount(action, params, wallet, price):
    """
    Calculate the buy/sell amount based on parameters and wallet balance.
    
    Args:
        action (str): "buy" or "sell".
        params (dict): Parameters from parameters.json.
        wallet (dict): Wallet balances.
        price (float): Current price of the coin.

    Returns:
        float: Amount to trade.
    """
    mode = params.get("mode", "$")
    percentage = params.get(f"{action}_%", 0)
    fixed_amount = params.get(f"{action}_$", 0)
    source = params.get(f"{action}% from", "C")

    if mode == "$":
        return fixed_amount / price
    elif mode == "%":
        if source == "C":
            return wallet.get(params["coin"], 0) * (percentage / 100)
        elif source == "P":
            return wallet.get(params["pair"], 0) * (percentage / 100) / price
    return 0

# Flask Routes
@app.route('/webhook', methods=['POST'])
def webhook():
    """Handle incoming webhooks."""
    data = request.get_json()

    # Validate the secret key
    if data.get("secret") != SECRET_KEY:
        return "Unauthorized", 401

    print("Webhook received:", data)
    action = data.get("action")

    if action == "buy":
        process_trade("buy")
        return "Buy executed!", 200
    elif action == "sell":
        process_trade("sell")
        return "Sell executed!", 200
    return "Unknown action", 400

def process_trade(action):
    """Process buy or sell trades based on parameters.json."""
    try:
        params = load_parameters()
        coin = params["coin"]
        pair = params["pair"]
        product_id = f"{coin}-{pair}"

        # Simulate wallet balances and current price
        wallet = {coin: 10, pair: 100}
        price = 0.5  # Example: 1 GIGA = 0.5 USDC

        # Calculate amount to trade
        trade_amount = calculate_amount(action, params, wallet, price)

        # Execute trade
        if action == "buy":
            print(f"Placing buy order for {trade_amount} {coin}.")
            client.market_order_buy(
                product_id=product_id,
                base_size=str(trade_amount),
                client_order_id=str(uuid.uuid4())
            )
        elif action == "sell":
            print(f"Placing sell order for {trade_amount} {coin}.")
            client.market_order_sell(
                product_id=product_id,
                base_size=str(trade_amount),
                client_order_id=str(uuid.uuid4())
            )
    except Exception as e:
        print(f"{action.capitalize()} processing failed:", str(e))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
