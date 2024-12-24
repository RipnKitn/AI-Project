import os
from flask import Flask, request, jsonify
from coinbase.wallet.client import Client

app = Flask(__name__)

# Coinbase API credentials from environment
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
client = Client(API_KEY, API_SECRET)

# Function to place a trade
def place_trade(symbol, side, trade_amount=None, percentage=None):
    try:
        # Fetch account balance
        account = client.get_accounts()
        balance = 0
        for acct in account.data:
            if acct['currency'] == symbol.split('-')[0]:
                balance = float(acct['balance']['amount'])
        
        if balance <= 0:
            return {"error": "Insufficient balance"}

        # Determine trade amount
        if percentage:
            trade_amount = round(balance * (percentage / 100), 6)
        
        if trade_amount > balance:
            return {"error": "Trade amount exceeds balance"}

        # Place order (pseudo-code for Coinbase Pro)
        # Replace with actual Coinbase API trade placement
        if side == "sell":
            response = {"message": f"Sell order placed for {trade_amount} {symbol}"}
        elif side == "buy":
            response = {"message": f"Buy order placed for {trade_amount} {symbol}"}
        else:
            response = {"error": "Invalid trade side"}
        
        return response
    except Exception as e:
        return {"error": str(e)}

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    symbol = data.get("symbol")
    side = data.get("side")
    percentage = data.get("percentage", None)

    if not symbol or not side:
        return jsonify({"status": "error", "message": "Invalid parameters"}), 400

    result = place_trade(symbol, side, percentage=percentage)
    return jsonify({"status": "success", "result": result}), 200

if __name__ == "__main__":
    app.run(debug=True, port=80)
