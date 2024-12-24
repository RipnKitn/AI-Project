from coinbase_advanced_trader.enhanced_rest_client import EnhancedRESTClient
from dotenv import load_dotenv
import os
import uuid  # For generating unique order IDs
from flask import Flask, request  # Flask for the server and request to handle incoming webhooks

# Load environment variables from .env file
load_dotenv()

# Retrieve API key and secret from environment variables
api_key = os.getenv("API_KEY")
api_secret = os.getenv("API_SECRET")

# Initialize the EnhancedRESTClient
client = EnhancedRESTClient(api_key=api_key, api_secret=api_secret)

# Define a secret key for secure webhook access
SECRET_KEY = "your_secret_key_here"  # Replace this with your unique key

# Initialize Flask app
app = Flask(__name__)

@app.route('/webhook', methods=['POST'])  # Webhook endpoint
def webhook():
    # Parse the incoming JSON payload
    data = request.get_json()

    # Validate the secret key in the payload
    if data.get("secret") != SECRET_KEY:
        return "Unauthorized", 401  # Respond with a 401 Unauthorized status if the key is invalid

    # Log the received data
    print("Authorized webhook received:", data)

    # Perform actions based on the payload
    action = data.get("action")  # Extract the action from the payload
    if action == "buy_giga":
        buy_giga()  # Trigger GIGA purchase logic
        return "Purchase triggered!"
    else:
        return "Unknown action", 400  # Respond with an error for unknown actions


def buy_giga():
    """
    Place a $1 market order for GIGA using USDC.
    """
    try:
        print("Attempting to place a market order for $1 GIGA...")
        # Generate a unique client order ID
        client_order_id = str(uuid.uuid4())

        # Use the correct method to place a market order
        response = client.market_order_buy(
            product_id="GIGA-USDC",  # Replace with the correct trading pair ID
            funds="1",              # USD amount to spend
            client_order_id=client_order_id  # Unique order identifier
        )
        print("Order placed:", response)  # Log the response from Coinbase
    except Exception as e:
        print("Order failed:", str(e))  # Log any errors


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Start the Flask server