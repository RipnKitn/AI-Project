from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def home():
    return 'Webhook server is running!'

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        # Parse the incoming JSON data from the POST request
        data = request.json
        if data:
            print(f"Received data: {data}")
            
            # Example: log the action, symbol, price, and amount
            action = data.get('action')
            symbol = data.get('symbol')
            price = data.get('price')
            amount = data.get('amount')
            
            print(f"Action: {action}, Symbol: {symbol}, Price: {price}, Amount: {amount}")
            
            # You can add your trading logic here (e.g., place an order, etc.)

            return 'Webhook received', 200
        else:
            return 'Invalid data received', 400
    except Exception as e:
        return f'Error processing request: {str(e)}', 500

if __name__ == '__main__':
    app.run(debug=True)
