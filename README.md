# Binance Futures Testnet Trading Bot

## Project Overview
A robust, class-based Python trading bot designed for the Binance Futures Testnet, featuring a CLI and a Streamlit UI for easy interaction.

## Setup Instructions

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/vanshharma/Trading-Bot.git
    cd Trading-Bot
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure Environment:**
    Create a `.env` file in the root directory and add your Binance Testnet credentials:
    ```env
    BINANCE_TESTNET_API_KEY=your_api_key_here
    BINANCE_TESTNET_SECRET_KEY=your_secret_key_here
    ```

## Architecture
The project follows a modular design to ensure maintainability and scalability:
*   **`bot.py` (BasicBot Class):** Encapsulates all logic for interacting with the Binance API. It handles authentication, connection verification, order placement, and error handling. This separation allows the core logic to be reused across different interfaces.
*   **`main.py`:** Provides a command-line interface (CLI) for quick testing and interaction in a terminal environment.
*   **`app.py`:** Offers a user-friendly web interface using Streamlit for visual interaction and monitoring.

## Key Features
*   **Simulation Mode:** Includes a `MockBot` that simulates API responses, allowing users to test the UI and CLI logic without valid API keys.
*   **Precision & Step-Size Handling:** Automatically fetches exchange filters (`stepSize`, `tickSize`) and rounds order quantities and prices to prevent `APIError(code=-1111)`.
*   **Correct Futures Endpoints:** Strictly uses `futures_*` endpoints (e.g., `futures_create_order`, `futures_time`) to ensure compatibility with the Futures market, avoiding common Spot API mix-ups.
*   **Testnet Safety:** Explicitly flags Testnet usage to prevent accidental real-money trading.
*   **Robust Error Handling:** Comprehensive logging and try-except blocks to gracefully handle API exceptions.

## Usage Examples

### Command Line Interface (CLI)
Run the interactive terminal menu:
```bash
python main.py
```
You will be asked if you want to run in **Simulation Mode**. Type `y` to test without keys, or `n` to use real Testnet keys.

### Streamlit UI
Launch the web dashboard:
```bash
streamlit run app.py
```
Check the **"Enable Simulation Mode"** box in the sidebar to test the interface without API keys.
