# ---------------------- IMPORTS ----------------------
import streamlit as st
import datetime
import pandas_datareader.data as web
import yfinance as yf
import pandas as pd
from pages.utils import capm_functions
import numpy as np
import plotly.express as px

# ---------------------- PAGE CONFIG ----------------------
st.set_page_config(
    page_title="CAPM - Beta & Return Calculator",
    page_icon="📈",
    layout="wide",
)

# ---------------------- HEADER ----------------------
st.markdown(
    """
    <h1 style="text-align:center; color:#1E88E5;">📊 CAPM Beta & Return Calculator</h1>
    <p style="text-align:center; font-size:18px; color:#555;">
    Analyze how your chosen stock performs against the market using the Capital Asset Pricing Model (CAPM).
    </p>
    <hr style="height:2px; border:none; background-color:#1E88E5;">
    """,
    unsafe_allow_html=True
)

# ---------------------- USER INPUTS ----------------------
col1, col2 = st.columns(2)
with col1:
    stock = st.selectbox(
        "📌 Select a Stock",
        ('AAPL', 'TSLA', 'NFLX', 'MGM', 'MSFT', 'AMZN', 'NVDA', 'GOOGL')
    )
with col2:
    year = st.number_input(
        "📅 Number of Years",
        min_value=1, max_value=10, value=5
    )

# ---------------------- DATA FETCHING ----------------------
try:
    end = datetime.date.today()
    start = datetime.date(end.year - year, end.month, end.day)

    # S&P500 data
    SP500 = web.DataReader(['sp500'], 'fred', start, end)

    # Stock data
    stocks_df = yf.download(stock, period=f'{year}y')[['Close']]
    stocks_df.columns = [stock]
    stocks_df.reset_index(inplace=True)

    SP500.reset_index(inplace=True)
    SP500.columns = ['Date', 'sp500']

    # Merge on Date
    stocks_df['Date'] = pd.to_datetime(stocks_df['Date'].dt.strftime('%Y-%m-%d'))
    stocks_df = pd.merge(stocks_df, SP500, on='Date', how='inner')

    # ---------------------- CALCULATIONS ----------------------
    stocks_daily_return = capm_functions.daily_return(stocks_df)
    rm = stocks_daily_return['sp500'].mean() * 252  # Annual market return
    beta, alpha = capm_functions.calculate_beta(stocks_daily_return, stock)
    rf = 0  # Risk-free rate
    return_value = round(rf + (beta * (rm - rf)), 2)

    # ---------------------- RESULTS ----------------------
    st.markdown("### 📌 Results")
    res_col1, res_col2 = st.columns(2)
    res_col1.metric(label="Beta", value=f"{beta:.2f}")
    res_col2.metric(label="Expected Return (%)", value=f"{return_value:.2f}%")

    # ---------------------- PLOT ----------------------
    fig = px.scatter(
        stocks_daily_return,
        x='sp500',
        y=stock,
        title=f"{stock} vs S&P 500 Daily Returns",
        labels={"sp500": "S&P 500 Daily Return", stock: f"{stock} Daily Return"},
        template="plotly_white"
    )
    fig.add_scatter(
        x=stocks_daily_return['sp500'],
        y=beta * stocks_daily_return['sp500'] + alpha,
        mode='lines',
        name='Expected Return',
        line=dict(color="crimson", width=2)
    )
    st.plotly_chart(fig, use_container_width=True)

    # ---------------------- INSIGHTS ----------------------
    st.markdown("### 📊 Insights & Analysis")

    # Beta interpretation
    # --- Beta Interpretation with Color Labels ---
    if beta < 0:
     beta_insight = (
        f"🟣 **Negative Beta Alert**\n\n"
        f"**{stock}** has a **Beta of {beta:.2f}**, meaning it often moves **opposite** to the market. "
        "This rare behavior can act as a hedge during market downturns but may lag when the market rises."
    )
    elif beta == 0:
        beta_insight = (
        f"⚪ **Zero Market Correlation**\n\n"
        f"**{stock}** has a **Beta of 0**, indicating **no correlation** with market movements. "
        "Its price changes are largely driven by company-specific factors, not market trends."
    )
    elif 0 < beta < 1:
     beta_insight = (
        f"🟢 **Low Volatility**\n\n"
        f"**{stock}** has a **Beta of {beta:.2f}**, meaning it moves **less than the market**. "
        "Expect smaller price swings, which may appeal to risk-averse investors seeking stability."
    )
    elif beta == 1:
     beta_insight = (
        f"🟡 **Market-Matching Volatility**\n\n"
        f"**{stock}** has a **Beta of 1.00**, meaning it typically mirrors the market’s ups and downs. "
        "Its risk and return are aligned with broad market performance."
    )
    else:  # beta > 1
     beta_insight = (
        f"🔴 **High Volatility**\n\n"
        f"**{stock}** has a **Beta of {beta:.2f}**, meaning it amplifies market moves. "
        "When markets rise, it often rises more; when they fall, it may drop harder. "
        "Suitable for aggressive investors comfortable with larger swings."
    )
# --- Expected Return Interpretation ---
    if return_value > rm:
     return_insight = (
        f"With an expected return of **{return_value:.2f}%**, this is projected to **outperform** "
        f"the market’s average return of **{rm:.2f}%**. This could signal stronger growth potential, "
        "assuming the CAPM assumptions hold."
    )
    elif return_value < rm:
     return_insight = (
        f"With an expected return of **{return_value:.2f}%**, this is projected to **underperform** "
        f"the market’s average return of **{rm:.2f}%**. It may still be suitable for stability, "
        "but growth prospects appear limited under CAPM."
    )
    else:
     return_insight = (
        f"The expected return of **{return_value:.2f}%** matches the market’s average return, "
        "suggesting performance in line with broad market trends."
    )

# --- Graph Interpretation ---
    graph_insight = (
    "The scatter plot compares the stock’s daily returns with those of the market (S&P 500). "
    "The red CAPM line shows the predicted relationship between market returns and stock returns. "
    "Points tightly clustered around the line indicate that the stock’s performance closely follows "
    "CAPM expectations, while greater dispersion signals other factors at play."
)
    # Display insights
    st.markdown(f"- {beta_insight}")
    st.markdown(f"- {return_insight}")
    st.markdown(f"- {graph_insight}")

except Exception as e:
    st.error(f"⚠️ Unable to fetch data. Please try again later.\nError: {e}")
