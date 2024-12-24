from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

# Retrieve API info
API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')

# Print API key and secret
print(f"API_KEY: {API_KEY}")
print(f"API_SECRET: {API_SECRET}")
