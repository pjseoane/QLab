import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st






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