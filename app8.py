from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

@app.route('/')
def home():
    return "Webhook server is running!", 200

@app.route('/webhook', methods=['POST'])
def handle_webhook():
    try:
        # Retrieve the data from the POST request
        data = request.json
        
        # You can log the incoming data for debugging purposes
        print(f"Received data: {data}")

        # Example: handle the 'symbol' and 'action' from TradingView
        symbol = data.get('symbol')
        price = data.get('price')
        action = data.get('action')
        amount = data.get('amount')
        order_type = data.get('order_type')

        # Perform the necessary actions based on the data (you can add your logic here)
        # Example: Just return the data for now (you can replace this with your actual trading logic)
        return jsonify({
            'status': 'success',
            'symbol': symbol,
            'price': price,
            'action': action,
            'amount': amount,
            'order_type': order_type
        }), 200

    except Exception as e:
        # Handle any errors
        print(f"Error handling webhook: {e}")
        return jsonify({'status': 'error', 'message': 'Failed to process the webhook'}), 400

if __name__ == '__main__':
    app.run(debug=True)
