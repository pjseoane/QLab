import streamlit as st

welcome    = st.Page("pages/etfs.py", title="Welcome", icon="👋")
dashboard  = st.Page("pages/dashboard.py", title="Dashboard", icon="📊")
ticker   = st.Page("pages/single_ticker.py", title="Ticker", icon="⚙️")
portfolios = st.Page("pages/portfolios.py", title="Portfolios", icon="📋")
etf=st.Page("pages/etf.py", title="ETFs Components", icon=":material/graph_5:")


# grouped navigation
pg = st.navigation({
    "Main": [welcome, dashboard],
    "Config": [ticker, portfolios,etf],
})
pg.run()

