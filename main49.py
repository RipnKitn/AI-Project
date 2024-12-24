from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")

# Flask app setup
app = Flask(__name__)

# Webhook endpoint
@app.route('/webhook', methods=['POST'])
def webhook():
    # Get JSON data from request
    data = request.get_json()

    # Validate parameters
    symbol = data.get("symbol")
    side = data.get("side")
    quantity = data.get("quantity")  # Add this parameter
    
    if not symbol or not side or not quantity:
        return jsonify({"error": "Missing parameters! Please provide 'symbol', 'side', and 'quantity'."}), 400

    # Log the received data
    print(f"Received order - Symbol: {symbol}, Side: {side}, Quantity: {quantity}")
    
    # Simulate processing (replace with actual API logic if needed)
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
