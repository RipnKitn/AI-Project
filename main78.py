from coinbase_advanced_trader.enhanced_rest_client import EnhancedRESTClient
from flask import Flask, request
import uuid

# Replace these with your actual API credentials
API_KEY = "your_api_key_here"
API_SECRET = "your_api_secret_here"

# Initialize the EnhancedRESTClient
client = EnhancedRESTClient(api_key=API_KEY, api_secret=API_SECRET)

# Define a secret key for secure webhook access
SECRET_KEY = "your_secret_key_here"

# Initialize Flask app
app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()

    # Validate the secret key in the payload
    if data.get("secret") != SECRET_KEY:
        return "Unauthorized", 401

    # Log the received data
    print("Authorized webhook received:", data)

    # Perform actions based on the payload
    action = data.get("action")
    if action == "buy_giga":
        buy_giga(data.get("percentage", 90), data.get("is_fixed", False))  # Default: 90% of USDC
        return "Buy order triggered!"
    elif action == "sell_giga":
        sell_giga(data.get("percentage", 80), data.get("is_fixed", False))  # Default: 80% of GIGA
        return "Sell order triggered!"
    else:
        return "Unknown action", 400


def buy_giga(percentage_or_fixed, is_fixed):
    """
    Buy GIGA using either a percentage of USDC balance or a fixed amount.
    """
    try:
        usdc_balance = get_balance("USDC")
        if usdc_balance <= 0:
            print("Insufficient USDC balance!")
            return

        # Calculate trade size
        trade_size = percentage_or_fixed if is_fixed else round(usdc_balance * (percentage_or_fixed / 100), 2)

        # Enforce minimum trade size
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
    """
    Sell GIGA using either a percentage of GIGA balance or a fixed amount.
    """
    try:
        giga_balance = get_balance("GIGA")
        if giga_balance <= 0:
            print("Insufficient GIGA balance!")
            return

        # Calculate trade size
        trade_size = percentage_or_fixed if is_fixed else round(giga_balance * (percentage_or_fixed / 100), 8)

        # Enforce minimum trade size
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
    """
    Retrieve the balance for a specific currency.
    """
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
