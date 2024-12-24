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
    try:
        with open(file_path, "r") as f:
            return json.load(f).get("pairs", [])
    except (FileNotFoundError, KeyError):
        print(f"Error: Could not load pairs from {file_path}.")
        return []

pairs = load_pairs()

# Fetch all account UUIDs dynamically with debug output
def fetch_account_ids():
    try:
        accounts = client.get_accounts()
        print(f"Accounts response: {accounts}")  # Debugging output to see the API response
        account_map = {}
        for account in accounts["accounts"]:
            print(f"ID: {account['id']}, Name: {account['name']}, Balance: {account['balance']['amount']} {account['balance']['currency']}")
            account_map[account["currency"]] = account["id"]
        return account_map
    except Exception as e:
        print(f"Error fetching accounts: {e}")
        return {}

# Map accounts dynamically
account_ids = fetch_account_ids()

# Fetch current price dynamically
def get_current_price(product_id):
    try:
        product = client.get_product(product_id)
        return float(product["price"])
    except Exception as e:
        print(f"Failed to fetch price for {product_id}: {e}")
        return None

# Calculate buy/sell amounts
def calculate_amount(action, params, wallet, price):
    mode = params.get("mode", "$")  # Either "$" or "%"
    fixed_amount = params.get(f"{action}_$", 0)
    percentage = params.get(f"{action}_%", 0)

    if mode == "$":
        return fixed_amount / price  # Buy or sell based on pair amount

    elif mode == "%":
        pair_balance = wallet.get("pair", 0)
        return (pair_balance * percentage / 100) / price if action == "buy" else (pair_balance * percentage / 100)

    return 0  # Fallback in case of invalid mode

# Fetch and print current wallet balances dynamically based on UUIDs
params = load_parameters()
coin = params.get("coin")
pair = params.get("pair")

# Map UUIDs to currencies dynamically
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

# Log trades
def log_trade(action, amount, price):
    with open("trades_log.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([action, amount, price, str(uuid.uuid4())])
        print(f"Trade logged: {action} {amount} at {price}")

# Send notifications
def send_notification(action, amount, price):
    print(f"Notification: {action.upper()} {amount} at {price}.")

# Webhook Route
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    print("Webhook authorized:", data)
    action = data.get("action")

    if action in ["buy", "sell"]:
        process_trade(action)
        return f"{action.capitalize()} executed!", 200
    return "Unknown action", 400

# Process trade
def process_trade(action):
    try:
        product_id = f"{coin}-{pair}"
        current_price = get_current_price(product_id)
        if not current_price:
            print("Price fetch failed. Aborting trade.")
            return

        trade_amount = calculate_amount(action, params, wallet, current_price)

        if action == "buy":
            print(f"Placing buy order for {trade_amount} {pair}.")
            log_trade("buy", trade_amount / current_price, current_price)
            send_notification("buy", trade_amount / current_price, current_price)
        elif action == "sell":
            print(f"Placing sell order for {trade_amount} {coin}.")
            log_trade("sell", trade_amount, current_price)
            send_notification("sell", trade_amount, current_price)

        # Update simulated wallet
        if action == "buy":
            wallet["pair"] -= trade_amount
            wallet["coin"] += trade_amount / current_price
        elif action == "sell":
            wallet["coin"] -= trade_amount
            wallet["pair"] += trade_amount * current_price

        print(f"Updated wallet: {wallet}")

    except Exception as e:
        print(f"{action.capitalize()} trade failed: {str(e)}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
