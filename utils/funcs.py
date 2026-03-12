import pandas as pd
def load_portfolios (fileCSV) -> dict:
    df = pd.read_csv(fileCSV)
    output={}
    for pack, group in df.groupby("Pack"):
        output[pack]={
            'tickers': group['Ticker'].tolist(),
            "weights": dict(zip(group['Ticker'], group['Wgt']))
        }
    return output