import cbpro
import os
from dotenv import load_dotenv
from flask import Flask, request

# Load environment variables from .env
load_dotenv()

# Get API keys from .env
API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')
API_PASSPHRASE = os.getenv('API_PASSPHRASE')

# Initialize the Coinbase Pro client
client = cbpro.AuthenticatedClient(API_KEY, API_SECRET, API_PASSPHRASE)

# Flask app setup
app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return 'Flask app is running!'

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    symbol = data['symbol']
    price = data['price']
    action = data['action']
    amount = data['amount']
    order_type = data['order_type']
    
    print(f"Received data: {data}")
    
    # Example of placing a market order with Coinbase Pro
    if action == "buy":
        try:
            # Place a market order
            order = client.place_market_order(
                product_id=symbol,
                side='buy',
                funds=amount * price  # Assuming 'amount' is in USDC
            )
            print(f"Buy order placed: {order}")
            return {"message": "Buy order placed successfully", "status": 200}, 200
        except Exception as e:
            print(f"Error placing buy order: {str(e)}")
            return {"message": f"Error: {str(e)}", "status": 500}, 500
    else:
        return {"message": "Action not supported", "status": 400}, 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
