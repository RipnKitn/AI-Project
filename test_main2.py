from flask import Flask, request
import os
from coinbase.wallet.client import Client

app = Flask(__name__)

# Set up Coinbase API credentials
api_key = os.getenv('COINBASE_API_KEY')
api_secret = os.getenv('COINBASE_API_SECRET')
passphrase = os.getenv('COINBASE_PASSPHRASE')
client = Client(api_key, api_secret)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()

    if data['secret'] == os.getenv('WEBHOOK_SECRET'):  # Replace with your secret
        action = data['action']  # 'buy' or 'sell'

        if action == 'buy':
            # Execute buy order
            buy_order()
        elif action == 'sell':
            # Execute sell order
            sell_order()

    return 'OK', 200

def buy_order():
    # Execute buy logic here (example)
    client.place_market_order('BTC-USD', 'buy', funds='10.00')  # Buy $10 worth of BTC

def sell_order():
    # Execute sell logic here (example)
    client.place_market_order('BTC-USD', 'sell', size='0.001')  # Sell 0.001 BTC

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
