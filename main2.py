import streamlit as st

from datetime import timedelta,datetime

from utils.funcs import *
from pjs_qlab.data.YahooPriceFetcher import YahooPriceFetcher as price_fetcher
from pjs_qlab.analytics.cQuantClass import cQuantClass as cQuant


# ── Data fetching ──────────────────────────────────────────────────────────────
# 5min conserva el cache de llamadas a yFinance
@st.cache_resource(ttl=timedelta(minutes=5),
                       max_entries=20,
                       show_spinner=True,
                       )
def get_yFinance_obj_from_API(tickers, period, interval):
    return price_fetcher(tickers, period=period, interval=interval)


# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Investment Ideas Quant Lab",
    page_icon="📈",
    layout="wide",
)

#st.title("📈 Investment Ideas Quant Lab")
#st.caption("Powered by yfinance · Data from Yahoo Finance")
st.markdown("""
                                    <style>
                                    [data-testid="stNumberInput"] input {
                                        font-size: 12px;
                                        height: 28px;
                                        padding: 2px 8px; 
                                        color: #26a69a;
                                        background-color: #1e1e2e;
                                        border: 1px solid #26a69a;
                                        border-radius: 4px;
                                        width: 40px;
                                    }
                                    [data-testid="stNumberInput"] label {
                                    color: #aaaaaa;
                                    font-size: 12px;
                                    }
                                    </style>
                                """, unsafe_allow_html=True)


# ── Sidebar controls ───────────────────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Settings")

    with st.expander("Load Portfolios", icon=":material/search:", expanded=False):
        file = st.text_input('Filename', value="Portfolios.csv")
        path_to_csv = "./Portfolios/" + file
        portfolios: dict = load_portfolios(path_to_csv)


    #with st.expander("Portfolio Selector", icon=":material/analytics:", expanded=False):
        selected_watchlist = st.selectbox("Select Pack", list(portfolios.keys()))
        tickers = portfolios[selected_watchlist]['tickers']
        weights = portfolios[selected_watchlist]['weights']

        for ticker, weight in weights.items():
           st.caption(f"{ticker}: {weight:.0%}")

    #with st.expander("Tickers", icon=":material/playlist_add_check:", expanded=False):

        tickers_input = st.text_input(
            "Tickers (comma-separated)",
            # value="AAPL, MSFT, GOOGL",
            value=', '.join(tickers),
            help="e.g. AAPL, TSLA, AMZN",
        )
        tickers = [t.strip().upper() for t in tickers_input.split(",") if t.strip()]

    #with st.expander('Period', icon=":material/playlist_add_check:", expanded=False):
        col1, col2 = st.columns(2)

        with col1:
            period = st.selectbox(
                "Period", ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max'], index=7
            )
        with col2:
            interval = st.selectbox(
                "Interval", ['1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '4h',
                             '1d', '5d', '1wk', '1mo', '3mo'], index=9,
                help="Candle / data point size"
            )

        #st.divider()
        # downloaded=False
    if st.sidebar.button("Refresh Data", icon=":material/refresh:"):
        st.cache_resource.clear()
        st.toast("Cache cleared! Fetching fresh data...", icon="✅")
        st.session_state["last_refresh"] = datetime.now().strftime("%H:%M:%S")

        with st.spinner("Fetching data..."):
            y_obj = get_yFinance_obj_from_API(tickers, period=period, interval=interval)
            closes = y_obj.get_close(adjusted=True, freq='d')
            quant = cQuant(closes)

        # downloaded=True

            st.rerun()
        # This persists across reruns
    if "last_refresh" in st.session_state:
            st.sidebar.caption(f"Last refreshed at {st.session_state['last_refresh']}")

    with st.expander('Datasets', icon=":material/dataset:", expanded=False):
        pass


    with st.expander("Chart Settings", icon=":material/chart_data:", expanded=False):
        pass
    with st.expander("️Calculate", icon=":material/calculate:",expanded=False):
        normalize = st.checkbox("Normalize to 100", value=True)

    with st.expander("Fundamental Metrics", icon=":material/account_balance:",expanded=False):
        show_pe = st.checkbox("P/E", value=True)
        show_beta = st.checkbox("Beta", value=True)



    st.divider()
    with st.expander("ETF Analysis", icon=":material/graph_5:", expanded=False):
        etf_components=st.checkbox("ETF Components", value=True)







# ── Load data for all tickers ──────────────────────────────────────────────────






# ── Tabs ───────────────────────────────────────────────────────────────────────
ticker, portfolios, tab3, tab4 = st.tabs(["📊 Ticker", "⚖️ Portfolios", "📋 ETFs", "🔥 etc"])

# ════════════════════════════════════════════════════════════════════════════════
# TAB 1 — Price Charts (one per ticker)
# ════════════════════════════════════════════════════════════════════════════════
with (ticker): #Ticker
    pass


    desc, tab2, tab3, tab4, tab5, tab6 = st.tabs(
        ["Description", "Fundamentals", "Charts", "Dataframes", "Options", "News"])

    with desc:
        pass

    with tab2:
        pass

    with tab3:
        pass

    with tab4:
        pass

    with tab5:
        pass

    with tab6:
        pass


with portfolios:
    load, returns, correlations, risk, Optimize=st.tabs(["Load","Returns","Correlations", "Risks","Optimize"])
    with load:
        pass

with tab3:
    pass
with tab4:
    pass
