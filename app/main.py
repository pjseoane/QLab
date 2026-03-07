import pandas as pd
import streamlit as st
import sys
import os
from datetime import timedelta, datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from pjs_qlab.data.YahooPriceFetcher import YahooPriceFetcher as price_fetcher
from pjs_qlab.analytics.cQuantClass import cQuantClass as cQuant

#test cambio git2
# ── Data fetching ──────────────────────────────────────────────────────────────
df=pd.DataFrame()
@st.cache_resource(ttl=timedelta(minutes=5),
                   max_entries=20,
                   show_spinner=True,
                   )
# cache for 5 minutes
def get_prices(tickers: list, period='max', interval='1d')-> pd.DataFrame:
    y_obj= price_fetcher(tickers, period=period, interval=interval)
    return y_obj.get_close(adjusted=True,freq='d')

def get_cum_returns(prices:pd.DataFrame,freq='d'):
    q_obj= cQuant(prices)
    return q_obj.get_cum_returns(freq=freq)

def get_pct_returns(prices:pd.DataFrame,freq='d'):
    q_obj= cQuant(prices)
    return q_obj.get_pct_returns(freq=freq)




# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Investment Ideas Quant Lab",
    page_icon="📈",
    layout="wide",
)

st.title("📈 Investment Ideas Quant Lab")
st.caption("Powered by yfinance · Data from Yahoo Finance")

#******************************************************************************************
with st.sidebar:
    st.header("⚙️ Settings")

    with st.expander("📊 Chart Settings", expanded=True):
        chart_type = st.radio("Type", ["Candlestick", "Line"])
        show_ma = st.checkbox("Moving Averages", value=True)
        show_rsi = st.checkbox("RSI", value=True)

    with st.expander("⚖️ Comparison Settings"):
        normalize = st.checkbox("Normalize to 100", value=True)

    with st.expander("📋 Fundamental Metrics"):
        show_pe = st.checkbox("P/E", value=True)
        show_beta = st.checkbox("Beta", value=True)