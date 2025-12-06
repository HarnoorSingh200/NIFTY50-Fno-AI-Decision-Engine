## 🤖 NIFTY50-FnO-AI-Decision-Engine: Real-Time Algorithmic Trading System

---

### **Overview** 🚀

The **NIFTY50-FnO-AI-Decision-Engine** is a high-frequency, real-time algorithmic trading pipeline designed to execute trades on the National Stock Exchange (NSE) Futures & Options (F&O) segment for the NIFTY 50 index.

This project integrates a **Finvasia Shoonya API** for market data and order execution with a **Large Language Model (LLM)** via the **OpenAI Assistant API** to generate minute-by-minute trading decisions. It showcases a robust, low-latency system capable of automated financial market operations.

---

### **Key Features** ✨

* **Real-Time Data Pipeline:** Fetches and processes **live NIFTY 50** spot data and **At-The-Money (ATM)** option chain data (Call/Put premiums) every minute.
* **Finvasia Shoonya Integration:** Uses the official API for secure login, market data retrieval (quotes, time-series candles), and market order placement/exit.
* **AI-Driven Decision Making:** A custom-trained **OpenAI Assistant** analyzes the market data (including 1-minute candlestick charts and option premiums) to determine the optimal action: `buy_call_option`, `buy_put_option`, `exit_option`, or `wait_and_watch`.
* **Automated Trade Execution:** Executes market orders (buy/sell) for NIFTY FnO options based on the AI's recommendations.
* **Position Management:** Tracks open positions, calculates real-time Profit & Loss (P&L), and manages potential reversals (e.g., exiting a Put to enter a Call).
* **Time-Synchronous Operations:** Employs a precise `wait_for_next()` function to ensure the trading cycle aligns exactly with the start of every minute for high-frequency strategy implementation.

---

### **Technology Stack** 🛠️

| Category | Component | Description |
| :--- | :--- | :--- |
| **Language** | Python 3.x | Core programming language for the engine. |
| **Trading API** | Finvasia Shoonya API (via `NorenRestApiPy`) | Used for market connectivity, data feeds, and order execution. |
| **AI/ML** | OpenAI Assistant API (GPT-3.5/4) | The core decision-making engine; customized for trading logic. |
| **Data Processing** | `pandas` | Efficient handling and filtering of large NFO symbol data files. |
| **Security/Auth** | `pyotp` | Implementation of Time-based One-Time Password (TOTP) for secure login. |
| **Environment** | `json`, `datetime`, `time` | Modules for data serialization, time synchronization, and program flow control. |

---

### **System Architecture** 🏗️

The system operates in a continuous loop, executing a precise workflow every minute:

1.  **Initialization:** Establish a connection with the Finvasia Shoonya API and fetch the complete NFO symbol master data.
2.  **Data Acquisition:** Every minute, fetch the current NIFTY spot price, calculate the **At-The-Money (ATM) strike price**, and retrieve the live premiums and 1-minute historical candles for the corresponding Call and Put options.
3.  **Position Update:** If a position is open, update its current premium and calculate the running P&L.
4.  **AI Decision Phase:** The structured market data (including P&L context) is sent to the **OpenAI Assistant**. The assistant returns an action (`buy_call_option`, `exit_put_option`, etc.).
5.  **Execution & Management:** The returned action is executed via the `BuyOption` or `ExitOption` functions, placing a market order through the Shoonya API. The position state is updated accordingly.
6.  **Synchronization:** The `wait_for_next()` function pauses the execution until the exact start of the next minute, ensuring the trading logic runs on a consistent, timely basis.

---

### **Installation and Setup** ⚙️

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/YourUsername/NIFTY50-Fno-AI-Decision-Engine.git](https://github.com/YourUsername/NIFTY50-Fno-AI-Decision-Engine.git)
    cd NIFTY50-Fno-AI-Decision-Engine
    ```
2.  **Install Dependencies:**
    ```bash
    pip install NorenRestApiPy pyotp openai pandas requests
    ```
3.  **API Key Configuration:**
    Create a file named `keys.py` and populate it with your confidential API keys:
    ```python
    # keys.py
    openaikey = "YOUR_OPENAI_API_KEY"
    ```
    Update the `Login()` function in your `login.py` file with your Finvasia Shoonya credentials:
    ```python
    # login.py
    def Login():
        user = 'YOUR_USER_ID'
        pwd = 'YOUR_PASSWORD'
        factor2 = 'YOUR_TOTP_SECRET_KEY'
        # ... other credentials ...
    ```
4.  **OpenAI Assistant Setup:**
    You must pre-create an Assistant in the OpenAI playground with your desired trading strategy prompt and ensure its ID is added to the `main.py` file:
    ```python
    # main.py
    assistant_id = "asst_xxxxxxxxxxxxxxxxxxxxxxxxxxx" # <--- YOUR ASSISTANT ID HERE
    ```
5.  **Run the Engine:**
    ```bash
    python main.py
    ```

---

### **Future Enhancements** 💡

* **Risk Management Module:** Implement automated Stop-Loss (SL) and Target Profit (TP) orders.
* **Websocket Integration:** Switch from polling (`get_quotes`) to live data streaming via WebSockets for sub-second latency.
* **Tool Complexity:** Enhance the LLM's toolset with functions for dynamic strike price selection (e.g., slightly Out-of-the-Money).
* **Backtesting & Simulation:** Develop a module to simulate the trading logic against historical data to evaluate performance metrics (Sharpe Ratio, Max Drawdown).

---


### **Disclaimer** ⚠️

> **This project is for educational and portfolio demonstration purposes only.**
>
> **It is NOT intended for real-world production trading.** The author is not a financial advisor. All code provided here is based on technical logic and AI models, which are prone to errors and market unpredictability.
>
> **Trading in Futures and Options carries a high level of risk.** By using or adapting this code, you acknowledge and accept that you are solely responsible for any financial outcomes, losses, or gains that may result. **DO NOT** trade with capital you cannot afford to lose. Use this system only in a paper trading or simulation environment.

