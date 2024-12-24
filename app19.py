from flask import Flask, request
from dotenv import load_dotenv
import os
import cbpro

# Load environment variables from the .env file
load_dotenv()

# Access the environment variables in your code
COINBASE_API_KEY = os.getenv("COINBASE_API_KEY")
COINBASE_API_SECRET = os.getenv("COINBASE_API_SECRET")
COINBASE_ORGANIZATION_ID = os.getenv("COINBASE_ORGANIZATION_ID")

# Initialize the Flask app
app = Flask(__name__)

# Function to place an order on Coinbase
def place_order(symbol, price, action, amount, order_type):
    # Create a Coinbase Pro client
    client = cbpro.AuthenticatedClient(COINBASE_API_KEY, COINBASE_API_SECRET, COINBASE_ORGANIZATION_ID)

    # Prepare the order details
    if action == "buy":
        side = "buy"
    elif action == "sell":
        side = "sell"
    else:
        return "Invalid action"

    # Create the order
    try:
        order = client.place_market_order(
            product_id=symbol,
            side=side,
            funds=amount  # The amount of currency to buy/sell
        )
        return order
    except Exception as e:
        return f"Error placing order: {str(e)}"

# Route for receiving webhook requests
@app.route("/", methods=["GET", "POST"])
def webhook():
    if request.method == "POST":
        data = request.get_json()
        symbol = data.get("symbol")
        price = data.get("price")
        action = data.get("action")
        amount = data.get("amount")
        order_type = data.get("order_type")

        if not all([symbol, price, action, amount, order_type]):
            return "Missing data in the request", 400

        # Place the order
        order_response = place_order(symbol, price, action, amount, order_type)

        return order_response

    return "Webhook is running", 200

if __name__ == "__main__":
    app.run(debug=True)
