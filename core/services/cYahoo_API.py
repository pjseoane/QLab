# -*- coding: utf-8 -*-
"""
Created on Fri Dec  8 12:25:38 2023

@author: Paulino
"""

import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
#from matplotlib.ticker import PercentFormatter
import seaborn as sns

negative_infinity = -np.inf


class cYahoo_API():
    
    #def __new__(cls,tickers,start_date=None, end_date=None, period='10y', interval='1d',auto_adjust=False,progress=True):
        #if isinstance (tickers,list):
        #   return super().__new__(cls)
       #else:
        #    raise ValueError('Tickers debe ser una lista')
            
    def __init__(self,tickers,start_date=None, end_date=None, period='max', interval='1d',auto_adjust=False,progress=True):

          self.tickers=tickers
          self.tickers.sort()
          self.period=period
          self.start_date=start_date
          self.end_date=end_date
          self.interval=interval
          self.auto_adjust = auto_adjust
          self.progress=progress
          self.len_lista=len(self.tickers)       
          self.downloaded=False
          
          
         
            
    def get_tickers(self):
        return self.tickers
        
        
    def get_all_info(self, ticker=None):
        if ticker==None:
            ticker=self.tickers[0]
           
            
        return yf.Ticker(ticker).info
       
    
    
   
    def get_all_info_panda(self):
        keys_to_get = ['address1', 'city', 'state', 'zip', 'country', 'phone', 'website', 'industry', 'industryDisp',
                       'sector', 'longBusinessSummary', 'fullTimeEmployees', 'auditRisk', 'boardRisk', 'compensationRisk',
                       'shareHolderRightsRisk', 'overallRisk', 'governanceEpochDate', 'compensationAsOfEpochDate', 'maxAge',
                       'priceHint', 'previousClose', 'open', 'dayLow', 'dayHigh', 'regularMarketPreviousClose', 'regularMarketOpen',
                       'regularMarketDayLow', 'regularMarketDayHigh', 'dividendRate', 'dividendYield', 'exDividendDate', 'payoutRatio',
                       'fiveYearAvgDividendYield', 'beta', 'trailingPE', 'forwardPE', 'volume', 'regularMarketVolume', 'averageVolume',
                       'averageVolume10days', 'averageDailyVolume10Day', 'bid', 'ask', 'bidSize', 'askSize', 'marketCap', 
                       'fiftyTwoWeekLow', 'fiftyTwoWeekHigh', 'priceToSalesTrailing12Months', 'fiftyDayAverage', 'twoHundredDayAverage',
                       'trailingAnnualDividendRate', 'trailingAnnualDividendYield', 'currency', 'enterpriseValue', 'profitMargins', 
                       'floatShares', 'sharesOutstanding', 'sharesShort', 'sharesShortPriorMonth', 'sharesShortPreviousMonthDate',
                       'dateShortInterest', 'sharesPercentSharesOut', 'heldPercentInsiders', 'heldPercentInstitutions', 
                       'shortRatio', 'shortPercentOfFloat', 'impliedSharesOutstanding', 'bookValue', 'priceToBook', 'lastFiscalYearEnd',
                       'nextFiscalYearEnd', 'mostRecentQuarter', 'earningsQuarterlyGrowth', 'netIncomeToCommon', 'trailingEps',
                       'forwardEps', 'pegRatio', 'lastSplitFactor', 'lastSplitDate', 'enterpriseToRevenue', 'enterpriseToEbitda',
                       '52WeekChange', 'SandP52WeekChange', 'lastDividendValue', 'lastDividendDate', 'exchange', 'quoteType',
                       'symbol', 'underlyingSymbol', 'shortName', 'longName', 'firstTradeDateEpochUtc', 'timeZoneFullName', 
                       'timeZoneShortName', 'uuid', 'messageBoardId', 'gmtOffSetMilliseconds', 'currentPrice', 'targetHighPrice',
                       'targetLowPrice', 'targetMeanPrice', 'targetMedianPrice', 'recommendationMean', 'recommendationKey',
                       'numberOfAnalystOpinions', 'totalCash', 'totalCashPerShare', 'ebitda', 'totalDebt', 'quickRatio', 
                       'currentRatio', 'totalRevenue', 'debtToEquity', 'revenuePerShare', 'returnOnAssets', 'returnOnEquity',
                       'grossProfits', 'freeCashflow', 'operatingCashflow', 'earningsGrowth', 'revenueGrowth', 'grossMargins',
                       'ebitdaMargins', 'operatingMargins', 'financialCurrency', 'trailingPegRatio']

        result=pd.DataFrame()
        for t in self.tickers:
            all_dat=self.get_all_info(t)
            selected_items = {key: all_dat.get(key) for key in keys_to_get}
           
            df = pd.DataFrame(selected_items,index=[0])
            result=pd.concat([result, df], ignore_index=True)
        
        result.set_index('symbol', inplace=True)
        return result
    
    
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
          
      
    #def get_ESG(self, ticker=None):
    #    if ticker==None:
    #        ticker=self.tickers[0]
    #    return yf.Ticker(ticker).sustainability
            
    
    def get_HLC(self, freq='d'):
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
                                            
                                            ).dropna()
                self.downloaded=True
             
         
            except:
                # Problemas
                raise ValueError('Problemas con el download de yfinance')
                return
              
        return self.historic_prices.groupby(pd.Grouper(freq=freq)).last().dropna()
                    
    
    def get_adj_close(self,ticker=None,freq='d'):
        
        if ticker==None:
            return self.get_HLC(freq)['Adj Close']
        else:
            try:
                return self.get_HLC(freq)['Adj Close'][ticker]
            except:
                return self.get_HLC(freq)['Adj Close']
          
        
    def get_pct_returns(self,ticker=None,freq='d'):
        return self.get_adj_close(ticker,freq).pct_change().dropna()
    
    
    def get_log_returns(self, ticker=None,freq='d'):
        return np.log(1+self.get_pct_returns(ticker,freq)).dropna()
    
    
    def get_mean_returns(self, ticker=None,freq='d'):
        return self.get_log_returns(ticker,freq).mean()


    def get_std_returns(self, ticker=None,freq='d'):
          return self.get_log_returns(ticker,freq).std()
    
    
    def get_rebase(self, ticker=None,freq='d'):
        return self.get_adj_close(ticker,freq).groupby(pd.Grouper(freq=freq)).last()/self.get_adj_close(ticker,freq).groupby(pd.Grouper(freq=freq)).last().iloc[[0]].values.flatten().tolist()


    def get_volatility(self,  ticker=None,freq='d'):
        #return np.std(self.portfolio_returns['Log_Returns'])*252**0.5
        return np.std(self.get_log_returns(ticker,freq))*252**0.5
    
    
    def get_largest_pct_drop (self, ticker=None,days=30):
       return self.get_pct_returns(ticker).rolling(window=days).min().dropna()

     
    def get_statistics(self,ticker=None,freq='w',years=2)-> dict:
        if ticker==None:
            ticker=self.tickers[0]
            
        estac_table=self.get_returns_table(ticker,freq)
        params={}
        params['mean']  =estac_table.iloc[-(years+1):-1,:].mean(axis=0)
        params['median']=estac_table.iloc[-(years+1):-1,:].median(axis=0)
        params['std']   =estac_table.iloc[-(years+1):-1,:].std(axis=0)
        params['max']   =estac_table.iloc[-(years+1):-1,:].max(axis=0)
        params['min']   =estac_table.iloc[-(years+1):-1,:].min(axis=0)
        params['count'] =estac_table.iloc[-(years+1):-1,:].count(axis=0)
        return params
 
    
    def get_log_returns_corr_matrix(self, freq='d'):
             try:
              return self.get_log_returns(freq).corr(method='pearson') #.style.background_gradient(cmap='coolwarm')
             except:
              return None
           
            
    def get_cov_matrix(self, freq='d'):
        try:
          return self.get_log_returns(freq).cov().style.background_gradient(cmap='coolwarm')
        except:
            return None
       
        
    #Rolling calcs
    # historical volatility
    def _hist_vlt(self,chunk):
        return chunk.std()*252**0.5


    def get_hist_vlt_series(self,ticker=None, days=30)-> pd.Series:
      return self.get_log_returns(ticker,freq='d').rolling(window=days).apply(self._hist_vlt).dropna()
    
    
    #**** z_Score
    def _get_zScore(self,chunk):
       return (chunk[-1] - chunk.mean()) / chunk.std()
 
   
    def get_zScore_series(self,ticker=None,days=30)->pd.Series:
       return self.get_log_returns(ticker,freq='d').rolling(window=days).apply(self._get_zScore).dropna()
   
    
    #**** Sharpe
    # https://pyquantnews.com/how-to-use-the-sharpe-ratio-for-risk-adjusted/
    def _sharpe(self,chunk):
       return chunk.mean()/chunk.std()*np.sqrt(252)
       
   
    def get_sharpe_series(self,ticker=None, days=30)->pd.Series:
        ##da igual que el de quantstats
     return self.get_pct_returns(ticker,freq='d').rolling(window=days).apply(self._sharpe).dropna()
    
 
    def _sortino(self, chunk,riskFree=0):
      """
      Determines the Sortino ratio of a strategy.
    
        Parameters
        ----------
        returns : pd.Series or np.ndarray
        Daily returns of the strategy, noncumulative.
		adjustment_factor : int, float
        Constant daily benchmark return throughout the period.

        Returns
        -------
        sortino_ratio : float

        Note
        -----
        See `<https://www.sunrisecapital.com/wp-content/uploads/2014/06/Futures_
        Mag_Sortino_0213.pdf>`__ for more details.
      """
      returns_risk_adj = np.asanyarray(chunk - riskFree)
      mean_annual_return = returns_risk_adj.mean() * 252

      # compute the downside deviation
      downside_diff = np.clip(returns_risk_adj, np.NINF, 0)
      np.square(downside_diff, out=downside_diff)
      annualized_downside_deviation = np.sqrt(downside_diff.mean()) * np.sqrt(252)
    
      return mean_annual_return / annualized_downside_deviation
  
    
    def get_sortino_series(self, ticker=None, days=30) ->pd.Series:
     return self.get_log_returns(ticker,freq='d').rolling(window=days).apply(self._sortino).dropna()
    
    
    def get_risk_table(self, ticker=None, days=30) ->pd.DataFrame:
      if ticker==None:
          ticker=self.tickers[0]
          
      risk_table=pd.DataFrame()
      vlt=self.get_hist_vlt_series (ticker,days)
      sort=self.get_sortino_series(ticker,days)
      sharpe=self.get_sharpe_series(ticker,days)
      zscore=self.get_zScore_series(ticker,days)
      risk_table=pd.concat([risk_table, vlt, sort,sharpe,zscore],axis=1).dropna()
      risk_table.columns=['vlt','sortino', 'sharpe','zscore']  
      return risk_table
    
    
    def get_daily_vlt(self,ticker=None,freq='d'):
        return self.get_pct_returns(ticker,freq).std() 
     
      
    def plot_daily_returns(self,ticker=None,freq='d'):
        dfYields=self.get_log_returns(ticker,freq)
        print('Daily simple returns')
        fig, ax = plt.subplots(figsize=(15,8))
        
        if len (self.tickers) >1 and ticker ==None:
            
            for t in self.tickers:
                ax.plot(dfYields[t], lw =2 ,label = t)
        else:
            ax.plot(dfYields, lw =2 ,label = ticker)
        

        ax.legend( loc = 'upper right' , fontsize =10)
        ax.set_title('Volatility in Daily simple returns ')
        ax.set_xlabel('Date')
        ax.set_ylabel('Daily simple returns')
        plt.show(fig)
        
      
    def plot_risk_box_plot(self,ticker=None,freq='1d'):
        return self.get_log_returns(ticker,freq).plot(kind = "box",figsize = (10,5), title = "Log Returns Risk Box Plot")
        
   
    def plot_risk_return(self,ticker=None,freq='1d'):
      if len(self.tickers)>1:
        ret=self.get_log_returns(ticker,freq)
        APR_avg=ret.groupby([ret.index.year]).agg('sum').mean()
        STD=ret.groupby([ret.index.year]).agg('std')*np.sqrt(252)
        STD_avg=STD.mean()
        
        # configuration - generate different colors & sizes
        c = [y + x for y, x in zip(APR_avg, STD_avg)]
        c = list(map(lambda x : x /max(c), c))
        s = list(map(lambda x : x * 600, c))
       
        # plot
        plt.style.use('dark_background')
        fig, ax = plt.subplots(figsize = (10,5))
        ax.set_title(r"Risk ($\sigma$) vs Return ($APY$) of all  instruments")
        #ax.set_facecolor((0.95, 0.95, 0.99))
        ax.grid(c = (0.80, 0.80, 0.99))
        ax.set_xlabel(r"Standard Deviation $\sigma$")
        ax.set_ylabel(r"Annualized Returns")
        ax.scatter(STD_avg, APR_avg, s = s , c = c , cmap = "Blues", alpha = 0.8, edgecolors="red", linewidth=3)
        ax.axhline(y = 0.0,xmin = 0 ,xmax = 5,c = "white",linewidth = 1.0,zorder = 0,  linestyle = '--')
        ax.axvline(x = 0.0,ymin = 0 ,ymax = 40,c = "white",linewidth = 1.0,zorder = 0,  linestyle = '--')
        
        ax.text(0.5,0.1,'Balanz', alpha=0.1,fontsize=50,ha='center',va='center',
                rotation=0, transform=ax.transAxes)
        for idx, instr in enumerate(list(STD.columns)):
            ax.annotate(instr, (STD_avg[idx] + 0.01, APR_avg[idx]))
      
      else:
        print('Solo para 2 o mas tickers')
        return


 ####ir agregando estas func

    def plot_std_years(self):
      
        STD=self.get_log_returns().groupby([self.get_log_returns().index.year]).agg('std')*np.sqrt(252)
        fig, ax = plt.subplots(figsize = (10,5))
        ax.set_title(r"Standard Deviation ($\sigma$) of all instruments for all years")
        ax.set_facecolor((0.95, 0.95, 0.99))
        ax.grid(c = (0.75, 0.75, 0.99))
        ax.set_ylabel(r"Standard Deviation $\sigma$")
        ax.set_xlabel(r"Years")
        STD.plot(ax = plt.gca(),grid = True)
        for instr in STD:
            stds = STD[instr]
            years = list(STD.index)
            for year, std in zip(years, stds):
                label = "%.3f"%std
                plt.annotate(label, xy = (year, std), xytext=((-1)*50,   40),textcoords = 'offset points', ha = 'right', va='bottom', bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5),arrowprops=dict(arrowstyle = '->', connectionstyle='arc3,rad=0'))
        return


    def plotDensityDailyReturns(self):
        sns.displot(self.get_LogReturns(), kind = 'kde', aspect = 2)
        plt.xlim(-0.1, 0.1)
        return
        
    
    def plotVlt_Histogram(self, ticker=None,freq='d'):
        #https://www.learnpythonwithrune.org/calculate-the-volatility-of-historic-stock-prices-with-pandas-and-python/
        #https://tinytrader.io/how-to-calculate-historical-price-volatility-with-python/
        #str_vol=str(round(self.get_LogReturns()[stock]*100,2))

          
        if ticker==None:
                 ticker=self.tickers[0]
              
              
        fig, ax = plt.subplots(1, 1, figsize=(7, 5))
        n, bins, patches = ax.hist(self.get_log_returns(ticker,freq), bins=50, alpha=0.65, color='blue')

        ax.set_xlabel('log return of stock price')
        ax.set_ylabel('frequency of log return')
        #ax.set_title('Historical Volatility for ' + self.get_stock_longname(stock))
        ax.set_title('Historical Volatility for ' + ticker)

        # get x and y coordinate limits
        x_corr = ax.get_xlim()
        y_corr = ax.get_ylim()

        # make room for text
        header = y_corr[1] / 5
        y_corr = (y_corr[0], y_corr[1] + header)
        ax.set_ylim(y_corr[0], y_corr[1])

        # print historical volatility on plot
        x = x_corr[0] + (x_corr[1] - x_corr[0]) / 30
        y = y_corr[1] - (y_corr[1] - y_corr[0]) / 15
        ax.text(x, y , 'Annualized Volatility: ' + '%', fontsize=11, fontweight='bold')
        x = x_corr[0] + (x_corr[1] - x_corr[0]) / 15
        y -= (y_corr[1] - y_corr[0]) / 20

        ax.xaxis.set_major_formatter(mtick.PercentFormatter(xmax=1, decimals=None, symbol='%', is_latex=False))
        # save histogram plot of historical price volatility
        fig.tight_layout()
        #fig.savefig('volatility histogram.png')
        fig.savefig(f'Charts\\{ticker}-histogram.png') 
   
      
    def plot_historical_volatility(self, ticker=None, days=30):
        if ticker==None:
           ticker=self.tickers[0]
           y1=self.get_adj_close(ticker)
           y2=self.get_hist_vlt_series(ticker,days)
              
        else:
          y1=self.get_adj_close(ticker)
          y2=self.get_hist_vlt_table(days)[ticker]

                  
        plt.style.use('dark_background')
        

        fig, ax=plt.subplots(figsize = (10, 5))
        plt.title('Historical Volatility for ' + ticker)

        
        #Eje izq
        ax.set_xlabel('Fecha', color = 'w')
        ax.set_ylabel("Close", color = 'b')
        ax.plot(y1,color='b',label='Close',linewidth = 3)
        
        ax.text(0.5,0.1,'Balanz', alpha=0.1,fontsize=50,ha='center',va='center',
                rotation=0, transform=ax.transAxes)
        
        
        #Eje der
        ax2=ax.twinx()
        ax2.set_ylabel('Vlt Hist', color = 'g' )
        ax2.plot(y2,color='g',linestyle='--')
        
        yticks = mtick.PercentFormatter(xmax=1, decimals=1)
        ax2.yaxis.set_major_formatter(yticks)
        
        plt.grid(color = 'white', linestyle = '--', linewidth = 0.2)
        plt.tight_layout()
        plt.show()
        
        
    def __plotHeatmap(self, correlation_matrix, title):
            try:
                #fig1 = plt.figure()
                #sns.heatmap(correlation_matrix,xticklabels=correlation_matrix.columns, yticklabels=correlation_matrix.columns,
                #            cmap='YlGnBu', annot=True, linewidth=0.5)
                #print(title)
                #plt.savefig('Charts\\Correlation Heatmap.png')
                #return plt.show(fig1)
                
                fig1 = plt.figure()
                corr=correlation_matrix
                mask=np.zeros_like(corr, dtype=bool)
                mask[np.triu_indices_from(mask)]=True
                sns.heatmap(corr,annot=True,mask=mask,xticklabels=corr.columns, yticklabels=corr.columns)
                plt.savefig('Charts\\Correlation Heatmap.png')
                plt.show(fig1) 
                return
                
                
            except:
                return None
      

    def plot_returns_corr_heatmap(self, freq='d'):
            if self.len_lista>1:
                return self.__plotHeatmap(self.get_log_returns_corr_matrix(freq),'Heatmap de Log returns')
            else:
                raise ValueError('Solo se aplica a una lista de tickers')