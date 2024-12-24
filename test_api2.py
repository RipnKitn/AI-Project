from dotenv import load_dotenv
import os

# Load the .env file
load_dotenv()

# Retrieve the API credentials from the .env file
API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')

# Print the credentials to verify they're loaded correctly
print("API_KEY:", API_KEY)
print("API_SECRET:", API_SECRET)

# Check if they are loaded
if API_KEY and API_SECRET:
    print("Successfully loaded API credentials!")
else:
    print("Error: API credentials not loaded properly.")
