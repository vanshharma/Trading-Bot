import streamlit as st
import logging
from bot import BasicBot

# Configure logging to capture in UI (basic approach)
# For a real app, we might want to capture logs to a string buffer, 
# but for now we'll just display results directly.

st.set_page_config(page_title="Binance Futures Bot", page_icon="🤖", layout="wide")

st.title("🤖 Binance Futures Testnet Bot")

# Sidebar for Configuration
st.sidebar.header("Configuration")
st.sidebar.markdown("Enter your Testnet API Keys below (optional if set in .env).")

api_key_input = st.sidebar.text_input("API Key", type="password")
api_secret_input = st.sidebar.text_input("Secret Key", type="password")

# Initialize Bot
@st.cache_resource(show_spinner=False)
def get_bot(api_key, api_secret):
    try:
        # Pass None if inputs are empty strings so it falls back to env vars
        key = api_key if api_key else None
        secret = api_secret if api_secret else None
        return BasicBot(key, secret)
    except Exception as e:
        return None

bot = get_bot(api_key_input, api_secret_input)

if not bot:
    st.error("Failed to initialize bot. Please check your API keys in .env or the sidebar.")
    st.stop()

# Connection Status
st.subheader("Connection Status")
if st.button("Check Connection"):
    try:
        # We need to capture the output or return value. 
        # BasicBot.check_connection prints to stdout. 
        # Let's just call the client directly for the UI or modify BasicBot to return the time.
        # Since we can't easily change BasicBot return type without breaking other things potentially,
        # we'll just access the client here for the UI check or trust the logs.
        # Actually, let's just wrap it.
        server_time = bot.client.get_server_time()
        st.success(f"Connected! Server Time: {server_time['serverTime']}")
    except Exception as e:
        st.error(f"Connection failed: {e}")

st.divider()

# Order Placement
st.subheader("Place Order")

col1, col2 = st.columns(2)

with col1:
    symbol = st.text_input("Symbol", value="BTCUSDT").upper()
    side = st.selectbox("Side", ["BUY", "SELL"])

with col2:
    order_type = st.selectbox("Type", ["MARKET", "LIMIT"])
    quantity = st.number_input("Quantity", min_value=0.001, value=0.001, step=0.001, format="%.3f")

price = 0.0
if order_type == "LIMIT":
    price = st.number_input("Price", min_value=0.1, value=50000.0, step=10.0)

if st.button("Execute Order", type="primary"):
    with st.spinner("Placing order..."):
        result = None
        if order_type == "MARKET":
            result = bot.place_market_order(symbol, side, quantity)
        else:
            result = bot.place_limit_order(symbol, side, quantity, price)
        
        if "error" in result:
            st.error(f"Order Failed: {result['error']}")
        else:
            st.success("Order Placed Successfully!")
            st.json(result)

st.divider()

# Logs / Info
st.info("Logs are being written to the console/terminal where you ran `streamlit run app.py`.")
