from flask import Flask, request, jsonify

app = Flask(__name__)

# Root route to handle GET requests
@app.route('/', methods=['GET'])
def home():
    return "Webhook server is running!"

# Webhook route to handle POST requests from TradingView or other services
@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.json  # Get the JSON data from the request
        if not data:
            return jsonify({"error": "No data received"}), 400  # Return error if no data

        # Print out the received data
        print(f"Received data: {data}")

        # Extract the necessary values from the received data
        symbol = data.get('symbol')
        price = data.get('price')
        action = data.get('action')
        amount = data.get('amount')
        order_type = data.get('order_type')

        # Process the received data and execute actions based on it
        print(f"Action: {action}, Symbol: {symbol}, Price: {price}, Amount: {amount}")

        # Here, you could place the buy/sell order using the API for your exchange (like Coinbase)
        # Example: execute_order(symbol, action, price, amount, order_type)

        return jsonify({"status": "success", "message": "Webhook received successfully!"}), 200
    except Exception as e:
        print(f"Error handling the webhook: {e}")
        return jsonify({"status": "error", "message": "Error handling the webhook"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
