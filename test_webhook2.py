@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        # Print the raw request data for debugging
        print("Raw request data:", request.data)

        # Parse incoming JSON data
        data = request.get_json()
        print("Parsed JSON data:", data)

        # Extract values from JSON
        symbol = data.get("symbol", "")
        side = data.get("side", "")
        percentage = float(data.get("percentage", 1))

        # Debug: Print extracted values
        print(f"Symbol: {symbol}, Side: {side}, Percentage: {percentage}")

        # Call trade function
        result = place_trade(symbol, side, percentage)
        print("Trade Result:", result)

        return jsonify({"status": "success", "result": result}), 200

    except Exception as e:
        # Print and return error details
        print("Error:", str(e))
        return jsonify({"status": "error", "message": str(e)}), 400
