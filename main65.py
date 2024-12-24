from coinbase_advanced_trader.enhanced_rest_client import EnhancedRESTClient
from dotenv import load_dotenv
import os
from flask import Flask, request

# Load environment variables from .env file
load_dotenv()

# Retrieve API key and secret from environment variables
api_key = os.getenv("API_KEY")
api_secret = os.getenv("API_SECRET")

# Initialize the EnhancedRESTClient
client = EnhancedRESTClient(api_key=api_key, api_secret=api_secret)

# Define a secret key for secure webhook access
SECRET_KEY = "your_secret_key_here"  # Replace this with a strong, unique key

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
        return "Purchase triggered!"  # Respond to TradingView
    else:
        return "Unknown action", 400  # Respond with an error for unknown actions

def buy_giga():
    """
    Place a $1 market order for GIGA using USDC.
    """
    try:
        response = client.create_market_order(
            product_id="GIGA-USDC",  # Replace with your actual trading pair ID
            side="buy",
            funds="1"  # USD amount to spend
        )
        print("Order placed:", response)  # Log the response from Coi
