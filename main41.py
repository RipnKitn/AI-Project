import os
from flask import Flask, request, jsonify
from coinbase.wallet.client import Client

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Get Coinbase API credentials from .env
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")

# Initialize Coinbase client
client = Client(API_KEY, API_SECRET)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    if data:
        # Here you can add logic to handle the webhook data, such as placing a trade
        # For example, checking balance or placing a trade
        try:
            # Fetch balance for USD on Coinbase account
            account = client.get_account('USD')
            balance = account['balance']['amount']
            print(f"Current balance: {balance}")

            # Example: Place a trade logic here (for now, just returning balance)
            return jsonify({
                "status": "success",
                "balance": balance,
                "data_received": data
            }), 200
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500
    else:
        return jsonify({"status": "error", "message": "No data received"}), 400

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)
