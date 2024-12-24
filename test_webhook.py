import requests

# Replace this with your actual Ngrok URL
webhook_url = "https://080e-204-144-212-76.ngrok-free.app/webhook"

# Example data to send
data = {"key": "test_value"}

# Send POST request
response = requests.post(webhook_url, json=data)

# Print response
print("Status Code:", response.status_code)
print("Response Text:", response.text)
