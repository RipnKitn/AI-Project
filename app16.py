import os
import cbpro
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Coinbase API Credentials from the .env file
API_KEY = os.getenv("COINBASE_API_KEY")
API_SECRET = os.getenv("COINBASE_API_SECRET")
PASSPHRASE = os.getenv("COINBASE_PASSPHRASE")

# Make sure the variables are set
if not API_KEY or not API_SECRET or not PASSPHRASE:
    raise ValueError("API_KEY, API_SECRET, or PASSPHRASE are missing. Please check your .env file.")

# Instantiate the Coinbase API client
client = cbpro.AuthenticatedClient(API_KEY, API_SECRET, PASSPHRASE)

# Example: Getting current account balance
def get_balance():
    try:
        accounts = client.get_accounts()
        for account in accounts:
            print(f"Currency: {account['currency']} | Balance: {account['balance']}")
    except Exception as e:
        print(f"Error retrieving balance: {e}")

# Example: Placing a limit order
def place_limit_order():
    try:
        # Example: Buy order for 0.1 BTC at price 50000 USD per BTC
        order = client.place_limit_order(
            product_id='BTC-USD',
            side='buy',
            price='50000',
            size='0.1'
        )
        print(f"Order placed: {order}")
    except Exception as e:
        print(f"Error placing order: {e}")

# Call the function (for testing)
get_balance()
place_limit_order()
