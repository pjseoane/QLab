import streamlit as st
from utils.funcs import * #load_portfolios
from datetime import timedelta,datetime



st.set_page_config(page_title="Portfolio", layout="wide")
st.title("📁 Portfolio Analysis")

BENCHMARKS = {
    "S&P 500":  "^GSPC",
    "Nasdaq":   "^IXIC",
    "Dow Jones":"^DJI",
    "None":     None,
}
# ── Data fetching ──────────────────────────────────────────────────────────────
# 5min conserva el cache de llamadas a yFinance
@st.cache_resource(ttl=timedelta(minutes=5),
                       max_entries=20,
                       show_spinner=True,
                       )

def get_yFinance_obj_from_API(tickers, period, interval):
    return price_fetcher(tickers, period=period, interval=interval)


# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    #st.header("Select Portfolio", icon=":arrow_drop_down_circle:", expanded=False)
    st. header("🗂️️ Portfolios")
    downloaded=False

    # watchlist selector
    #watchlists = load_portfolios("data/Model Portfolios - Export.csv")
    #selected   = st.selectbox("📋 Watchlist", list(watchlists.keys()))
    #tickers    = st.multiselect("Stocks", watchlists[selected], default=watchlists[selected])

    #st.divider()
    #period    = st.selectbox("Period",    ["3mo", "6mo", "1y", "2y", "5y"])
    #interval  = st.selectbox("Interval",  ["1d", "1wk", "1mo"])
    #benchmark = st.selectbox("Benchmark", list(BENCHMARKS.keys()))

    with st.expander("Load Portfolios", icon=":material/analytics:", expanded=False):
        # tickers = {}
        # path_to_csv=  st.text_input('Path to CSV', value="C:\\Users\\pauli\\PyCharmProjects\\QLab\\Portfolios\\Model Portfolios - Export.csv")
        file = st.text_input('Filename', value="Portfolios.csv")
        path_to_csv = "./Portfolios/" + file
        portfolios: dict = load_portfolios(path_to_csv)

        selected_watchlist = st.selectbox("Select Pack", list(portfolios.keys()))
        tickers = portfolios[selected_watchlist]['tickers']
        weights = portfolios[selected_watchlist]['weights']

        for ticker, weight in weights.items():
            st.caption(f"{ticker}: {weight:.0%}")


    with st.expander("Select Benchmark", icon=":material/check_box:", expanded=False):
        #bench = st.multiselect("Benchmark", BENCHMARKS, default=BENCHMARKS)
        benchmark = st.selectbox("Benchmark", list(BENCHMARKS.keys()))
        bench_ticker= BENCHMARKS[benchmark]
        if bench_ticker !=None:
            tickers.append(bench_ticker)


    with st.expander('Period', icon=":material/playlist_add_check:",expanded=False):
        col1, col2 = st.columns(2)

        with col1:
            period = st.selectbox(
                "Period", ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max'],
                index=6
            )
        with col2:
            interval = st.selectbox(
                "Interval", ['1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '4h',
                             '1d', '5d', '1wk', '1mo', '3mo'], index=9,
                help="Candle / data point size"
            )

    if st.sidebar.button("Refresh Data", icon=":material/refresh:"):
       # if downloaded:
            st.cache_resource.clear()
            st.toast("Cache cleared! Fetching fresh data...", icon="✅")
            st.session_state["last_refresh"] = datetime.now().strftime("%H:%M:%S")

            with st.spinner("Fetching data..."):
                y_obj = get_yFinance_obj_from_API(tickers, period=period, interval=interval)
                closes = y_obj.get_close(adjusted=True, freq='d')
                quant = cQuant(closes)

            #    downloaded = True
                st.rerun()

    if "last_refresh" in st.session_state:
        st.sidebar.caption(f"Last refreshed at {st.session_state['last_refresh']}")


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