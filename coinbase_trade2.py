from coinbase_advanced_trader.enhanced_rest_client import EnhancedRESTClient

# Your API key and secret (correctly placed here)
api_key = "organizations/{org_id}/apiKeys/7e23b2c4-f91d-47db-bc56-35775be759aa"  # API Key
api_secret = """-----BEGIN EC PRIVATE KEY-----
MHcCAQEEIEajBK7ysPzoNM3v79sYdyzcaN9VH9eWi7PUeZF1k5CdoAoGCCqGSM49
AwEHoUQDQgAEo8k64SDokeG8dlwpuyTCJau0AhxAWfh/hML9UEdrEAxmD5WEYp+B
O89GXmvpw598CtdSSZmp02IQyMp3cOa5YA==
-----END EC PRIVATE KEY-----"""  # API Secret

client = EnhancedRESTClient(api_key=api_key, api_secret=api_secret)

# Step 1: Get and print balances
balances = client.list_held_crypto_balances()
print("Balances:", balances)

# Step 2: Place a $1 market buy order for GIGA/USDC
response = client.fiat_market_buy("GIGA-USDC", "1")
print("Buy Order Response:", response)
