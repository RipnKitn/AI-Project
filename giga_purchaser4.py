def place_giga_buy_order(size):
    try:
        endpoint = "/orders"
        url = f"{BASE_URL}{endpoint}"
        timestamp = str(int(time.time()))

        # GIGA-USDC order payload
        body = {
            "product_id": "GIGA-USDC",
            "side": "buy",
            "order_configuration": {
                "market_market_ioc": {
                    "quote_size": size  # Trade size in USDC
                }
            },
            "client_order_id": f"order-{int(time.time())}"  # Unique ID
        }
        body_json = json.dumps(body)

        # Generate signature
        signature = generate_signature(endpoint, body_json, timestamp)

        # API request headers
        headers = {
            "CB-ACCESS-KEY": API_KEY,
            "CB-ACCESS-SIGN": signature,
            "CB-ACCESS-TIMESTAMP": timestamp,
            "Content-Type": "application/json"
        }

        # Print the request for debugging
        print("URL:", url)
        print("Headers:", headers)
        print("Body:", body_json)

        # Make the API request
        response = requests.post(url, headers=headers, data=body_json)

        # Print the response for debugging
        print("Response Status Code:", response.status_code)
        print("Response Body:", response.text)

        return response.json()

    except Exception as e:
        return {"error": f"Failed to place order: {str(e)}"}
