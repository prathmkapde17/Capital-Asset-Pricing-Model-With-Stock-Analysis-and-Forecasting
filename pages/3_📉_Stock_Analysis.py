import streamlit as st
import pandas as pd
import yfinance as yf
import datetime
from pages.utils.plotly_figure import plotly_table, close_chart, candlestick, RSI, Moving_average, MACD

# Page config
st.set_page_config(
    page_title="Stock Analysis",
    page_icon="📈",
    layout="wide"
)

# ----------------- CUSTOM STYLES -----------------
st.markdown("""
<style>
/* Main page background */
.stApp {
    background-color: #f8f9fa;
}

/* Headings */
h1, h2, h3, h4 {
    color: #1f4e79;
    font-weight: bold;
}

/* Metric cards */
[data-testid="stMetric"] {
    background: white;
    padding: 15px;
    border-radius: 12px;
    box-shadow: 0px 2px 8px rgba(0,0,0,0.05);
}

/* Dataframe tables */
.stDataFrame {
    background-color: white;
    border-radius: 10px;
    padding: 10px;
}

/* Selectboxes */
.stSelectbox {
    background: white;
    border-radius: 8px;
}

/* Section separators */
hr {
    border: 1px solid #ccc;
}
</style>
""", unsafe_allow_html=True)

# --- Header ---
st.title("📊 Stock Analysis Dashboard")
st.markdown("Analyze stock fundamentals, trends, and technical indicators in one interactive view.")

# --- Stock Selector ---
popular_stocks = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "META", "NVDA", "NFLX", "BABA", "JPM"]
col1, col2, col3 = st.columns(3)

with col1:
    ticker = st.selectbox("Select Stock Ticker", popular_stocks, index=0)
with col2:
    start_date = st.date_input("Start Date", datetime.date.today() - datetime.timedelta(days=365))
with col3:
    end_date = st.date_input("End Date", datetime.date.today())

# --- Company Info ---
stock = yf.Ticker(ticker)
info = stock.info

st.subheader(f"📄 {ticker} — {info.get('longName', 'N/A')}")
st.write(info.get('longBusinessSummary', 'No summary available.'))

col1, col2, col3 = st.columns(3)
col1.metric("Sector", info.get("sector", "N/A"))
col2.metric("Employees", info.get("fullTimeEmployees", "N/A"))
col3.markdown(f"[🌐 Company Website]({info.get('website', '#')})")

# --- Key Stats ---
col1, col2 = st.columns(2)

with col1:
    df1 = pd.DataFrame({
        "Metric": ["Market Cap", "Beta", "EPS", "PE Ratio"],
        "Value": [
            info.get("marketCap", "N/A"),
            info.get("beta", "N/A"),
            info.get("trailingEps", "N/A"),
            info.get("trailingPE", "N/A")
        ]
    })
    st.table(df1)

with col2:
    df2 = pd.DataFrame({
        "Metric": ["Quick Ratio", "Revenue/Share", "Profit Margins", "Debt/Equity", "Return on Equity"],
        "Value": [
            info.get("quickRatio", "N/A"),
            info.get("revenuePerShare", "N/A"),
            info.get("profitMargins", "N/A"),
            info.get("debtToEquity", "N/A"),
            info.get("returnOnEquity", "N/A")
        ]
    })
    st.table(df2)

# --- Price Data ---
data = yf.download(ticker, start=start_date, end=end_date)

if len(data) < 1:
    st.error("Invalid ticker or no data available.")
else:
    daily_change = data['Close'].iloc[-1] - data['Close'].iloc[-2]
    daily_pct = (daily_change / data['Close'].iloc[-2]) * 100
    col1, col2 = st.columns(2)
    col1.metric(
    "Daily Price", 
    f"${float(data['Close'].iloc[-1]):.2f}",  # <-- fixed here
    f"{(float(data['Close'].iloc[-1]) - float(data['Close'].iloc[-2])):.2f} "
    f"({((float(data['Close'].iloc[-1]) - float(data['Close'].iloc[-2])) / float(data['Close'].iloc[-2]) * 100):.2f}%)"
)


    # --- Historical Data Table ---
    st.write("### 📜 Historical Data (Last 10 Trading Days)")
    hist_df = data.tail(10).sort_index(ascending=False).round(2).reset_index()
    st.dataframe(hist_df, use_container_width=True)


# --- Chart Section ---
st.markdown("---")
st.subheader("📈 Price & Technical Analysis")

period_options = {
    "5D": "5d", "1M": "1mo", "6M": "6mo", "YTD": "ytd",
    "1Y": "1y", "5Y": "5y", "MAX": "max"
}

# Three side-by-side columns for controls
col1, col2, col3 = st.columns(3)

with col1:
    selected_period = st.selectbox("Select Period", list(period_options.keys()), index=4)

with col2:
    chart_type = st.selectbox("Chart Type", ("Candle", "Line"))

with col3:
    if chart_type == "Candle":
        indicator = st.selectbox("Indicator", ("RSI", "MACD"))
    else:
        indicator = st.selectbox("Indicator", ("RSI", "Moving Average", "MACD"))

# Get data
period = period_options[selected_period]
ticker_data = stock.history(period=period)

# Chart logic
if chart_type == "Candle" and indicator == "RSI":
    st.plotly_chart(candlestick(ticker_data, period), use_container_width=True)
    st.plotly_chart(RSI(ticker_data, period), use_container_width=True)

elif chart_type == "Candle" and indicator == "MACD":
    st.plotly_chart(candlestick(ticker_data, period), use_container_width=True)
    st.plotly_chart(MACD(ticker_data, period), use_container_width=True)

elif chart_type == "Line" and indicator == "RSI":
    st.plotly_chart(close_chart(ticker_data, period), use_container_width=True)
    st.plotly_chart(RSI(ticker_data, period), use_container_width=True)

elif chart_type == "Line" and indicator == "Moving Average":
    st.plotly_chart(Moving_average(ticker_data, period), use_container_width=True)

elif chart_type == "Line" and indicator == "MACD":
    st.plotly_chart(close_chart(ticker_data, period), use_container_width=True)
    st.plotly_chart(MACD(ticker_data, period), use_container_width=True)

# --- Insights ---
st.write("### 📌 Insights")

# ---- Beta Analysis ----
beta_val = info.get("beta", None)
if beta_val is not None:
    if beta_val == 0:
        st.markdown(
            f"- **Beta = {beta_val:.2f}** → Essentially no sensitivity to market movements. "
            f"This means the stock's price changes are mostly driven by company-specific factors, "
            f"not overall market sentiment."
        )
    elif beta_val < 0:
        st.markdown(
            f"- **Beta = {beta_val:.2f}** → Negative correlation with the market. "
            f"When the market rises, this stock tends to fall, and vice versa. "
            f"This is rare and could indicate a strong defensive or hedging asset."
        )
    elif beta_val < 1:
        st.markdown(
            f"- **Beta = {beta_val:.2f}** → Less volatile than the market. "
            f"Tends to move in the same direction as the market but with smaller swings. "
            f"Suitable for conservative investors seeking stability with moderate growth."
        )
    elif beta_val == 1:
        st.markdown(
            f"- **Beta = {beta_val:.2f}** → Moves almost exactly in line with the market. "
            f"Offers no volatility advantage or disadvantage—risk mirrors overall market risk."
        )
    else:
        st.markdown(
            f"- **Beta = {beta_val:.2f}** → More volatile than the market. "
            f"Tends to amplify market moves—rising more in bull markets but also falling more in bear markets. "
            f"Suitable for aggressive investors seeking higher returns but willing to accept greater risk."
        )
else:
    st.markdown("- **Beta data unavailable** → Unable to assess market sensitivity.")

# ---- Return on Equity (ROE) Analysis ----
if "returnOnEquity" in info and info["returnOnEquity"] is not None:
    roe = info["returnOnEquity"] * 100
    if roe > 20:
        st.markdown(
            f"- **ROE = {roe:.2f}%** → Exceptional profitability. "
            f"The company is highly efficient in generating returns from shareholders' equity—"
            f"often a sign of strong management and competitive advantage."
        )
    elif roe > 15:
        st.markdown(
            f"- **ROE = {roe:.2f}%** → Strong profitability. "
            f"Indicates the company generates healthy returns on equity compared to industry norms."
        )
    elif roe > 10:
        st.markdown(
            f"- **ROE = {roe:.2f}%** → Moderate profitability. "
            f"Reasonable performance, but there may be room for operational improvement."
        )
    elif roe > 5:
        st.markdown(
            f"- **ROE = {roe:.2f}%** → Below-average profitability. "
            f"May indicate inefficiencies, weaker margins, or heavy reinvestment periods."
        )
    else:
        st.markdown(
            f"- **ROE = {roe:.2f}%** → Weak profitability. "
            f"Suggests difficulty in generating returns from equity, possibly due to high costs, "
            f"low margins, or industry headwinds."
        )
else:
    st.markdown("- **ROE data unavailable** → Unable to assess profitability.")
