from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get API_KEY and API_SECRET from environment variables
API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')

print(API_KEY)
print(API_SECRET)
