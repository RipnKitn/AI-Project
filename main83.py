from flask import Flask, request
from coinbase_advanced_trader.enhanced_rest_client import EnhancedRESTClient
import json
import uuid

# Load API credentials from environment variables
API_KEY = "your_api_key_here"
API_SECRET = "your_api_secret_here"

# Initialize Coinbase Advanced REST Client
client = EnhancedRESTClient(api_key=API_KEY, api_secret=API_SECRET)

# Initialize Flask app
app = Flask(__name__)

# Load configuration files
PAIRS_FILE = "pairs.json"
PARAMETERS_FILE = "parameters.json"

def load_file(file_path, default_value):
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return default_value

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    if not data:
        return "Invalid payload", 400

    action = data.get("action")
    if action == "buy":
        handle_buy()
        return "Buy order triggered!", 200
    elif action == "sell":
        handle_sell()
        return "Sell order triggered!", 200
    else:
        return "Unknown action", 400

def handle_buy():
    params = load_file(PARAMETERS_FILE, {"buy_percentage": 90, "pair": "GIGA-USDC"})
    pairs = load_file(PAIRS_FILE, [])
    pair = params.get("pair", "GIGA-USDC")
    if pair not in pairs:
        print(f"Invalid trading pair: {pair}")
        return

    usdc_balance = get_balance("USDC")
    if usdc_balance <= 0:
        print("Insufficient USDC balance!")
        return

    trade_size = round(usdc_balance * (params["buy_percentage"] / 100), 2)
    if trade_size < 1:
        print("Trade size too small!")
        return

    print(f"Placing buy order for {trade_size} USDC worth of {pair}...")
    client_order_id = str(uuid.uuid4())
    response = client.market_order_buy(
        product_id=pair, quote_size=str(trade_size), client_order_id=client_order_id
    )
    print("Buy order response:", response)

def handle_sell():
    params = load_file(PARAMETERS_FILE, {"sell_percentage": 80, "pair": "GIGA-USDC"})
    pairs = load_file(PAIRS_FILE, [])
    pair = params.get("pair", "GIGA-USDC")
    if pair not in pairs:
        print(f"Invalid trading pair: {pair}")
        return

    giga_balance = get_balance(pair.split("-")[0])  # Extract the base currency from the pair
    if giga_balance <= 0:
        print("Insufficient crypto balance!")
        return

    trade_size = round(giga_balance * (params["sell_percentage"] / 100), 8)
    if trade_size < 0.0001:
        print("Trade size too small!")
        return

    print(f"Placing sell order for {trade_size} of {pair.split('-')[0]}...")
    client_order_id = str(uuid.uuid4())
    response = client.market_order_sell(
        product_id=pair, base_size=str(trade_size), client_order_id=client_order_id
    )
    print("Sell order response:", response)

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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
