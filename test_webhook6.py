import requests

url = "https://your-ngrok-url/webhook"  # Replace this with your actual Ngrok URL
payload = {
    "symbol": "GIGA-USDC",
    "side": "buy"
}
headers = {
    "Content-Type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)

print("Status Code:", response.status_code)
print("Response Body:", response.json())
