import streamlit as st
from utils.funcs import load_portfolios

st.set_page_config(page_title="Portfolio", layout="wide")
st.title("📁 Portfolio Analysis")

BENCHMARKS = {
    "S&P 500":  "^GSPC",
    "Nasdaq":   "^IXIC",
    "Dow Jones":"^DJI",
    "None":     None,
}

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Settings")

    # watchlist selector
    watchlists = load_portfolios("data/Model Portfolios - Export.csv")
    selected   = st.selectbox("📋 Watchlist", list(watchlists.keys()))
    tickers    = st.multiselect("Stocks", watchlists[selected], default=watchlists[selected])

    st.divider()
    period    = st.selectbox("Period",    ["3mo", "6mo", "1y", "2y", "5y"])
    interval  = st.selectbox("Interval",  ["1d", "1wk", "1mo"])
    benchmark = st.selectbox("Benchmark", list(BENCHMARKS.keys()))

# ── Tabs ───────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "⚖️ Comparison",
    "📊 Performance",
    "🔥 Correlation",
    "💼 Weights",
])

with tab1:
    # normalised returns chart vs benchmark
    pass

with tab2:
    # return, volatility, sharpe, max drawdown table
    pass

with tab3:
    # correlation heatmap triangle
    pass

with tab4:
    # pie chart of weights from watchlist CSV
    pass