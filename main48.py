from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json  # Receive the POST data
    print("Received data:", data)

    # Extract required parameters
    symbol = data.get('symbol')
    side = data.get('side')
    quantity = data.get('quantity')

    # Mock response for now
    if symbol and side and quantity:
        response = {
            "message": "Trade executed successfully!",
            "symbol": symbol,
            "side": side,
            "quantity": quantity
        }
        print("Trading Details:", response)
        return jsonify(response), 200
    else:
        return jsonify({"error": "Missing parameters!"}), 400

if __name__ == '__main__':
    app.run(debug=True, port=80)
