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
#df=pd.DataFrame()
@st.cache_resource(ttl=timedelta(minutes=5),
                   max_entries=20,
                   show_spinner=True,
                   )

def get_closes(adjusted=True, freq='d'):
    return y_obj.get_close(adjusted=adjusted, freq=freq)

def get_cum_returns(freq='d'):
    return q_obj.get_cum_returns(freq=freq)

def get_pct_returns(freq='d'):
    return q_obj.get_pct_returns(freq=freq)

def get_log_returns(freq='d'):
    return q_obj.get_log_returns(freq=freq)

def get_rebase(freq='d'):
    return q_obj.get_rebase(freq=freq)

def get_largest_pct_drop(days=30):
    return q_obj.get_largest_pct_drop(days=days)

def get_largest_pct_rise(days=30):
    return q_obj.get_largest_pct_rise(days=days)

def get_hist_vlt_series(days=30):
    return q_obj.get_hist_vlt_series(days=days)

def get_summary(freq='ME'):
    return q_obj.get_summary(freq=freq)



def function_executor(func, parameters,tickers,title='title' ):
    st.subheader(title)
    output_df=func(parameters)
    output_df.index = output_df.index.date
    st.dataframe(

        output_df.style
        .format("{:.2%}", subset=tickers)
        .background_gradient(subset=tickers, cmap="RdYlGn")
        .highlight_max(subset=tickers, color="lightgreen")
        .highlight_min(subset=tickers, color="salmon"),

        hide_index=False,  # hide the index column
        column_order=tickers,  # reorder columns shown

    )
    return output_df


# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Investment Ideas Quant Lab",
    page_icon="📈",
    layout="wide",
)

st.title("📈 Investment Ideas Quant Lab")
st.caption("Powered by yfinance · Data from Yahoo Finance")
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
                                     'Rebase',
                                     'Largest pct drop',
                                     'Largest pct rise',
                                     'Historic Volatility',
                                     'Summary',

                                     ])



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
    y_obj = price_fetcher(tickers, period=period, interval=interval)
    closes=y_obj.get_close(adjusted=True,freq='d')
    q_obj= cQuant(closes)

    #df = get_prices(tickers, period, interval)
   #df1 = df.copy(True)
   #df.index = df.index.date



# ── Tabs ───────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs(["🗃️ Datasets","📊 Price Charts", "⚖️ Comparison", "📋 Fundamentals", "🔥 Correlation"])

# ════════════════════════════════════════════════════════════════════════════════
# TAB 1 — Price Charts (one per ticker)
# ════════════════════════════════════════════════════════════════════════════════
with tab1: #Datasets
    #if downloaded:
        col1, col2 = st.columns([1,3])

        width = 400,  # stretch to full width
        height = 300

        display_df = closes.copy()
        format_y_axis_as_pct = False

        with col1:
            if show_dataset=='Closes':
                format_y_axis_as_pct = False

                st.subheader("Closes")
                display_df.index = display_df.index.strftime("%Y-%m-%d")

                st.dataframe(
                   display_df,

                    hide_index=False,  # hide the index column
                    column_order=tickers,  # reorder columns shown
                )
            elif show_dataset=='Cumulative Returns':

                format_y_axis_as_pct = True
                display_df = function_executor(get_cum_returns, 'd', tickers, title=show_dataset)

            elif show_dataset=='Returns':

                format_y_axis_as_pct = True
                display_df = function_executor(get_pct_returns, 'd', tickers, title=show_dataset)

            elif show_dataset=='Log Returns':

                format_y_axis_as_pct = True
                display_df = function_executor(get_log_returns, 'd', tickers, title=show_dataset)

            elif show_dataset=='Rebase':
                format_y_axis_as_pct = True
                display_df = function_executor(get_rebase, 'd', tickers, title=show_dataset)

            elif show_dataset == 'Largest pct drop':
                format_y_axis_as_pct = True
                days = st.number_input('days', min_value=1, max_value=500, value=30, step=1)
                display_df = function_executor(get_largest_pct_drop, days,tickers,   title=show_dataset)

            elif show_dataset == 'Largest pct rise':
                format_y_axis_as_pct = True
                days = st.number_input('days', min_value=1, max_value=500, value=30, step=1)
                display_df = function_executor(get_largest_pct_rise, days,tickers,   title=show_dataset)

            elif show_dataset == 'Historic Volatility':
                format_y_axis_as_pct = True,
                days = st.number_input('days', min_value=1, max_value=500, value=30, step=1)
                display_df = function_executor(get_hist_vlt_series, days,tickers, title=show_dataset)

            elif show_dataset == 'Summary':
                format_y_axis_as_pct = True,
                #days = st.number_input('days', min_value=1, max_value=500, value=30, step=1)
                #display_df = function_executor(get_summary, 'ME',tickers, title=show_dataset)

                st.subheader(show_dataset)
                output_df = get_summary(freq='ME')
                #output_df.index = output_df.index.date
                st.dataframe(

                    (output_df #.style.format("{:.2%}")
                     # .background_gradient( cmap="RdYlGn")
                     #.highlight_max(color="lightgreen")
                     #.highlight_min(color="salmon")
                     )
                    #column_order=tickers,  # reorder columns shown

                )

        with col2: # Chart
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

            fig.update_layout(
                title=dict(
                    text=show_dataset,
                    font=dict(size=20, color="white"),
                    x=0.5,  # centered (0=left, 0.5=center, 1=right)
                    xanchor="center",
                    y=0.95,  # vertical position
                )
            )

            fig.update_xaxes(
                    dtick="M1",  # one tick per month
                    tickformat="%b '%y",  # Jan '24
                    tickangle=-45,  # tilt to avoid overlap
                    showgrid=True,
                    gridcolor="rgba(255,255,255,0.1)",
                    tickcolor="white",
                    tickfont=dict(size=11),
                )

            end_date = closes.index[-1]  # last row index value
            start_date = closes.index[0]

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






