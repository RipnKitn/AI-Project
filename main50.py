from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Webhook route - POST only
@app.route('/webhook', methods=['POST'])
def webhook():
    # Get JSON data sent to the webhook
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON payload received!"}), 400

    # Check for required parameters
    symbol = data.get("symbol")
    side = data.get("side")
    quantity = data.get("quantity")

    if not symbol or not side or not quantity:
        return jsonify({"error": "Missing parameters! Required: symbol, side, quantity"}), 400

    # Simulated success response
    response = {
        "status": "success",
        "message": "Order received successfully",
        "data": {
            "symbol": symbol,
            "side": side,
            "quantity": quantity
        }
    }
    return jsonify(response), 200


if __name__ == '__main__':
    app.run(debug=True, port=80)
