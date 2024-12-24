from coinbase_advanced_trader.enhanced_rest_client import EnhancedRESTClient
from flask import Flask, request
from dotenv import load_dotenv
import os
import uuid

# Load environment variables from .env file
load_dotenv()

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
SECRET_KEY = "your_actual_secret_key_here"  # Replace with your desired secret key for webhook validation

if not API_KEY or not API_SECRET:
    raise RuntimeError("Missing API credentials in .env")

# Initialize the EnhancedRESTClient
client = EnhancedRESTClient(api_key=API_KEY, api_secret=API_SECRET)

# Initialize Flask app
app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        # Parse incoming webhook data
        data = request.get_json()
        print("Webhook received:", data)

        # Validate secret key
        if data.get("secret") != SECRET_KEY:
            return "Unauthorized", 401

        # Handle actions
        action = data.get("action")
        if action == "buy_giga":
            buy_giga(data.get("percentage_or_fixed", 90), data.get("is_fixed", False))
            return "Buy order triggered!"
        elif action == "sell_giga":
            sell_giga(data.get("percentage_or_fixed", 80), data.get("is_fixed", False))
            return "Sell order triggered!"
        else:
            return "Unknown action", 400
    except Exception as e:
        print("Error processing webhook:", str(e))
        return "Error", 500


def buy_giga(percentage_or_fixed, is_fixed):
    try:
        usdc_balance = get_balance("USDC")
        if usdc_balance <= 0:
            print("Insufficient USDC balance!")
            return

        # Calculate trade size
        trade_size = percentage_or_fixed if is_fixed else round(usdc_balance * (percentage_or_fixed / 100), 2)

        if trade_size < 1:
            print("Trade size too small!")
            return

        print(f"Attempting to buy {trade_size} USDC worth of GIGA...")
        client_order_id = str(uuid.uuid4())

        response = client.market_order_buy(
            product_id="GIGA-USDC",
            quote_size=str(trade_size),
            client_order_id=client_order_id
        )
        print("Buy order placed:", response)
    except Exception as e:
        print("Buy order failed:", str(e))


def sell_giga(percentage_or_fixed, is_fixed):
    try:
        giga_balance = get_balance("GIGA")
        if giga_balance <= 0:
            print("Insufficient GIGA balance!")
            return

        trade_size = percentage_or_fixed if is_fixed else round(giga_balance * (percentage_or_fixed / 100), 8)

        if trade_size < 0.0001:
            print("Trade size too small!")
            return

        print(f"Attempting to sell {trade_size} GIGA...")
        client_order_id = str(uuid.uuid4())

        response = client.market_order_sell(
            product_id="GIGA-USDC",
            base_size=str(trade_size),
            client_order_id=client_order_id
        )
        print("Sell order placed:", response)
    except Exception as e:
        print("Sell order failed:", str(e))


def get_balance(currency):
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
