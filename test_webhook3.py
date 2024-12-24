import requests

url = "http://127.0.0.1:8080/webhook"
headers = {"Content-Type": "application/json"}
payload = {
    "symbol": "ETH-USD",
    "side": "buy",
    "percentage": 10
}

response = requests.post(url, json=payload, headers=headers)

print("Response Status:", response.status_code)
print("Response Body:", response.json())
