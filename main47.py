from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os

app = Flask(__name__)

# Load environment variables
load_dotenv()
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")

@app.route("/", methods=["GET"])
def home():
    return "Flask server is running!"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json  # Get incoming JSON data
    print("Webhook Data:", data)
    return jsonify({"status": "success", "message": "Webhook received!"})

if __name__ == "__main__":
    app.run(port=80, debug=True)
