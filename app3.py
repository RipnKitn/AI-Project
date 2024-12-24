from flask import Flask
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

@app.route('/')
def home():
    return "Webhook Handler is Running!"

# Start Flask app
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
