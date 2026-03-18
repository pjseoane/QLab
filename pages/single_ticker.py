import streamlit as st
#from utils.data       import fetch_data
#from utils.indicators import compute_indicators
#from utils.charts     import build_price_chart

st.set_page_config(page_title="Single Ticker", layout="wide")
st.title("📊 Single Ticker Analysis")

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Settings")
    ticker = st.text_input("Ticker", st.session_state.get("default_ticker", "AAPL"))
    #ticker   = st.text_input("Ticker", "AAPL").upper()
    period   = st.selectbox("Period", ["1mo", "3mo", "6mo", "1y", "2y", "5y"])
    interval = st.selectbox("Interval", ["1d", "1wk", "1mo"])

    st.divider()
    st.subheader("📐 Indicators")
    show_ma     = st.checkbox("Moving Averages", value=True)
    show_rsi    = st.checkbox("RSI",             value=True)
    show_bb     = st.checkbox("Bollinger Bands", value=False)
    show_volume = st.checkbox("Volume",          value=True)

# ── Tabs ───────────────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["📊 Chart", "📋 Fundamentals", "🗃️ Raw Data"])

with tab1:
    # chart here
    pass

with tab2:
    # fundamentals here
    pass

with tab3:
    # raw dataframe here
    pass