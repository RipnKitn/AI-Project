python main.py


ngrok http 80

ngrok http 8080

ngrok http 5000

https://080e-204-144-212-76.ngrok-free.app/

python test_webhook.py

python app.py

curl -X POST -H "Content-Type: application/json" -d "{\"secret\":\"your_secret_key_here\",\"action\":\"buy_giga\"}" http://127.0.0.1:5000/webhook

C:\Users\dylan\OneDrive\Desktop\AI Crypto\Code>curl -X POST -H "Content-Type: application/json" -d "{\"secret\":\"your_secret_key_here\",\"action\":\"buy_giga\"}" https://9b2c-204-144-212-76.ngrok-free.app/webhook --insecure
Dry run: Purchase triggered!
C:\Users\dylan\OneDrive\Desktop\AI Crypto\Code>

{
    "secret": "your_secret_key_here",
    "action": "buy_giga"
}

