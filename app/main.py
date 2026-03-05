import pandas as pd
import streamlit as st
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

#from core.services.YahooPriceFetcher import YahooPriceFetcher as price_fetcher
from pjs_qlab.data.YahooPriceFetcher import YahooPriceFetcher as price_fetcher
import pjs_qlab.data.vacio

#test cambio git2
# ── Data fetching ──────────────────────────────────────────────────────────────
df=pd.DataFrame()
@st.cache_resource(ttl=300)  # cache for 5 minutes
def get_prices(tickers: list, period='max', interval='1d')-> pd.DataFrame:
    y_obj= price_fetcher(tickers, period=period, interval=interval)
    return y_obj.get_close(adjusted=True,freq='d')



# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Investment Ideas Quant Lab",
    page_icon="📈",
    layout="wide",
)

st.title("📈 Investment Ideas Quant Lab")
st.caption("Powered by yfinance · Data from Yahoo Finance")



# ── Sidebar controls ───────────────────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Settings")

    with st.expander("Tickers", icon=":material/playlist_add_check:",expanded=False):
        tickers_input = st.text_input(
            "Tickers (comma-separated)",
            value="AAPL, MSFT, GOOGL",
            help="e.g. AAPL, TSLA, AMZN",
        )
        tickers = [t.strip().upper() for t in tickers_input.split(",") if t.strip()]

        col1, col2 = st.columns(2)

        # with col1:
        #  start_date = st.date_input("Start date", date.today() - timedelta(days=365))
        # with col2:
        #   end_date = st.date_input("End date", date.today())

        with col1:
            period = st.selectbox(
                "Period", ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max'], index=5
            )

        with col2:
            interval = st.selectbox(
                "Interval", ['1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '4h',
                         '1d', '5d', '1wk', '1mo', '3mo'], index=9,
                help="Candle / data point size"
            )

    with st.expander("Chart Settings", icon=":material/chart_data:", expanded=False):
        chart_type = st.radio("Type", ["Candlestick", "Line"])
        show_ma = st.checkbox("Moving Averages", value=True)
        show_rsi = st.checkbox("RSI", value=True)

    with st.expander("️Calculate", icon=":material/calculate:",expanded=False):
        normalize = st.checkbox("Normalize to 100", value=True)

    with st.expander("Fundamental Metrics", icon=":material/account_balance:",expanded=False):
        show_pe = st.checkbox("P/E", value=True)
        show_beta = st.checkbox("Beta", value=True)

    with st.expander("Portfolio Analysis", icon=":material/analytics:", expanded=False):
        sharpe_analysis=st.checkbox("Sharpe Ratio", value=True)
        markowitz=st.checkbox("Markowitz", value=True)

    st.divider()
    with st.expander("ETF Analysis", icon=":material/graph_5:", expanded=False):
        etf_components=st.checkbox("ETF Components", value=True)

    st.divider()
    downloaded=False
    if st.sidebar.button("Refresh Data", icon=":material/refresh:"):
        st.cache_resource.clear()
        st.toast("Cache cleared! Fetching fresh data...", icon="✅")

        # Load data
        with st.spinner("Fetching data..."):
         df = get_prices(tickers, period, interval)
        downloaded=True

        #st.rerun()



# ── Load data for all tickers ──────────────────────────────────────────────────
#data: dict[str, pd.DataFrame] = {}
#errors: list[str] = []

#with st.spinner("Fetching data..."):
#   df = get_prices(tickers, period, interval)


# ── Tabs ───────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs(["🗃️ Dataset","📊 Price Charts", "⚖️ Comparison", "📋 Fundamentals", "🔥 Correlation"])

# ════════════════════════════════════════════════════════════════════════════════
# TAB 1 — Price Charts (one per ticker)
# ════════════════════════════════════════════════════════════════════════════════
with tab1:
    if downloaded:
        st.dataframe(
           df,
           #use_container_width=False,  # stretch to full width
           width=800,  # stretch to full width
           height=400,  # fixed height with scroll
           hide_index=False,  # hide the index column
           column_order=tickers,  # reorder columns shown
       )

with tab2:
    selected = st.selectbox("Select ticker to view", tickers)

#xxxxxxx

