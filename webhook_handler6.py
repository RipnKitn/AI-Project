from flask import Flask, request
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')

@app.route('/', methods=['POST'])
def webhook():
    data = request.json
    print(f"Received data: {data}")
    return "Success", 200

if __name__ == '__main__':
    app.run(debug=True)
