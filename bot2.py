from flask import Flask, request, jsonify
from coinbase import jwt_generator
import requests
import time

app = Flask(__name__)

# API Credentials (replace with your own)
API_KEY = "organizations/{org_id}/apiKeys/{key_id}"
API_SECRET = """-----BEGIN EC PRIVATE KEY-----
YOUR PRIVATE KEY
-----END EC PRIVATE KEY-----
"""

# Generate JWT for requests
def generate_jwt(method, path):
    jwt_uri = jwt_generator.format_jwt_uri(method, path)
    return jwt_generator.build_rest_jwt(jwt_uri, API_KEY, API_SECRET)

# Place a trade
@app.route('/trade', methods=['POST'])
def trade():
    data = request.json
    symbol = data.get("symbol", "BTC-USD")
    side = data.get("side", "buy")
    size = data.get("size", "0.001")  # Example: 0.001 BTC

    try:
        jwt_token = generate_jwt("POST", "/api/v3/brokerage/orders")
        headers = {"Authorization": f"Bearer {jwt_token}"}

        payload = {
            "product_id": symbol,
            "side": side,
            "order_configuration": {
                "market_market_ioc": {
                    "quote_size": size
                }
            },
            "client_order_id": str(int(time.time()))
        }

        response = requests.post("https://api.coinbase.com/api/v3/brokerage/orders", json=payload, headers=headers)
        return jsonify(response.json())

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
