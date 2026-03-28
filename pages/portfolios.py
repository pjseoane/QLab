
from utils.funcs import *
from datetime import timedelta,datetime

#import from external API
from pjs_qlab.data.yAPI_class import yAPI_class as yAPI
from pjs_qlab.analytics.cQuantClass import cQuantClass as cQuant
from pjs_qlab.analytics.cPyPortfolio import PyPortfolio as cPyPortfolio



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

def get_yFinance_obj_from_API(tickers): #, period, interval):
    yOBJECT=yAPI(tickers)
    return yOBJECT #.get_HLC(period=period, interval=interval)['Adj Close']


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

        days = st.number_input('Window days', min_value=1, max_value=500, value=30, step=1)

    if st.sidebar.button("Refresh Data", icon=":material/refresh:"):
        if not downloaded:
            st.cache_resource.clear()
            st.toast("Cache cleared! Fetching fresh data...", icon="✅")
            st.session_state["last_refresh"] = datetime.now().strftime("%H:%M:%S")

            with st.spinner("Fetching data..."):
                y_obj = get_yFinance_obj_from_API(tickers)#, period=period, interval=interval)
                closes = y_obj.get_HLC(period=period, interval=interval)['Adj Close']
                quant = cQuant(closes)


                downloaded = True
                #st.rerun()

    if "last_refresh" in st.session_state:
        st.sidebar.caption(f"Last refreshed at {st.session_state['last_refresh']}")


# ── Tabs ───────────────────────────────────────────────────────────────────────
if downloaded:
 returns, rebase, drop_rise, hist_vlt, ratios, pyPortfolio, test  = st.tabs([
    "Price & Returns",
    "Rebase",
    "Drop & Rises",
    "Volatility",
    "Ratios",
    "pyPortfolio",
    "test",
])

 with returns:




 # with c_returns:
     display_df = quant.get_cum_returns('d')
     title = 'Cumulative Returns'
     format = "{:.2%}"
     format_y_axis_as_pct = True
     get_tab_chart2(quant, display_df, title, format, format_y_axis_as_pct)

     display_df = quant.get_pct_returns('d')
     title = ' Pct Returns'
     format = "{:.2%}"
     format_y_axis_as_pct = True
     get_tab_chart2(quant, display_df, title, format, format_y_axis_as_pct)

 #with log_returns:
     display_df = quant.get_log_returns('d')
     title = 'Log Returns'
     format = "{:.2%}"
     format_y_axis_as_pct = True
     get_tab_chart2(quant, display_df, title, format, format_y_axis_as_pct)

     display_df = quant.get_close(interval)
     title = 'Closes'
     format = "{:.2f}"
     format_y_axis_as_pct = False
     get_tab_chart2(quant, display_df, title, format, format_y_axis_as_pct)

 with rebase:
     display_df = quant.get_rebase('d')
     title='Rebase'
     format = "{:.2f}"
     format_y_axis_as_pct = False
     get_tab_chart2(quant, display_df, title, format, format_y_axis_as_pct)

 with drop_rise:
    display_df = quant.get_largest_pct_drop(days)
    title = 'Largest Pct Drop'
    format = "{:.2%}"
    format_y_axis_as_pct = True
    get_tab_chart2(quant, display_df, title, format, format_y_axis_as_pct)

 #with lp_rise:
    display_df = quant.get_largest_pct_rise(days)
    title = 'Largest Pct Rise'
    format = "{:.2%}"
    format_y_axis_as_pct = True
    get_tab_chart2(quant, display_df, title, format, format_y_axis_as_pct)

 with hist_vlt:
     display_df = quant.get_hist_vlt_series(days)
     title = 'Volatility'
     format = "{:.2%}"
     format_y_axis_as_pct = True
     get_tab_chart2(quant, display_df, title, format, format_y_axis_as_pct)

 with ratios:
     display_df = quant.get_zScore_series(days)
     title = 'z-Score'
     format = "{:.2%}"
     format_y_axis_as_pct = False
     get_tab_chart2(quant, display_df, title, format, format_y_axis_as_pct)

 #with sharpe:
     display_df = quant.get_sharpe_series(days)
     title = 'Sharpe Ratio'
     format = "{:.2%}"
     format_y_axis_as_pct = False
     get_tab_chart2(quant, display_df, title, format, format_y_axis_as_pct)

 #with sortino:
     display_df = quant.get_sortino_series(days)
     title = 'Sortino Ratio'
     format = "{:.2%}"
     format_y_axis_as_pct = False
     get_tab_chart2(quant, display_df, title, format, format_y_axis_as_pct)

 with pyPortfolio:
     if benchmark == 'None':
         port_closes = closes
     else:
         port_closes = closes.drop(columns=[bench_ticker])

     port_Obj = cPyPortfolio(port_closes)
     weights = port_Obj.get_weightsHRP()
     col1, col2, col3 = st.columns(
         [1, 2, 3],
         gap="small",  # space between columns: "small", "medium", "large"
         vertical_alignment="top"
     )
     col1.header("Weights")
     col2.header("Pie Chart")
     col3.header("Evolution")

     with col1:

         display_df = pd.DataFrame(list(weights.items()), columns=['Ticker', 'Weight'])
         format = ({'Weight': '{:.2%}'})

         st.dataframe(
             display_df.style
             .format(formatter=format, subset=display_df.columns.tolist()),
             # .background_gradient(subset=tickers, cmap="RdYlGn")
             # .background_gradient(subset=tickers, cmap="RdYlGn"),
             # .highlight_max(subset=tickers, color="lightgreen")
             # .highlight_min(subset=tickers, color="salmon"),

             width=200,
             height=400,
             hide_index=False,  # hide the index column
             column_order=display_df.columns.tolist(),  # reorder columns shown
         )

     with col2:
         fig = px.pie(values=list(weights.values()), names=list(weights.keys()), title='Distribution')
         fig.update_layout(
             autosize=True,  # ignores width/height, fills container
             margin=dict(l=50, r=50, t=40, b=20)  # control margins too
         )
         st.plotly_chart(fig, theme='streamlit', width='stretch')
         # fig.show()

     with col3:
         display_df = pd.DataFrame(port_Obj.get_cumulative_returns(weights))
         display_df.columns = ["Portfolio"]

         if benchmark == 'None':
             display_df["Benchmark"] =1
         else:
             display_df[bench_ticker] = closes[bench_ticker]/closes[bench_ticker].iloc[0]

         #
         format = "{:.4f}"

         title="Portfolio & Benchmark"

         get_tab_chart2(quant, display_df, title, format, format_y_axis_as_pct)



 with test:
     pass








