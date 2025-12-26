import os
import logging
from decimal import Decimal, ROUND_DOWN
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
    def __init__(self, api_key=None, api_secret=None):
        self.api_key = api_key or os.getenv("BINANCE_TESTNET_API_KEY")
        self.api_secret = api_secret or os.getenv("BINANCE_TESTNET_SECRET_KEY")
        
        if not self.api_key or not self.api_secret:
            logger.error("API credentials not found in .env file or arguments")
            raise ValueError("API credentials not found in .env file or arguments")

        # Initialize the Client for Testnet
        self.client = Client(self.api_key, self.api_secret, testnet=True)
        logger.info("Binance Client initialized in Testnet mode")
        print("⚠️ RUNNING ON TESTNET")

    def check_connection(self):
        try:
            server_time = self.client.futures_time()
            logger.info(f"Connected to Binance Futures Testnet. Server time: {server_time}")
            print(f"Connected to Binance Futures Testnet. Server time: {server_time}")
        except Exception as e:
            logger.error(f"Error connecting to Binance Futures Testnet: {e}")
            print(f"Error connecting to Binance Futures Testnet: {e}")

    def get_symbol_precision(self, symbol):
        try:
            info = self.client.futures_exchange_info()
            for item in info['symbols']:
                if item['symbol'] == symbol:
                    step_size = None
                    tick_size = None
                    for filter in item['filters']:
                        if filter['filterType'] == 'LOT_SIZE':
                            step_size = filter['stepSize']
                        if filter['filterType'] == 'PRICE_FILTER':
                            tick_size = filter['tickSize']
                    return step_size, tick_size
            return None, None
        except Exception as e:
            logger.error(f"Error fetching symbol precision: {e}")
            return None, None

    def _round_down(self, value, step):
        if not step:
            return value
        value = Decimal(str(value))
        step = Decimal(str(step))
        return float(value.quantize(step, rounding=ROUND_DOWN))

    def place_market_order(self, symbol, side, quantity):
        try:
            step_size, _ = self.get_symbol_precision(symbol)
            if step_size:
                quantity = self._round_down(quantity, step_size)
                logger.info(f"Adjusted quantity to {quantity} based on stepSize {step_size}")

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
            step_size, tick_size = self.get_symbol_precision(symbol)
            if step_size:
                quantity = self._round_down(quantity, step_size)
            if tick_size:
                price = self._round_down(price, tick_size)
            
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
