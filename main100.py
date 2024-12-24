import os
import json
import uuid
from dotenv import load_dotenv
from flask import Flask, request
from trade_logic import calculate_buy_amount, calculate_sell_amount, load_parameters
from coinbase_advanced_trader.enhanced_rest_client import EnhancedRESTClient

# Load environment variables
load_dotenv()
api_key = os.getenv("API_KEY")
api_secret = os.getenv("API_SECRET")

# Initialize Coinbase Client
client = EnhancedRESTClient(api_key=api_key, api_secret=api_secret)

# Flask App Setup
app = Flask(__name__)

# Load Pairs from pairs.json
def load_pairs(file_path="pairs.json"):
    try:
        with open(file_path, "r") as f:
            return json.load(f)["pairs"]
    except (FileNotFoundError, KeyError):
        print(f"Error: Could not load pairs from {file_path}.")
        return []

pairs = load_pairs()

# Simulated wallet for testing
wallet = {"coin": 10, "pair": 100}  # Example: 10 GIGA, 100 USDC
current_price = 2.0  # Example: 1 GIGA = 2 USDC

# Webhook Route
@app.route('/webhook', methods=['POST'])
def webhook():
    """Handle TradingView alerts via webhooks."""
    data = request.get_json()

    print("Webhook received:", data)
    action = data.get("action")

    if action == "buy":
        execute_trade("buy")
        return "Buy executed!", 200
    elif action == "sell":
        execute_trade("sell")
        return "Sell executed!", 200
    return "Unknown action", 400

def execute_trade(action):
    """Execute a buy or sell trade based on parameters and wallet balances."""
    try:
        # Load parameters
        params = load_parameters()

        # Determine trading pair
        coin = params["coin"]
        pair = params["pair"]
        product_id = f"{coin}-{pair}"

        # Calculate trade amounts
        if action == "buy":
            trade_amount = calculate_buy_amount(wallet, current_price, params)
            print(f"Calculated Buy Amount: {trade_amount} {pair}")
            client.market_order_buy(
                product_id=product_id,
                base_size=str(trade_amount / current_price),  # Convert pair amount to coin amount
                client_order_id=str(uuid.uuid4())
            )
        elif action == "sell":
            trade_amount = calculate_sell_amount(wallet, current_price, params)
            print(f"Calculated Sell Amount: {trade_amount} {coin}")
            client.market_order_sell(
                product_id=product_id,
                base_size=str(trade_amount),  # Already in terms of coin
                client_order_id=str(uuid.uuid4())
            )
    except Exception as e:
        print(f"{action.capitalize()} trade failed: {str(e)}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
