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

simulation_mode = st.sidebar.checkbox("Enable Simulation Mode", value=False)

if simulation_mode:
    st.sidebar.warning("Simulation Mode Active. No real trades will be placed.")
    api_key_input = None
    api_secret_input = None
else:
    st.sidebar.markdown("Enter your Testnet API Keys below (optional if set in .env).")
    api_key_input = st.sidebar.text_input("API Key", type="password")
    api_secret_input = st.sidebar.text_input("Secret Key", type="password")

# Initialize Bot
@st.cache_resource(show_spinner=False)
def get_bot(api_key, api_secret, is_sim):
    if is_sim:
        from bot import MockBot
        return MockBot()
    
    try:
        # Pass None if inputs are empty strings so it falls back to env vars
        key = api_key if api_key else None
        secret = api_secret if api_secret else None
        return BasicBot(key, secret)
    except Exception as e:
        return None

bot = get_bot(api_key_input, api_secret_input, simulation_mode)

if not bot:
    st.error("Failed to initialize bot. Please check your API keys in .env or the sidebar.")
    st.stop()

# Connection Status
st.subheader("Connection Status")
if st.button("Check Connection"):
    try:
        if simulation_mode:
             bot.check_connection() # Prints to console
             st.success("Connected to Simulated Server!")
        else:
            server_time = bot.client.futures_time()
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
            
            # Create a nice dashboard-style receipt
            st.markdown("### 🎫 Trade Receipt")
            
            # Row 1: Key Info
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Symbol", result.get('symbol', symbol))
            m2.metric("Side", result.get('side', side), delta="BUY" if result.get('side') == 'BUY' else "-SELL", delta_color="normal")
            m3.metric("Type", result.get('type', order_type))
            m4.metric("Status", result.get('status', 'UNKNOWN'))

            # Row 2: Details
            d1, d2, d3 = st.columns(3)
            d1.metric("Quantity", result.get('origQty', quantity))
            d2.metric("Price", result.get('price', price) if float(result.get('price', 0)) > 0 else "Market")
            d3.metric("Order ID", result.get('orderId', 'N/A'))

            # Raw JSON in an expander for debugging/technical review
            with st.expander("🔍 View Raw API Response (Technical Details)"):
                st.json(result)

st.divider()

# Logs / Info
st.info("Logs are being written to the console/terminal where you ran `streamlit run app.py`.")
