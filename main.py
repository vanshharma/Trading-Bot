import sys
import json
from bot import BasicBot

def print_json(data):
    print(json.dumps(data, indent=4, default=str))

def get_valid_float(prompt):
    while True:
        try:
            value = float(input(prompt))
            if value <= 0:
                print("Value must be positive.")
                continue
            return value
        except ValueError:
            print("Invalid input. Please enter a number.")

def get_valid_side():
    while True:
        side = input("Enter Side (BUY/SELL): ").upper()
        if side in ['BUY', 'SELL']:
            return side
        print("Invalid side. Please enter 'BUY' or 'SELL'.")

def main():
    print("Initializing Binance Futures Testnet Bot...")
    
    use_sim = input("Run in Simulation Mode? (y/n): ").lower() == 'y'
    
    try:
        if use_sim:
            from bot import MockBot
            bot = MockBot()
        else:
            bot = BasicBot()
    except ValueError as e:
        print(f"Error: {e}")
        return

    while True:
        print("\n--- Main Menu ---")
        print("1. Check Connection")
        print("2. Place Market Order")
        print("3. Place Limit Order")
        print("4. Exit")
        
        choice = input("Enter your choice (1-4): ")

        if choice == '1':
            bot.check_connection()
        
        elif choice == '2':
            symbol = input("Enter Symbol (e.g., BTCUSDT): ").upper()
            side = get_valid_side()
            quantity = get_valid_float("Enter Quantity: ")
            
            print(f"\nPlacing MARKET {side} order for {quantity} {symbol}...")
            response = bot.place_market_order(symbol, side, quantity)
            print_json(response)

        elif choice == '3':
            symbol = input("Enter Symbol (e.g., BTCUSDT): ").upper()
            side = get_valid_side()
            quantity = get_valid_float("Enter Quantity: ")
            price = get_valid_float("Enter Price: ")
            
            print(f"\nPlacing LIMIT {side} order for {quantity} {symbol} at {price}...")
            response = bot.place_limit_order(symbol, side, quantity, price)
            print_json(response)

        elif choice == '4':
            print("Exiting...")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
