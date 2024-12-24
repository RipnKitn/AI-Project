import requests
import json

# Define the public ngrok URL for your bot
NGROK_URL = "https://b464-204-144-212-76.ngrok-free.app/webhook"

# Define the payload to send (example: buy action)
payload = {
    "action": "buy"  # Change to "sell" to test selling
}

# Send the POST request
try:
    response = requests.post(NGROK_URL, json=payload)
    print(f"Status Code: {response.status_code}")
    print("Response:", response.json() if response.status_code == 200 else response.text)
except Exception as e:
    print(f"Error testing the bot: {e}")
