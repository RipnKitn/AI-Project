import json
from flask import Flask, request
from giga_purchaser import place_giga_buy_order

app = Flask(__name__)

# Handle incoming webhook to trigger the purchase
@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        # Get the data from the webhook request
        data = request.json
        print("Received webhook data:", data)

        # Check for the necessary 'size' key
        if "size" in data:
            size = data["size"]
            print(f"Trade size: {size}")

            # Place the order with the extracted size
            result = place_giga_buy_order(size)

            # Return the result of the API request
            return json.dumps(result), 200
        else:
            return json.dumps({"error": "Missing 'size' in webhook data"}), 400
    except Exception as e:
        return json.dumps({"error": f"Webhook processing error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
