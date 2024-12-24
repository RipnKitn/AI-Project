import requests

# Replace with your ngrok forwarding URL
url = "https://080e-204-144-212-76.ngrok-free.app/webhook"

# Test data to send
data = {
    "test": "new_webhook_test",
    "status": "success"
}

# Send a POST request
response = requests.post(url, json=data)

# Print the response
print("Status Code:", response.status_code)
print("Response Text:", response.text)
