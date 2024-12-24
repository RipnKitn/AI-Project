import json

def load_parameters(file_path="parameters.json"):
    """
    Load trading parameters from the specified JSON file.

    Args:
        file_path (str): Path to the parameters file.

    Returns:
        dict: Parameters dictionary.
    """
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return {}
    except json.JSONDecodeError:
        print(f"Error: The file {file_path} contains invalid JSON.")
        return {}

def calculate_buy_amount(params, wallet):
    """
    Calculate the amount to buy based on the mode and parameters.

    Args:
        params (dict): Parameters loaded from `parameters.json`.
        wallet (dict): Wallet balances, e.g., {"GIGA": 10, "USDC": 100}.

    Returns:
        float: Amount of coin to buy.
    """
    mode = params.get("mode", "$")
    coin = params.get("coin")
    pair = params.get("pair")
    
    if mode == "$":
        # Buy based on dollar amount
        buy_amount = params.get("buy_$", 0)
        return buy_amount / wallet.get(f"{coin}-{pair}-price", 1)  # Price fetched externally
    elif mode == "%":
        # Buy based on percentage
        source = params.get("buy% from", "C")
        if source == "C":
            return wallet.get(coin, 0) * (params.get("buy_%", 0) / 100)
        elif source == "P":
            return wallet.get(pair, 0) * (params.get("buy_%", 0) / 100)
    return 0

def calculate_sell_amount(params, wallet):
    """
    Calculate the amount to sell based on the mode and parameters.

    Args:
        params (dict): Parameters loaded from `parameters.json`.
        wallet (dict): Wallet balances, e.g., {"GIGA": 10, "USDC": 100}.

    Returns:
        float: Amount of coin to sell.
    """
    mode = params.get("mode", "$")
    coin = params.get("coin")
    pair = params.get("pair")
    
    if mode == "$":
        # Sell based on dollar amount
        sell_amount = params.get("sell_$", 0)
        return sell_amount / wallet.get(f"{coin}-{pair}-price", 1)  # Price fetched externally
    elif mode == "%":
        # Sell based on percentage
        source = params.get("sell% from", "C")
        if source == "C":
            return wallet.get(coin, 0) * (params.get("sell_%", 0) / 100)
        elif source == "P":
            return wallet.get(pair, 0) * (params.get("sell_%", 0) / 100)
    return 0

# Example usage
if __name__ == "__main__":
    # Example wallet and parameters for testing
    wallet = {"GIGA": 10, "USDC": 100, "GIGA-USDC-price": 0.5}
    params = load_parameters("parameters.json")
    
    buy_amount = calculate_buy_amount(params, wallet)
    sell_amount = calculate_sell_amount(params, wallet)
    
    print(f"Calculated buy amount: {buy_amount} {params.get('coin')}")
    print(f"Calculated sell amount: {sell_amount} {params.get('coin')}")
