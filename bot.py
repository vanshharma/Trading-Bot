import os
import logging
from binance.client import Client
from binance.exceptions import BinanceAPIException
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class BasicBot:
    def __init__(self):
        api_key = os.getenv("BINANCE_TESTNET_API_KEY")
        api_secret = os.getenv("BINANCE_TESTNET_SECRET_KEY")
        
        if not api_key or not api_secret:
            logger.error("API credentials not found in .env file")
            raise ValueError("API credentials not found in .env file")

        # Initialize the Client for Testnet
        self.client = Client(api_key, api_secret, testnet=True)
        logger.info("Binance Client initialized in Testnet mode")

    def check_connection(self):
        try:
            server_time = self.client.get_server_time()
            logger.info(f"Connected to Binance Futures Testnet. Server time: {server_time}")
            print(f"Connected to Binance Futures Testnet. Server time: {server_time}")
        except Exception as e:
            logger.error(f"Error connecting to Binance Futures Testnet: {e}")
            print(f"Error connecting to Binance Futures Testnet: {e}")

    def place_market_order(self, symbol, side, quantity):
        try:
            logger.info(f"Placing MARKET {side} order for {quantity} {symbol}")
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type='MARKET',
                quantity=quantity
            )
            logger.info(f"Market order placed successfully: {order}")
            return order
        except BinanceAPIException as e:
            logger.error(f"Binance API Exception placing market order: {e}")
            return {"error": str(e)}
        except Exception as e:
            logger.error(f"Unexpected error placing market order: {e}")
            return {"error": str(e)}

    def place_limit_order(self, symbol, side, quantity, price):
        try:
            logger.info(f"Placing LIMIT {side} order for {quantity} {symbol} at {price}")
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type='LIMIT',
                timeInForce='GTC',
                quantity=quantity,
                price=price
            )
            logger.info(f"Limit order placed successfully: {order}")
            return order
        except BinanceAPIException as e:
            logger.error(f"Binance API Exception placing limit order: {e}")
            return {"error": str(e)}
        except Exception as e:
            logger.error(f"Unexpected error placing limit order: {e}")
            return {"error": str(e)}

if __name__ == "__main__":
    try:
        bot = BasicBot()
        bot.check_connection()
    except ValueError as e:
        print(e)
