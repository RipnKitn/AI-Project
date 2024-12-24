import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import logging

# Initialize Flask app
app = Flask(__name__)

# Load environment variables
load_dotenv()
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")

# Verify API credentials
if not API_KEY or not API_SECRET:
    raise ValueError("Missing API_KEY or API_SECRET in .env file")

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Define the /webhook route
@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        # Log the incoming request
        logging.debug(f"Incoming request: {request.json}")

        # Parse the JSON payload
        data = request.json
        if not data:
            return jsonify({"error": "No data received"}), 400

        # Extract required parameters
        symbol = data.get("symbol")
        side = data.get("side")
        quantity = data.get("quantity")

        # Validate required parameters
        if not symbol or not side or not quantity:
            return jsonify({"error": "Missing parameters! Symbol, side, and quantity are required."}), 400

        # Log the received data
        logging.debug(f"Symbol: {symbol}, Side: {side}, Quantity: {quantity}")

        # Placeholder for trade execution logic
        # Example: Place a trade using Coinbase API or other logic
        logging.debug("Trade logic would execute here.")

        # Respond with success
        return jsonify({
            "status": "success",
            "message": "Webhook processed successfully",
            "received_data": {
                "symbol": symbol,
                "side": side,
                "quantity": quantity
            }
        }), 200

    except Exception as e:
        logging.error(f"Error processing webhook: {str(e)}")
        return jsonify({"error": f"Error processing webhook: {str(e)}"}), 500

if __name__ == "__main__":
    # Run the Flask app
    app.run(debug=True, port=80)
