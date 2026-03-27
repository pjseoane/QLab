import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st



#import from data
from pjs_qlab.data.YahooPriceFetcher import YahooPriceFetcher as price_fetcher
from pjs_qlab.analytics.cQuantClass import cQuantClass as cQuant
from pjs_qlab.analytics.cPyPortfolio import PyPortfolio as cPyPortfolio



def load_portfolios (fileCSV) -> dict:
    df = pd.read_csv(fileCSV)
    output={}
    for pack, group in df.groupby("Pack"):
        output[pack]={
            'tickers': group['Ticker'].tolist(),
            "weights": dict(zip(group['Ticker'], group['Wgt']))
        }
    return output


def plot_heat(log_returns):
        corr = log_returns

        mask = np.triu(np.ones(corr.shape), k=1).astype(bool)

        fig, ax = plt.subplots(figsize=(5, 3))
        ax.scatter([1, 2, 3], [1, 2, 3])
        ax.set_title(..., fontsize=6),
        ax.tick_params(labelsize=5)
        ax.set_title("Return Correlation Heat Map"),
        sns.heatmap(
            corr,
            mask=mask,
            annot=True,  # show values
            fmt=".2f",
            cmap="RdBu_r",
            vmin=-1, vmax=1,
            square=False,  # square cells
            linewidths=0.5,
            cbar_kws={"shrink": 0.8},

            annot_kws={"size": 5},  # values inside cells
            ax=ax,
        )

        return fig
"""
def charts(display_df, format, title='Title', format_y_axis_as_pct=False):
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
            text=title,
            font=dict(size=20, color="white"),
            x=0.5,  # centered (0=left, 0.5=center, 1=right)
            xanchor="center",
            y=0.95,

            # vertical position
        )
    )

    fig.update_layout(
        autosize=True,  # ignores width/height, fills container
        margin=dict(l=50, r=50, t=40, b=20)  # control margins too
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

    end_date = display_df.index[-1]  # last row index value
    start_date = display_df.index[0]

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

    # fig.update_layout(width=800, height=500)
    st.plotly_chart(fig, theme='streamlit', width='stretch')
"""

def show_dataframe(display_df, format):
    display_df.index = display_df.index.strftime("%Y-%m-%d")
    st.dataframe(
            display_df.style
            .format(formatter=format, subset=display_df.columns.tolist()),
            # .background_gradient(subset=tickers, cmap="RdYlGn")
            # .background_gradient(subset=tickers, cmap="RdYlGn"),
            # .highlight_max(subset=tickers, color="lightgreen")
            # .highlight_min(subset=tickers, color="salmon"),

            width=800,
            height=400,
            hide_index=False,  # hide the index column
            column_order=display_df.columns.tolist(),  # reorder columns shown
        )


#def get_tab_chart(display_df, title, format_df, format_y_axis_as_pct):
#    tab_chart, tab_dataframe = st.tabs(["Chart", "Dataframe"])

#    with tab_chart:  # Charts

#        try:
#            charts(display_df, format_df, title, format_y_axis_as_pct)

#        except:
#            st.write('Some problem with tickers...')

#    with tab_dataframe:  # Dataframe

#        st.subheader(title)
#        show_dataframe(display_df, format_df)


def get_tab_chart2(quant_obj, display_df, title, format, format_y_axis_as_pct ):
    tab_chart, tab_dataframe = st.tabs(["Chart", "Dataframe"])

    with tab_chart:  # Charts

        try:
            fig=quant_obj.charter_pd(display_df, format, title, format_y_axis_as_pct)
            st.plotly_chart(fig, theme='streamlit', width='stretch')
        except:
            st.write('Some problem with tickers...')

    with tab_dataframe:  # Dataframe

        st.subheader(title)
        show_dataframe(display_df, format)