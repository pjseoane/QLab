import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import pjs_qlab.analytics.plot_functions as cPlot





def load_portfolios (fileCSV) -> dict:
    df = pd.read_csv(fileCSV)
    output={}
    for pack, group in df.groupby("Pack"):
        output[pack]={
            'tickers': group['Ticker'].tolist(),
            "weights": dict(zip(group['Ticker'], group['Wgt']))
        }
    return output
def plot_risk_box(display_df, title, tickformat):
    fig = cPlot.plot_risk_box(display_df, title, tickformat)
    st.plotly_chart(fig, theme='streamlit', width='stretch')

def plot_heat_map(display_df, title, tickformat,width, height):
    fig=cPlot.plot_returns_corr_heatmap(display_df, title, tickformat,width, height)
    st.plotly_chart(fig, theme='streamlit', width='stretch')

def plot_density_daily_returns(display_df, title, tickformat):
    fig=cPlot.plotDensityDailyReturns(display_df, title, tickformat)
    st.plotly_chart(fig, theme='streamlit', width='stretch')


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
            fig=cPlot.charter_pd(display_df=display_df, title=title, format_y_axis_as_pct=False, format="{:.2f}")
            st.plotly_chart(fig, theme='streamlit', width='stretch')

        except:
            st.write('Some problem with tickers...')

    with tab_dataframe:  # Dataframe

        st.subheader(title)
        show_dataframe(display_df, format)