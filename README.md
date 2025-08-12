# 📊 Capital Asset Pricing Model (CAPM) with Stock Analysis & Forecasting

A powerful Streamlit-based dashboard for traders and investors to **analyze stocks, calculate CAPM Beta & returns, evaluate technical indicators, and forecast future prices** — all in one place.

---

## 🌟 Features

### 1. CAPM Beta & Expected Return
- Calculate **Beta** for a selected stock vs. market (S&P 500 or chosen index).
- Compute **expected return** using the Capital Asset Pricing Model.
- Visualize **scatter plots** of daily returns vs. market returns.
- Compare **risk & performance** across multiple stocks in table format.

### 2. Stock Analysis Dashboard
- View **fundamentals**: Market Cap, EPS, P/E Ratio, ROE, etc.
- Inspect **price & volume trends**.
- Access **historical data tables** with head/tail preview.
- Compare raw vs normalized price charts for multiple stocks.

### 3. Technical Analysis
- Interactive **candlestick charts**.
- **RSI (Relative Strength Index)** to detect overbought/oversold levels.
- Volatility and trend indicators.
- Actionable **insights & interpretation**.

### 4. Stock Price Forecasting
- Forecast **next 30 days’ closing prices** using ARIMA & Moving Average models.
- Display **predicted vs historical trends**.
- Show **RMSE scores** for model accuracy.
- Forecast table with date-wise predictions.

---

## 🖥️ User Interface

- **Sidebar Navigation**: Quick access to each feature (CAPM Beta, CAPM Return, Analysis, Prediction).
- **Dropdowns**: Select tickers, time periods, forecast horizons, and index comparisons.
- **Real-Time Charts**: Plotly/Matplotlib visualizations for accurate insights.
- **Insights Pane**: Displays interpretations for users without heavy finance knowledge.

---

## 🚀 Getting Started

### 1️⃣ Clone the Repository
git clone https://github.com/prathmkapde17/Capital-Asset-Pricing-Model-With-Stock-Analysis-and-Forecasting.git
cd Capital-Asset-Pricing-Model-With-Stock-Analysis-and-Forecasting

text

### 2️⃣ Install Dependencies
Make sure you have **Python 3.8+**.

pip install -r requirements.txt

text

**Key Libraries**:
streamlit
pandas
numpy
matplotlib
seaborn
plotly
yfinance
statsmodels
scikit-learn

text

### 3️⃣ Run the Application
streamlit run app.py

text
> Replace `app.py` with your main Streamlit file if different.

---

## 📂 Project Structure

├── app.py # Main Streamlit dashboard
├── capm.py # Functions for CAPM Beta & return calculation
├── analysis.py # Stock analysis logic
├── forecasting.py # Price forecasting models (ARIMA, moving average)
├── requirements.txt # Python dependencies
├── assets/ # Static images / screenshots
├── README.md # Project documentation

text

---

## 📊 Sample Outputs

| Feature | Example Output |
|---------|----------------|
| CAPM Scatter | ![Beta Plot](assets/capm_scatter.png) |
| Stock Comparison | ![Stock Comparison](assets/stock_comparison.png) |
| RSI Chart | ![RSI](assets/rsi_chart.png) |
| Forecast Table | ![Forecast](assets/forecast_table.png) |

*(Place actual screenshots inside the `assets/` folder to display correctly on GitHub.)*

---

## 🧠 How It Works

1. **CAPM**: Retrieves stock & index data via `yfinance`, computes daily returns, Beta via regression, and expected return with CAPM formula.
2. **Stock Analysis**: Uses APIs & historical data to display key financial metrics and charts.
3. **Technical Analysis**: Calculates and plots momentum indicators like RSI alongside candlestick patterns.
4. **Forecasting**: Fits an ARIMA model to closing prices, generates predicted values with error metrics.

---

## 💡 Usage Tips
- **High Beta (>1)**: Stock moves more than the market — volatile.
- **Low Beta (<1)**: Stock less volatile than the market.
- Combine **technical signals** (RSI, price movements) with **fundamentals** before making decisions.
- Forecasting is short-term — validate with other models for long-term strategy.

---

## ⚠️ Disclaimer
> This tool is for **educational and research purposes only**.  
> Forecasts & recommendations are **not financial advice** — always do your own research.

---

## 🛠 Future Improvements
- More technical indicators (`MACD`, `Bollinger Bands`, etc.).
- Real-time streaming data.
- Advanced ML models (`LSTM`, `Prophet`).
- Portfolio creation & backtesting features.

---

## 👤 Author
**Prathamesh Kapde**  
🔗 [GitHub](https://github.com/prathmkapde17)

---

## 📄 License
This project is licensed under the **MIT License** — free to use and modify.

---
