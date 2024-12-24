from coinbase_advanced_trader.enhanced_rest_client import EnhancedRESTClient
from dotenv import load_dotenv
import os
from flask import Flask, request  # Flask for the server and request to handle incoming webhooks

# Load environment variables from .env file
load_dotenv()

# Retrieve API key and secret from environment variables
api_key = os.getenv("API_KEY")
api_secret = os.getenv("API_SECRET")

# Initialize the EnhancedRESTClient
client = EnhancedRESTClient(api_key=api_key, api_secret=api_secret)

# Debug: List all available methods of the client
print("Available methods for EnhancedRESTClient:")
print(dir(client))

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
        return "Purchase triggered!"
    else:
        return "Unknown action", 400  # Respond with an error for unknown actions


def buy_giga():
    """
    Placeholder for the GIGA purchase logic. This will be updated once we know the correct method.
    """
    try:
        print("Attempting to place a market order for $1 GIGA...")
        # Replace `place_order` with the correct method once identified
        response = client.place_order(
            product_id="GIGA-USDC",  # Replace with the correct trading pair ID
            side="buy",
            funds="1"  # USD amount to spend
        )
        print("Order placed:", response)  # Log the response from Coinbase
    except Exception as e:
        print("Order failed:", str(e))  # Log any errors


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Start the Flask server
