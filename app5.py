from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv

# Load API credentials from .env file
load_dotenv()

API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')

app = Flask(__name__)

# Homepage route for GET requests
@app.route("/", methods=["GET"])
def home():
    return "Welcome to the Webhook Handler! Your Flask app is running."

# Webhook route for POST requests
@app.route("/webhook", methods=["POST"])
def webhook():
    if request.is_json:
        data = request.get_json()  # Extract JSON data from the POST request
        print("Received data:", data)  # For debugging, log the incoming data

        # Add your logic to handle the received data
        # Example: process the data and execute actions (like buying crypto)

        return jsonify({"message": "Data received successfully!"}), 200
    else:
        return jsonify({"error": "Invalid input, expected JSON."}), 400

if __name__ == "__main__":
    app.run(debug=True, port=5000)  # Run the app on port 5000
