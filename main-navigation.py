import streamlit as st

welcome    = st.Page("pages/welcome.py", title="Home", icon=":material/home:")
dashboard  = st.Page("pages/dashboard.py", title="Dashboard", icon="📊")
ticker   = st.Page("pages/single_ticker.py", title="Ticker", icon="⚙️")
portfolios = st.Page("pages/portfolios.py", title="Portfolios", icon="📋")
etf=st.Page("pages/etf.py", title="ETFs Components", icon=":material/graph_5:")
settings = st.Page("pages/settings.py", title="Settings", icon=":material/settings:")

# grouped navigation
pg = st.navigation({
    "Main": [welcome, dashboard],
    "Markets": [ticker, portfolios,etf],
    "Settings": [settings]
})
pg.run()

