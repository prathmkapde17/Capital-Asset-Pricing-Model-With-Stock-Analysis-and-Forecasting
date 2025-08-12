import streamlit as st

# ---------------------- PAGE CONFIG ----------------------
st.set_page_config(
    page_title="Trading Guide App",
    page_icon="💹",
    layout="wide"
)
# Inject custom CSS to style sidebar
st.markdown("""
    <style>
    /* Sidebar background color */
    [data-testid="stSidebar"] {
        background-color: #F8F9FA;
        padding: 20px;
    }

    /* Sidebar titles */
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        color: #2E86C1;
        font-weight: 700;
    }

    /* Sidebar menu items */
    [data-testid="stSidebar"] .css-1v3fvcr {
        color: #34495E;
        font-size: 16px;
        padding: 8px 14px;
        border-radius: 8px;
        transition: all 0.2s ease-in-out;
    }

    /* Hover effect */
    [data-testid="stSidebar"] .css-1v3fvcr:hover {
        background-color: #D6EAF8;
        color: #1B4F72;
        transform: translateX(5px);
    }

    /* Selected item */
    [data-testid="stSidebar"] .css-1v3fvcr[aria-current="page"] {
        background-color: #2E86C1 !important;
        color: white !important;
        font-weight: 600;
    }
    </style>
""", unsafe_allow_html=True)
# ---------------------- HEADER ----------------------
st.markdown(
    """
    <style>
    .main-title {
        font-size: 48px;
        font-weight: bold;
        color: #1E88E5;
        text-align: center;
    }
    .sub-title {
        font-size: 20px;
        text-align: center;
        color: #555;
    }
    .divider {
        border-top: 2px solid #1E88E5;
        margin-top: 10px;
        margin-bottom: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="main-title">📊 Trading Guide App</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Your trusted platform for smarter stock market decisions.</div>', unsafe_allow_html=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ---------------------- HERO IMAGE ----------------------
st.image("app.jpg", use_column_width=True)

# ---------------------- INTRO ----------------------
st.markdown(
    """
    ### 🚀 Why Choose Us?
    We provide the **most reliable** tools and insights to help you make **informed investment decisions**.
    From stock data to market predictions, everything is in one place — designed for traders & investors like you.
    """
)

# ---------------------- SERVICES ----------------------
st.markdown("## 🔍 Our Services")
col1, col2 = st.columns(2)

with col1:
    st.markdown("### ① 📈 Stock Information")
    st.write("Get **real-time stock data**, historical performance, and key financial insights to track your favorite companies.")

    st.markdown("### ② 🤖 Stock Prediction")
    st.write("View **AI-powered forecasts** for the next 30 days based on market trends & historical data.")

with col2:
    st.markdown("### ③ 📊 CAPM Return")
    st.write("Understand how **CAPM** calculates the expected return of an asset based on market risk and performance.")

    st.markdown("### ④ 📉 CAPM Beta")
    st.write("Calculate **Beta** to measure a stock’s volatility and expected return compared to the market.")

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

