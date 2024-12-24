from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json  # Get the incoming JSON data
    print(data)  # Print the data to check
    return jsonify({"status": "success", "message": "Received data!"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
