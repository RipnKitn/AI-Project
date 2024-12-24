from coinbase_advanced_trader.enhanced_rest_client import EnhancedRESTClient
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Retrieve API key and secret from environment variables
api_key = os.getenv("API_KEY")
api_secret = os.getenv("API_SECRET")

# Initialize the EnhancedRESTClient
client = EnhancedRESTClient(api_key=api_key, api_secret=api_secret)

from flask import Flask, request

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])  # This tells Flask to listen for POST requests at /webhook
def webhook():
    return "Webhook received!"  # This is a basic placeholder response

