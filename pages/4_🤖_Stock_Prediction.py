import streamlit as st
from pages.utils.model_train import (
    get_data, get_rolling_mean, get_differencing_order,
    scaling, evaluate_model, get_forecast, inverse_scaling
)
import pandas as pd
from pages.utils.plotly_figure import plotly_table, Moving_average_forecast

# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="📈 Stock Prediction",
    page_icon="📉",
    layout="wide",
)

# -------------------- HEADER --------------------
st.markdown("<h1 style='text-align: center; color: #2E86C1;'>📊 Stock Price Prediction Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>Forecasting next 30 days closing prices using time-series modeling</p>", unsafe_allow_html=True)

# -------------------- STOCK SELECTION --------------------
popular_stocks = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "META", "NVDA", "NFLX", "BABA", "JPM"]

col1, col2, col3 = st.columns([1.5, 1, 1])

with col1:
    ticker = st.selectbox("Select Stock Ticker", popular_stocks, index=0)

with col2:
    st.info("Model: ARIMA + Moving Average")

with col3:
    st.info("Forecast Horizon: 30 days")

# -------------------- MODEL EXECUTION --------------------
st.subheader(f'📌 Predicting Next 30 Days Close Price for: **{ticker}**')

close_price = get_data(ticker)
rolling_price = get_rolling_mean(close_price)

differencing_order = get_differencing_order(rolling_price)
scaled_data, scaler = scaling(rolling_price)
rmse = evaluate_model(scaled_data, differencing_order)

# -------------------- METRIC DISPLAY --------------------
st.metric("Model RMSE Score", f"{rmse:.4f}", help="Lower RMSE indicates better model accuracy.")

forecast = get_forecast(scaled_data, differencing_order)
forecast['Close'] = inverse_scaling(scaler, forecast['Close'])

# -------------------- FORECAST DATA TABLE --------------------
st.markdown("### 📜 Forecast Data (Next 30 Days)")
fig_tail = plotly_table(forecast.sort_index(ascending=True).round(3))
fig_tail.update_layout(height=300)
st.plotly_chart(fig_tail, use_container_width=True)

# -------------------- PLOT FORECAST --------------------
forecast_full = pd.concat([rolling_price, forecast])
st.markdown("### 📈 Moving Average Forecast Trend")
st.plotly_chart(Moving_average_forecast(forecast_full.iloc[150:]), use_container_width=True)

# -------------------- RESULT EXPLANATION --------------------
st.markdown("---")
st.markdown("## 🧠 Interpretation & Insights")

st.markdown(f"""
- **Stock Selected:** {ticker}  
- **Forecast Horizon:** 30 trading days ahead  
- **Model RMSE Score:** `{rmse:.4f}`  
    - RMSE measures prediction error — lower values mean more accurate forecasts.
- **Forecast Data Table:** Shows the predicted daily closing prices for the next month.
- **Moving Average Forecast Chart:** Displays the smoothed historical trend with predicted future prices.
- **Practical Use:**  
    - Identify potential upward or downward momentum.  
    - Plan buy/sell decisions based on predicted patterns.  
    - Use RMSE to compare this forecast with alternative models for better accuracy.
""")

st.info("⚠ Forecasts are based on historical price patterns. They do not guarantee future performance and should be combined with fundamental and market analysis before making investment decisions.")
