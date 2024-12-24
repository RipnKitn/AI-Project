from coinbase_advanced_trader.enhanced_rest_client import EnhancedRESTClient
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Retrieve API key and secret from environment variables
api_key = os.getenv("API_KEY")
api_secret = os.getenv("API_SECRET")

# Initialize the EnhancedRESTClient
client = EnhancedRESTClient(api_key=api_key, api_secret=api_secret)

def buy_crypto(pair: str, amount: float, currency: str):
    """
    Function to place a buy order for a specified amount of crypto.

    :param pair: Trading pair (e.g., "GIGA-USDC").
    :param amount: Amount to spend (in base currency, e.g., USDC).
    :param currency: The base currency (e.g., "USDC").
    """
    try:
        # Place a market order to buy crypto
        order_response = client.place_order(
            product_id=pair, 
            side="buy",  # 'buy' for purchasing
            order_type="market",  # 'market' for market orders
            funds=str(amount)  # Amount in base currency to spend (e.g., $1 USDC)
        )
        print("Order placed successfully!")
        print(order_response)
    except Exception as e:
        print(f"Failed to place order: {e}")

# Specify trading pair and amount
trading_pair = "GIGA-USDC"  # Replace with the exact trading pair for GIGA and USDC
amount_to_spend = 1.0  # Spend $1 USDC

# Call the function to buy GIGA
buy_crypto(trading_pair, amount_to_spend, "USDC")
