# ---------------------- IMPORTS ----------------------
import streamlit as st
import pandas_datareader.data as web
import datetime
import pandas as pd
import yfinance as yf
from pages.utils import capm_functions
import plotly.express as px

# ---------------------- PAGE CONFIG ----------------------
st.set_page_config(
    page_title="CAPM - Multi Stock Beta & Return",
    page_icon="📊",
    layout="wide",
)

# ---------------------- HEADER ----------------------
st.markdown(
    """
    <h1 style="text-align:center; color:#1E88E5;">📈 Capital Asset Pricing Model - Multi Stock Analysis</h1>
    <p style="text-align:center; font-size:18px; color:#555;">
    Compare Beta & Expected Returns of multiple stocks against the market (S&P 500) using CAPM.
    </p>
    <hr style="height:2px; border:none; background-color:#1E88E5;">
    """,
    unsafe_allow_html=True
)

# ---------------------- USER INPUTS ----------------------
col1, col2 = st.columns(2)
with col1:
    stocks_list = st.multiselect(
        "📌 Choose Stocks by Ticker",
        ('TSLA', 'AAPL', 'NFLX', 'MGM', 'MSFT', 'AMZN', 'NVDA', 'GOOGL'),
        ['TSLA', 'AAPL', 'MSFT', 'NFLX'],
        key="stock_list"
    )
with col2:
    year = st.number_input("📅 Number of Years", min_value=1, max_value=10, value=5)

# ---------------------- DATA FETCHING & CALCULATIONS ----------------------
try:
    end = datetime.date.today()
    start = datetime.date(end.year - year, end.month, end.day)

    # Market Data (S&P 500)
    SP500 = web.DataReader(['sp500'], 'fred', start, end)
    SP500.reset_index(inplace=True)
    SP500.columns = ['Date', 'sp500']

    # Stock Price Data
    stocks_df = pd.DataFrame()
    for stock in stocks_list:
        data = yf.download(stock, period=f'{year}y')
        stocks_df[stock] = data['Close']
    stocks_df.reset_index(inplace=True)

    # Merge with Market Data
    stocks_df['Date'] = pd.to_datetime(stocks_df['Date'].dt.strftime('%Y-%m-%d'))
    stocks_df = pd.merge(stocks_df, SP500, on='Date', how='inner')

    # ---------------------- DISPLAY RAW DATA ----------------------
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('### 📄 Stock Prices(Head)')
        st.dataframe(stocks_df.head(), use_container_width=True)
    with col2:
        st.markdown('### 📄 Stock Prices(Tail)')
        st.dataframe(stocks_df.tail(), use_container_width=True)

    # ---------------------- PRICE CHARTS ----------------------
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Price of all the Stocks")
        st.caption("initial stock prices")
        st.plotly_chart(capm_functions.interactive_plot(stocks_df), use_container_width=True)
    with col2:
        st.markdown("### Price of all the Stocks (After Normalizing)")
        st.caption("prices being normalized over initial stock prices")
        st.plotly_chart(capm_functions.interactive_plot(capm_functions.normalize(stocks_df)), use_container_width=True)

    # ---------------------- DAILY RETURNS ----------------------
    stocks_daily_return = capm_functions.daily_return(stocks_df)

    # ---------------------- CALCULATE BETA ----------------------
    beta = {}
    alpha = {}
    for i in stocks_daily_return.columns:
        if i not in ['Date', 'sp500']:
            b, a = capm_functions.calculate_beta(stocks_daily_return, i)
            beta[i] = b
            alpha[i] = a

    beta_df = pd.DataFrame({
        'Stock': list(beta.keys()),
        'Beta Value': [round(v, 2) for v in beta.values()]
    })

    # ---------------------- CALCULATE RETURNS ----------------------
    rf = 0
    rm = stocks_daily_return['sp500'].mean() * 252
    return_df = pd.DataFrame({
        'Stock': list(beta.keys()),
        'Expected Return (%)': [round(rf + (b * (rm - rf)), 2) for b in beta.values()]
    })

    # ---------------------- DISPLAY RESULTS ----------------------
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('### Calculated Risk (β)')
        st.caption("risk of market is considered as 1")
        st.dataframe(beta_df, use_container_width=True)
    with col2:
        st.markdown('### Calculated Return using CAPM')
        st.caption("the risk-free rate + the beta of the investment * the expected return on the market - the risk free rate")
        st.dataframe(return_df, use_container_width=True)

    # ---------------------- INSIGHTS ----------------------
    st.markdown("### 📊 Insights & Analysis")

    # Beta Insights
    for stock, b in beta.items():
     if b == 0:
        st.markdown(f"- **{stock}** → Beta = **{b:.2f}** → No sensitivity to market movements. Price changes are independent of market trends.")
     elif b < 0:
        st.markdown(f"- **{stock}** → Beta = **{b:.2f}** → Negative market sensitivity. Tends to move opposite to the market direction.")
     elif 0 < b < 1:
        st.markdown(f"- **{stock}** → Beta = **{b:.2f}** → Low market sensitivity. Moves in the same direction as the market but with smaller swings (lower volatility).")
     elif b == 1:
        st.markdown(f"- **{stock}** → Beta = **1.00** → Moves in line with the market. Price changes generally match market moves.")
     elif b > 1:
        st.markdown(f"- **{stock}** → Beta = **{b:.2f}** → High market sensitivity. Moves in the same direction as the market but with larger swings (higher volatility).")


    # Return Insights
    for idx, row in return_df.iterrows():
      stock = row['Stock']
      exp_return = row['Expected Return (%)']
      diff = exp_return - (rm * 100)  # rm is annualized market return in decimal

      if diff > 2:  # significantly above market
        st.markdown(
            f"- **{stock}** → Expected Return = **{exp_return:.2f}%** → **Well above** market average "
            f"by {diff:.2f}%. Strong potential for outperformance if risks are acceptable."
        )
      elif 0 < diff <= 2:  # slightly above market
        st.markdown(
            f"- **{stock}** → Expected Return = **{exp_return:.2f}%** → Slightly above market average "
            f"by {diff:.2f}%. Could be a steady outperformer."
        )
      elif -2 <= diff <= 0:  # slightly below market
        st.markdown(
            f"- **{stock}** → Expected Return = **{exp_return:.2f}%** → Slightly below market average "
            f"by {abs(diff):.2f}%. May still be attractive for defensive positioning."
        )
      else:  # significantly below market
        st.markdown(
            f"- **{stock}** → Expected Return = **{exp_return:.2f}%** → **Well below** market average "
            f"by {abs(diff):.2f}%. Limited growth potential unless volatility is very low or other fundamentals are strong."
        )

    # Graph Insight
    st.markdown(
        "- The price charts show how each stock has moved historically, while the normalized chart makes it easy to compare growth rates across stocks."
    )
    st.markdown(
        "- Stocks with higher Beta tend to have wider price fluctuations in the first chart, aligning with their risk profile."
    )

except Exception as e:
    st.error(f"⚠️ Please select valid stocks and years. Error: {e}")
