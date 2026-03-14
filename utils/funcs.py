import pandas as pd
import numpy as np
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns

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




