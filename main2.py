import ccxt

# Set up Coinbase Advanced Trade connection
exchange = ccxt.coinbase({
    'apiKey': 'organizations/1073f4e6-52f3-49e4-b7e4-e2bd34261c51/apiKeys/ac613607-d810-41d4-9196-48c14ab0f8d0',
    'secret': '''-----BEGIN EC PRIVATE KEY-----
MHcCAQEEID8afQ5/asXPaRoupSmKxu71KzAAs5xjGsvQ3HoF2xdUoAoGCCqGSM49
AwEHoUQDQgAEUjZHnfp6pU4hFnf6SEm89Q8SiIF9aAldefKNdKrHbpzTIpe8uROG
1vcvhdnAFC7IA5otSktGGAje1XPWj2hcLg==
-----END EC PRIVATE KEY-----''',
})

# Test connection to fetch account balance
try:
    balance = exchange.fetch_balance()
    print("Balance:", balance)
except Exception as e:
    print("Error connecting to Coinbase:", e)
