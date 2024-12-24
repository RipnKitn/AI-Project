from flask import Flask, request

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    # Capture the incoming data from the webhook
    data = request.get_json()
    print("Received data:", data)  # Log it to the terminal

    # Respond to acknowledge receipt
    return "Webhook received!", 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
