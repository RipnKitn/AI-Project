from coinbase_advanced_trader.enhanced_rest_client import EnhancedRESTClient
from dotenv import load_dotenv
import json
import os
import uuid
from flask import Flask, request
import csv

# Load environment variables
load_dotenv()
api_key = os.getenv("API_KEY")
api_secret = os.getenv("API_SECRET")

# Initialize Coinbase Client
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

def load_pairs(file_path="pairs.json"):
    """Load trading pairs from pairs.json."""
    try:
        with open(file_path, "r") as f:
            data = json.load(f)
            return data.get("pairs", [])
    except FileNotFoundError:
        print(f"Error: {file_path} not found.")
        return []
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in {file_path}.")
        return []

def fetch_account_ids():
    """Fetch all account UUIDs dynamically."""
    try:
        accounts = client.get_accounts()
        account_map = {}
        for account in accounts["accounts"]:
            account_map[account["currency"]] = account["id"]
        return account_map
    except Exception as e:
        print(f"Error fetching accounts: {e}")
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

    if action == "trade":
        process_trade()
        return "Trade executed!", 200
    return "Unknown action", 400

def process_trade():
    """Process buy or sell trades based on parameters.json."""
    try:
        params = load_parameters()
        pairs = load_pairs()
        account_ids = fetch_account_ids()

        coin = params["coin"]
        pair = params["pair"]
        product_id = f"{coin}-{pair}"

        # Fetch wallet balances dynamically based on UUIDs
        wallet = {}
        if coin in account_ids:
            wallet["coin"] = client.get_account(account_ids[coin])["balance"]
        else:
            print(f"Error: No account found for coin {coin}. Defaulting to 0 balance.")
            wallet["coin"] = 0

        if pair in account_ids:
            wallet["pair"] = client.get_account(account_ids[pair])["balance"]
        else:
            print(f"Error: No account found for pair {pair}. Defaulting to 0 balance.")
            wallet["pair"] = 0

        print(f"Current wallet balances: {wallet}")

        # Simulated price (should be replaced by actual price fetching)
        price = get_current_price(product_id)
        if not price:
            print("Failed to fetch price. Aborting trade.")
            return

        # Calculate amounts
        buy_amount = calculate_amount("buy", params, wallet, price)
        sell_amount = calculate_amount("sell", params, wallet, price)

        # Execute trades
        if params["mode"] == "$":
            print(f"Placing buy order for {buy_amount} {coin} for ${params['buy_$']}.")
            client.market_order_buy(
                product_id=product_id,
                quote_size=params["buy_$"],
                client_order_id=str(uuid.uuid4())
            )
            print(f"Placing sell order for {sell_amount} {coin} for ${params['sell_$']}.")
            client.market_order_sell(
                product_id=product_id,
                quote_size=params["sell_$"],
                client_order_id=str(uuid.uuid4())
            )
        elif params["mode"] == "%":
            print(f"Placing buy order for {buy_amount} {coin}.")
            client.market_order_buy(
                product_id=product_id,
                base_size=str(buy_amount),
                client_order_id=str(uuid.uuid4())
            )
            print(f"Placing sell order for {sell_amount} {coin}.")
            client.market_order_sell(
                product_id=product_id,
                base_size=str(sell_amount),
                client_order_id=str(uuid.uuid4())
            )
    except Exception as e:
        print(f"Trade processing failed: {str(e)}")

def get_current_price(product_id):
    """Fetch current price dynamically from Coinbase."""
    try:
        product = client.get_product(product_id)
        return float(product["price"])
    except Exception as e:
        print(f"Failed to fetch price for {product_id}: {e}")
        return None

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
