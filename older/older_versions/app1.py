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
df=pd.DataFrame()
@st.cache_resource(ttl=300)  # cache for 5 minutes
def get_prices(tickers: list, period, interval)-> pd.DataFrame:
    y_obj= price_fetcher(tickers, period=period, interval=interval)
    return y_obj.get_close(adjusted=True,freq='d')

# ── Sidebar controls ───────────────────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Settings")

    tickers_input = st.text_input(
        "Tickers (comma-separated)",
        value="AAPL, MSFT, GOOGL",
        help="e.g. AAPL, TSLA, AMZN",
    )
    tickers = [t.strip().upper() for t in tickers_input.split(",") if t.strip()]

    col1, col2 = st.columns(2)

    # with col1:
      #  start_date = st.date_input("Start date", date.today() - timedelta(days=365))
    #with col2:
     #   end_date = st.date_input("End date", date.today())

    with col1:
        period=st.selectbox(
        "Period", ['1d','5d','1mo','3mo','6mo','1y','2y','5y','10y','ytd','max'],index=5
        )

    with col2:
        interval = st.selectbox(
        "Interval", ['1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '4h',
                     '1d', '5d', '1wk', '1mo', '3mo'], index=9,
        help="Candle / data point size"
        )

    st.divider()
    #downloaded=False
    #if st.sidebar.button("Refresh Data", icon=":material/refresh:"):
    if st.sidebar.button("Refresh Data", icon=":material/refresh:"):
        st.cache_resource.clear()
        st.toast("Cache cleared! Fetching fresh data...", icon="✅")

        #Load data
        #with st.spinner("Fetching data..."):
        #    df = get_prices(tickers, period, interval)

        st.rerun()
     #downloaded=True

    st.divider()
    st.subheader("📐 Technical Indicators")
    show_ma = st.checkbox("Moving Averages (20 / 50 / 200)", value=True)
    show_bollinger = st.checkbox("Bollinger Bands", value=False)
    show_rsi = st.checkbox("RSI (14)", value=True)
    show_volume = st.checkbox("Volume", value=True)

    st.divider()
    chart_type = st.radio("Chart type", ["Candlestick", "Line"], index=0)




# ── Load data for all tickers ──────────────────────────────────────────────────
#data: dict[str, pd.DataFrame] = {}
#errors: list[str] = []

with st.spinner("Fetching data..."):
    df = get_prices(tickers, period, interval)


# ── Tabs ───────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs(["🗃️ Dataset","📊 Price Charts", "⚖️ Comparison", "📋 Fundamentals", "🔥 Correlation"])

# ════════════════════════════════════════════════════════════════════════════════
# TAB 1 — Price Charts (one per ticker)
# ════════════════════════════════════════════════════════════════════════════════
with tab1:
    #if downloaded:
        st.dataframe(
            df,
            use_container_width=False,  # stretch to full width
            height=400,  # fixed height with scroll
            hide_index=False,  # hide the index column
            column_order=tickers,  # reorder columns shown
        )


