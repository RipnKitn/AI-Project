from flask import Flask, request

app = Flask(__name__)

@app.route("/", methods=["POST"])
def handle_webhook():
    data = request.json  # Get the data sent to this endpoint
    print("Received data:", data)
    return "Success", 200

if __name__ == "__main__":
    app.run(debug=True, port=5000)
