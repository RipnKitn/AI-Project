import json

def load_parameters(file_path="parameters.json"):
    """Load trading parameters from parameters.json."""
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: {file_path} not found.")
        return {}
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in {file_path}.")
        return {}

def calculate_buy_amount(wallet, price, params):
    """
    Calculate the buy amount based on wallet balance and parameters.

    Args:
        wallet (dict): Wallet balances.
        price (float): Current price of the coin.
        params (dict): Parameters loaded from parameters.json.

    Returns:
        float: Amount to buy in terms of the pair coin (e.g., USDC).
    """
    mode = params.get("mode", "%")  # "%" or "$"
    buy_percent = params.get("buy_%", 0)
    buy_value = params.get("buy_$", 0)
    source = params.get("buy% from", "P")  # "C" (coin) or "P" (pair)

    if mode == "%":
        if source == "P":
            # Percentage of pair balance
            return wallet.get("pair", 0) * (buy_percent / 100)
        elif source == "C":
            # Percentage of coin balance converted to pair value
            return wallet.get("coin", 0) * (buy_percent / 100) * price
    elif mode == "$":
        # Flat dollar amount
        return buy_value
    return 0

def calculate_sell_amount(wallet, price, params):
    """
    Calculate the sell amount based on wallet balance and parameters.

    Args:
        wallet (dict): Wallet balances.
        price (float): Current price of the coin.
        params (dict): Parameters loaded from parameters.json.

    Returns:
        float: Amount to sell in terms of the coin (e.g., GIGA).
    """
    mode = params.get("mode", "%")  # "%" or "$"
    sell_percent = params.get("sell_%", 0)
    sell_value = params.get("sell_$", 0)
    source = params.get("sell% from", "C")  # "C" (coin) or "P" (pair)

    if mode == "%":
        if source == "C":
            # Percentage of coin balance
            return wallet.get("coin", 0) * (sell_percent / 100)
        elif source == "P":
            # Percentage of pair balance converted to coin value
            return (wallet.get("pair", 0) * (sell_percent / 100)) / price
    elif mode == "$":
        # Flat dollar amount converted to coin value
        return sell_value / price
    return 0

# Example Usage
if __name__ == "__main__":
    # Simulated wallet balances
    wallet = {"coin": 10, "pair": 100}  # 10 GIGA, 100 USDC
    current_price = 2.0  # 1 GIGA = 2 USDC

    # Load parameters
    parameters = load_parameters()

    # Calculate buy and sell amounts
    buy_amount = calculate_buy_amount(wallet, current_price, parameters)
    sell_amount = calculate_sell_amount(wallet, current_price, parameters)

    print(f"Buy Amount (USDC): {buy_amount}")
    print(f"Sell Amount (GIGA): {sell_amount}")
