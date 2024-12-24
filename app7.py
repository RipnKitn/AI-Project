from flask import Flask, request
import json
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json  # Get JSON data from TradingView webhook
    print("Received data:", data)  # Print out the data to verify

    # Implement logic to process the data, for example:
    symbol = data.get('symbol')
    price = data.get('price')
    action = data.get('action')

    # Logic for placing an order or taking action based on received data
    print(f"Action: {action}, Symbol: {symbol}, Price: {price}")

    return 'OK', 200  # Return a success response

@app.route('/')
def home():
    return 'This is the homepage!'

if __name__ == "__main__":
    app.run(debug=True, port=5000)
