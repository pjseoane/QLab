# -*- coding: utf-8 -*-
"""
Created on Sat May 17 13:33:06 2025

@author: pauli
"""

import yfinance as yf
import pandas as pd


class YahooPriceFetcher():
    def __init__(self, tickers: list, start_date=None, end_date=None, period='max', interval='1d',auto_adjust=False,progress=True):

      #if isinstance(tickers,list):
        self.tickers = tickers
        self.tickers.sort()
        self.start_date = start_date
        self.end_date = end_date
        self.period = period
        self.interval = interval
        self.auto_adjust = auto_adjust
        self.progress = progress
        self.len_lista = len(self.tickers)
        self.downloaded = False
        self.historic_prices = None


    def get_tickers(self):
        return self.tickers


    def get_HLC(self):
        if not self.downloaded:
            #Download de historic prices
            # Valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
            # Valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo

            try:
                self.historic_prices = yf.download(self.tickers,
                                            interval=self.interval,
                                            period=self.period,
                                            auto_adjust=self.auto_adjust,
                                            start=self.start_date,
                                            end=self.end_date,
                                            prepost=False,
                                            threads=True,
                                            progress=self.progress,

                                            )#.dropna()
                self.downloaded=True


            except:
                # Problemas
                raise ValueError('Problemas con el download de yfinance')
                return

        return self.historic_prices #.groupby(pd.Grouper(freq=freq)).last().dropna()
    
    
    def get_close(self,adjusted=True,freq='d'):

          if adjusted:
            # precios normalizados por dividendos, splits
              try:
                  return self.get_HLC().groupby(pd.Grouper(freq=freq)).last().dropna()['Adj Close']
              except:
                  return self.get_HLC().groupby(pd.Grouper(freq=freq)).last().dropna()['Close']
          else:
            #precios reales
                  return self.get_HLC().groupby(pd.Grouper(freq=freq)).last().dropna()['Close']