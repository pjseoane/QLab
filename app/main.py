import pandas as pd
import streamlit as st
import sys
import os
from datetime import timedelta,datetime

import plotly.express as px
import plotly.graph_objects as go

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

def get_log_returns(prices:pd.DataFrame,freq='d'):
    q_obj= cQuant(prices)
    return q_obj.get_log_returns(freq=freq)




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
    st.header("⚙️ Settings/New Layout")

    with st.expander("Tickers", icon=":material/playlist_add_check:",expanded=True):
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
    with st.expander('Datasets', icon=":material/dataset:", expanded=False):
        show_dataset = st.radio("Show Datasets",
                                ['Closes',
                                'Returns',
                                 'Cumulative Returns',
                                 'Log Returns',
                                 'Mean Returns',
                                 'Std Returns',
                                 'Rebase',
                                 'Largest pct drop',
                                 'Largest pct rise',

                                 ])
        #show_cumm_returns= st.checkbox("Cummulative Returns", value=True)
        #show_returns= st.checkbox("Returns", value=True)


    with st.expander("Chart Settings", icon=":material/chart_data:", expanded=False):
        chart_type = st.radio("Type", ["Candlestick", "Line"])
        show_ma = st.checkbox("Moving Averages", value=True)
        show_rsi = st.checkbox("RSI", value=True)

    with st.expander("Volatility", icon=":material/browse_activity:", expanded=False):
        chart_type = st.radio("Type", [
                                 'Annualized Volatility',
                                 'Daily Volatility',
                                 'Historical Vlt Series',])
        #show_ma = st.checkbox("Moving Averages", value=True)
        #show_rsi = st.checkbox("RSI", value=True)


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
    #downloaded=False
    if st.sidebar.button("Refresh Data", icon=":material/refresh:"):
        st.cache_resource.clear()
        st.toast("Cache cleared! Fetching fresh data...", icon="✅")
        st.session_state["last_refresh"] = datetime.now().strftime("%H:%M:%S")
        # Load data
        #with st.spinner("Fetching data..."):
         #   df = get_prices(tickers, period, interval)

        #    df1=df.copy(True)
        #    df.index = df.index.date


        #downloaded=True

        st.rerun()
    # This persists across reruns
    if "last_refresh" in st.session_state:
        st.sidebar.caption(f"Last refreshed at {st.session_state['last_refresh']}")



# ── Load data for all tickers ──────────────────────────────────────────────────
data: dict[str, pd.DataFrame] = {}
errors: list[str] = []

with st.spinner("Fetching data..."):
   df = get_prices(tickers, period, interval)
   #df1 = df.copy(True)
   #df.index = df.index.date


# ── Tabs ───────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs(["🗃️ Datasets","📊 Price Charts", "⚖️ Comparison", "📋 Fundamentals", "🔥 Correlation"])

# ════════════════════════════════════════════════════════════════════════════════
# TAB 1 — Price Charts (one per ticker)
# ════════════════════════════════════════════════════════════════════════════════
with tab1:
    #if downloaded:
        col1, col2 = st.columns(2)

        width = 400,  # stretch to full width
        height = 300
        display_df = df.copy()

        with col1:
            if show_dataset=='Closes':
                st.subheader("Closes")
                format_y_axis_as_pct= False

                display_df.index = display_df.index.strftime("%Y-%m-%d")

                st.dataframe(
                    display_df,

                    #use_container_width=False,  # stretch to full width

                    hide_index=False,  # hide the index column
                    column_order=tickers,  # reorder columns shown
                )
            elif show_dataset=='Cumulative Returns':
                st.subheader("Cumulative Returns")
                format_y_axis_as_pct= True

                display_df=get_cum_returns(df,freq='d')
                display_df.index=display_df.index.date

                st.dataframe(

                    display_df.style
                    .format("{:.2%}", subset=tickers)
                    .background_gradient(subset=tickers, cmap="RdYlGn")
                    .highlight_max(subset=tickers, color="lightgreen")
                    .highlight_min(subset=tickers, color="salmon"),


                    hide_index=False,  # hide the index column
                    column_order=tickers,  # reorder columns shown

            )
            elif show_dataset=='Returns':
                st.subheader("% Returns")

                format_y_axis_as_pct=True
                display_df = get_pct_returns(df,freq='d')
                display_df.index=display_df.index.date

                st.dataframe(
                    display_df.style
                    .format("{:.2%}", subset=tickers)
                    .background_gradient(subset=tickers, cmap="RdYlGn")
                    .highlight_max(subset=tickers, color="lightgreen")
                    .highlight_min(subset=tickers, color="salmon"),


                    hide_index=False,  # hide the index column
                    column_order=tickers,  # reorder columns shown

                )
            elif show_dataset=='Log Returns':
                st.subheader("Log Returns")

                format_y_axis_as_pct = True
                display_df = get_log_returns(df, freq='d')
                display_df.index = display_df.index.date

                st.dataframe(
                    display_df.style
                    .format("{:.2%}", subset=tickers)
                    .background_gradient(subset=tickers, cmap="RdYlGn")
                    .highlight_max(subset=tickers, color="lightgreen")
                    .highlight_min(subset=tickers, color="salmon"),

                    hide_index=False,  # hide the index column
                    column_order=tickers,  # reorder columns shown

                )





        with col2:
            fig = go.Figure()

            for ticker in display_df:
                fig.add_trace(go.Scatter(
                x=display_df.index,
                y=display_df[ticker],
                name=ticker,
                mode="lines"
                ))
            if format_y_axis_as_pct:
                fig.update_yaxes(tickformat=".1%")

            fig.update_xaxes(
                    dtick="M1",  # one tick per month
                    tickformat="%b '%y",  # Jan '24
                    tickangle=-45,  # tilt to avoid overlap
                    showgrid=True,
                    gridcolor="rgba(255,255,255,0.1)",
                    tickcolor="white",
                    tickfont=dict(size=11),
                )

            end_date = df.index[-1]  # last row index value
            start_date = df.index[0]

            delta_days = (end_date - start_date).days

            if delta_days <= 90:
                dtick, fmt = "M1", "%d %b"  # short range → daily/weekly labels
            elif delta_days <= 365:
                dtick, fmt = "M1", "%b '%y"  # 1 year → monthly
            elif delta_days <= 365 * 3:
                dtick, fmt = "M3", "%b '%y"  # 3 years → quarterly
            else:
                dtick, fmt = "M12", "%Y"  # long range → yearly

            fig.update_xaxes(dtick=dtick, tickformat=fmt, tickangle=-45)

            #fig.update_xaxes(dtick=dtick, tickformat=fmt, tickangle=-45)
            st.plotly_chart(fig, width='stretch')






