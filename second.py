from flask import Flask, request
import uuid
from trade_logic import load_parameters, calculate_buy_amount, calculate_sell_amount

# Simulated exchange client (replace with your actual client if available)
class MockExchangeClient:
    @staticmethod
    def market_order_buy(product_id, base_size, client_order_id):
        print(f"Buy Order: {base_size} of {product_id}, Order ID: {client_order_id}")

    @staticmethod
    def market_order_sell(product_id, base_size, client_order_id):
        print(f"Sell Order: {base_size} of {product_id}, Order ID: {client_order_id}")

client = MockExchangeClient()

# Flask App Setup
app = Flask(__name__)

# Simulated wallet balances
wallet = {"coin": 10, "pair": 100}  # Example: 10 GIGA, 100 USDC
current_price = 2.0  # Example: 1 GIGA = 2 USDC

@app.route('/webhook', methods=['POST'])
def webhook():
    """Handle incoming webhooks."""
    data = request.get_json()

    print("Webhook received:", data)
    action = data.get("action")

    if action == "buy":
        execute_trade("buy")
        return "Buy executed!", 200
    elif action == "sell":
        execute_trade("sell")
        return "Sell executed!", 200
    return "Unknown action", 400

def execute_trade(action):
    """Execute buy or sell trades."""
    try:
        # Load parameters
        params = load_parameters()

        # Determine product ID
        coin = params["coin"]
        pair = params["pair"]
        product_id = f"{coin}-{pair}"

        # Calculate trade amount
        if action == "buy":
            trade_amount = calculate_buy_amount(wallet, current_price, params)
            print(f"Calculated Buy Amount: {trade_amount} {pair}")
            client.market_order_buy(
                product_id=product_id,
                base_size=str(trade_amount / current_price),  # Convert pair value to coin value
                client_order_id=str(uuid.uuid4())
            )
        elif action == "sell":
            trade_amount = calculate_sell_amount(wallet, current_price, params)
            print(f"Calculated Sell Amount: {trade_amount} {coin}")
            client.market_order_sell(
                product_id=product_id,
                base_size=str(trade_amount),  # Already in terms of coin
                client_order_id=str(uuid.uuid4())
            )
    except Exception as e:
        print(f"{action.capitalize()} trade failed: {str(e)}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
