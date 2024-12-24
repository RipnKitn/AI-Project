import requests

url = "http://127.0.0.1:8080/webhook"

headers = {"Content-Type": "application/json"}

payload = {
    "symbol": "ETH-USD",  # Trading pair
    "side": "buy",        # Action: "buy" or "sell"
    "percentage": 10      # % of balance to trade
}

try:
    response = requests.post(url, json=payload, headers=headers)
    print("Response Status:", response.status_code)
    print("Response Body:", response.json())
except Exception as e:
    print(f"Error: {e}")
