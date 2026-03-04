# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import yfinance as yf
import pandas as pd
import time


class YahooDataFetcher():
  def __init__(self, tickers:list):
    self.tickers=tickers
    self.tickers.sort()


  def get_tickers(self):
    return self.tickers


  def get_all_info(self,ticker): #, ticker=None):
        #if ticker==None:
        #    ticker=self.tickers[0]
        
        print('fetching: ', ticker)
        out=yf.Ticker(ticker).info
               
        return out


  def get_all_info_panda(self):
        self.result=pd.DataFrame()

        for t in self.tickers:
          time.sleep(1)
          all_dat=self.get_all_info(t)
                
              
          
          #Remove empty or all-NA columns
          row_to_add=pd.DataFrame([all_dat])
          #row_to_add=row_to_add.dropna(axis=1, how='all')

          #self.result= pd.concat([self.result,pd.DataFrame([all_dat])], ignore_index=True)
          self.result = pd.concat([self.result, row_to_add], ignore_index=True)

        self.result.set_index(['symbol'], inplace=True)
        return self.result


  def get_actions(self, ticker=None):
        if ticker==None:
            ticker=self.tickers[0]
        return yf.Ticker(ticker).actions


  def get_dividends(self, ticker=None):
          if ticker==None:
              ticker=self.tickers[0]
          return yf.Ticker(ticker).dividends


  def get_splits(self, ticker=None):
          if ticker==None:
              ticker=self.tickers[0]
          return yf.Ticker(ticker).splits


  def get_financials(self, ticker=None):
          if ticker==None:
              ticker=self.tickers[0]
          return yf.Ticker(ticker).quarterly_financials


  def get_major_holders(self, ticker=None):
          if ticker==None:
              ticker=self.tickers[0]
          return yf.Ticker(ticker).major_holders


  def get_institutional_holders(self, ticker=None):
          if ticker==None:
              ticker=self.tickers[0]
          return yf.Ticker(ticker).institutional_holders


  def get_balance_sheet(self, ticker=None):
          if ticker==None:
              ticker=self.tickers[0]
          return yf.Ticker(ticker).quarterly_balance_sheet


  def get_cash_flow(self, ticker=None):
          if ticker==None:
             ticker=self.tickers[0]
          return yf.Ticker(ticker).quarterly_cashflow


  def get_ISIN(self, ticker=None):
          if ticker==None:
              ticker=self.tickers[0]
          return yf.Ticker(ticker).isin


  def get_recommendations(self, ticker=None):
          if ticker==None:
              ticker=self.tickers[0]
          return yf.Ticker(ticker).recommendations


  def get_earnings(self, ticker=None):
          if ticker==None:
              ticker=self.tickers[0]
          return yf.Ticker(ticker).earnings
