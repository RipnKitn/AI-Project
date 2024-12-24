import os
from dotenv import load_dotenv  # This will allow us to load the .env file
import cbpro  # Coinbase Pro API library

# Load the environment variables from the .env file
load_dotenv()

# Retrieve API Key and API Secret from environment variables
api_key = os.getenv('COINBASE_API_KEY')
api_secret = os.getenv('COINBASE_API_SECRET')

# Initialize the Coinbase Pro client (Advanced API) with your credentials
auth_client = cbpro.AuthenticatedClient(api_key, api_secret)

# Test if the connection works by getting account balances
def get_account_info():
    try:
        accounts = auth_client.get_accounts()  # Get account balances and information
        if accounts:
            print("Account Information:")
            for account in accounts:
                print(f"Currency: {account['currency']}, Balance: {account['balance']}")
        else:
            print("No account information available.")
    except Exception as e:
        print(f"Error getting account info: {e}")

# Call the function to print account information
get_account_info()
