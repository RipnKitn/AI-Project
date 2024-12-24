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

# Initialize Flask app
app = Flask(__name__)

@app.route('/webhook', methods=['POST'])  # Flask listens for POST requests at /webhook
def webhook():
    return "Webhook received!"  # Placeholder response to confirm it's working

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Start the Flask server on port 5000
