import streamlit as st

st.set_page_config(page_title="Quant Lab", page_icon="📈", layout="wide")
st.session_state["default_ticker"] = "AAPL"


st.title("📈 Quant Lab")
st.subheader("Welcome")

col1, col2, col3 = st.columns(3, gap="large")

with col1:
    with st.container(border=True):
        st.subheader("📊 Single Ticker")
        st.write("""
            - Candlestick / line chart
            - Moving averages, RSI, Bollinger Bands
            - Volume analysis
            - Fundamentals
        """)
        if st.button("Open →", key="single", use_container_width=True):
            st.switch_page("pages/single_ticker.py")

with col2:
    with st.container(border=True):
        st.subheader("📁 Portfolio")
        st.write("""
            - Multiple tickers from watchlist
            - Normalised return comparison
            - Benchmark (S&P 500, etc.)
            - Correlation, weights, drawdown
        """)
        if st.button("Open →", key="portfolio", use_container_width=True):
            st.switch_page("pages/portfolios.py")

with col3:
    with st.container(border=True):
        st.subheader("📁 ETFs")

        if st.button("Open →", key="etf", use_container_width=True):
            st.switch_page("pages/etf.py")