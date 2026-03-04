import pandas as pd
import streamlit as st

from Class.YahooPriceFetcher import YahooPriceFetcher as price_fetcher

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Investment Ideas Quant Lab",
    page_icon="📈",
    layout="wide",
)

st.title("📈 Investment Ideas Quant Lab")
st.caption("Powered by yfinance · Data from Yahoo Finance")

# ── Data fetching ──────────────────────────────────────────────────────────────
#df=pd.DataFrame()
@st.cache_resource(ttl=300)  # cache for 5 minutes
def get_prices(tickers: list, period, interval)-> pd.DataFrame:
    y_obj= price_fetcher(tickers, period=period, interval=interval)
    return y_obj.get_close(adjusted=True,freq='d')

# ── Sidebar controls ───────────────────────────────────────────────────────────
# Sidebar navigation drives the active tab
with st.sidebar:
    active_tab = st.radio("Navigation",
        ["📊 Price Charts", "⚖️ Comparison", "📋 Fundamentals", "🔥 Correlation"]
    )

    # Conditional sidebar content per "tab"
    if active_tab == "📊 Price Charts":
        st.divider()
        st.subheader("Chart Settings")
        chart_type = st.radio("Chart type", ["Candlestick", "Line"])
        show_ma = st.checkbox("Moving Averages")
        show_rsi = st.checkbox("RSI")

    elif active_tab == "⚖️ Comparison":
        st.divider()
        st.subheader("Comparison Settings")
        normalize = st.checkbox("Normalize to base 100", value=True)
        show_drawdown = st.checkbox("Show Max Drawdown")

    elif active_tab == "📋 Fundamentals":
        st.divider()
        st.subheader("Metrics to Show")
        show_pe = st.checkbox("P/E Ratio", value=True)
        show_eps = st.checkbox("EPS", value=True)
        show_beta = st.checkbox("Beta", value=True)

# ── Load data for all tickers ──────────────────────────────────────────────────
