from coinbase_advanced_trader.enhanced_rest_client import EnhancedRESTClient
from dotenv import load_dotenv
import json
import os
import uuid
from flask import Flask, request

# Load environment variables
load_dotenv()
api_key = os.getenv("API_KEY")
api_secret = os.getenv("API_SECRET")
webhook_secret = os.getenv("WEBHOOK_SECRET", "your_secret_key_here")

# Initialize Coinbase Client
client = EnhancedRESTClient(api_key=api_key, api_secret=api_secret)

# Flask App Setup
app = Flask(__name__)

# Load parameters from parameters.json
def load_parameters(file_path="parameters.json"):
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: {file_path} not found.")
        return {}
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in {file_path}.")
        return {}

# Load pairs from pairs.json
def load_pairs(file_path="pairs.json"):
    """Load tradable pairs from pairs.json."""
    try:
        with open(file_path, "r") as f:
            return json.load(f).get("pairs", [])
    except (FileNotFoundError, KeyError):
        print(f"Error: Could not load pairs from {file_path}.")
        return []

pairs = load_pairs()

# Calculate buy/sell amounts
def calculate_amount(action, params, wallet, price):
    mode = params.get("mode", "$")
    percentage = params.get(f"{action}_%", 0)
    fixed_amount = params.get(f"{action}_$", 0)
    source = params.get(f"{action}% from", "C")

    if mode == "$":
        return fixed_amount / price if action == "buy" else fixed_amount
    elif mode == "%":
        if source == "C":
            return wallet.get(params["coin"], 0) * (percentage / 100)
        elif source == "P":
            return wallet.get(params["pair"], 0) * (percentage / 100) / price if action == "buy" else wallet.get(params["pair"], 0) * (percentage / 100)
    return 0

# Simulated wallet for testing
wallet = {"coin": 10, "pair": 100}  # Example: 10 GIGA, 100 USDC
current_price = 2.0  # Example: 1 GIGA = 2 USDC

# Webhook Route
@app.route('/webhook', methods=['POST'])
def webhook():
    """Handle TradingView alerts via webhooks."""
    data = request.get_json()

    # Validate the secret key
    if data.get("secret") != webhook_secret:
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
    """Execute a buy or sell trade based on parameters and wallet balances."""
    try:
        # Load parameters
        params = load_parameters()

        # Determine trading pair
        coin = params["coin"]
        pair = params["pair"]
        product_id = f"{coin}-{pair}"

        # Calculate trade amounts
        trade_amount = calculate_amount(action, params, wallet, current_price)

        if action == "buy":
            print(f"Placing buy order for {trade_amount} {pair}.")
            client.market_order_buy(
                product_id=product_id,
                base_size=str(trade_amount / current_price),  # Convert pair amount to coin amount
                client_order_id=str(uuid.uuid4())
            )
        elif action == "sell":
            print(f"Placing sell order for {trade_amount} {coin}.")
            client.market_order_sell(
                product_id=product_id,
                base_size=str(trade_amount),  # Already in terms of coin
                client_order_id=str(uuid.uuid4())
            )
    except Exception as e:
        print(f"{action.capitalize()} trade failed: {str(e)}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
