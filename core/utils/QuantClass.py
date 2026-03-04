# -*- coding: utf-8 -*-
"""
Created on Sat May 17 13:36:47 2025

@author: pauli
"""

import numpy as np
import pandas as pd



class QuantClass():
  def __init__(self, prices: pd.DataFrame):

    self.prices=prices.dropna()


  def get_close(self,freq='d'):
      
        return self.prices.groupby(pd.Grouper(freq=freq)).last().dropna()

        """
        if adjusted:
          # precios normalizados por dividendos, splits
            try:
                return self.prices.groupby(pd.Grouper(freq=freq)).last().dropna()['Adj Close']
            except:
                return self.prices.groupby(pd.Grouper(freq=freq)).last().dropna()['Close']
        else:
          #precios reales
                return self.prices.groupby(pd.Grouper(freq=freq)).last().dropna()['Close']
        """

  def get_pct_returns(self,freq='d'):
    return self.get_close(freq=freq).pct_change().dropna()


  def get_cum_returns(self,freq='d'):
        return (1+self.get_pct_returns(freq=freq)).cumprod()-1


  def get_log_returns(self,freq='d'):
        return np.log(1+self.get_pct_returns(freq=freq)).dropna()


  def get_mean_returns(self, freq='d'):
        return self.get_log_returns(freq=freq).mean()


  def get_std_returns(self, freq='d'):
          return self.get_log_returns(freq=freq).std()


  def get_rebase(self, freq='d'):
        return self.get_close(freq=freq).groupby(pd.Grouper(freq=freq)).last()/self.get_close(freq=freq).groupby(pd.Grouper(freq=freq)).last().iloc[[0]].values.flatten().tolist()


  def get_annualized_volatility(self,freq='d'):
        #return np.std(self.portfolio_returns['Log_Returns'])*252**0.5
        return np.std(self.get_log_returns(freq))*252**0.5


  def get_daily_vlt(self,freq='d'):
        return np.std(self.get_log_returns(freq))


  def get_largest_pct_drop (self, days=30):
       return self.get_pct_returns().rolling(window=days).min().dropna()


  def get_largest_pct_rise (self, days=30):
       return self.get_pct_returns().rolling(window=days).max().dropna()


  def get_log_returns_corr_matrix(self, lista=[],freq='d'):
       if not lista:
          out= self.get_log_returns(freq=freq).corr(method='pearson')
       else:
          out= self.get_log_returns(freq=freq).corr(method='pearson')[lista].loc[lista]   
       return out.style.background_gradient(cmap='coolwarm')


  def get_cov_matrix(self, lista=[],freq='d'):
      if not lista:
         out= self.get_log_returns(freq=freq).cov()
      else:
          out= self.get_log_returns(freq=freq).cov()[lista].loc[lista]      
      return out.style.background_gradient(cmap='coolwarm')
  

  #Rolling calcs
      # historical volatility
  def _hist_vlt(self,chunk):
      return chunk.std()*252**0.5


  def get_hist_vlt_series(self, days=30)-> pd.Series:
      return self.get_log_returns(freq='d').rolling(window=days).apply(self._hist_vlt).dropna()


  #**** z_Score
  def _get_zScore(self,chunk):
       return (chunk[-1] - chunk.mean()) / chunk.std()


  def get_zScore_series(self,days=30)->pd.Series:
       return self.get_log_returns(freq='d').rolling(window=days).apply(self._get_zScore).dropna()


  #**** Sharpe
  # https://pyquantnews.com/how-to-use-the-sharpe-ratio-for-risk-adjusted/
  def _sharpe(self,chunk):
       return chunk.mean()/chunk.std()*np.sqrt(252)


  def get_sharpe_series(self, days=30)->pd.Series:
     return self.get_log_returns(freq='d').rolling(window=days).apply(self._sharpe).dropna()


  def get_sharpes(self,pivot='SPY', lt_years=5, st_years=2):
      
      lt_returns = self.get_log_returns().tail(int(252 * lt_years))
      st_returns = self.get_log_returns().tail(int(252 * st_years))
      lt_sharpes = lt_returns.mean() / lt_returns.std() * np.sqrt(252)
      st_sharpes = st_returns.mean() / st_returns.std() * np.sqrt(252)

      #st_sharpes=self.get_sharpe_series(days=int(252 * st_years)).iloc[-1]
      #lt_sharpes=self.get_sharpe_series(days=int(252 * lt_years)).iloc[-1]

      sharpes = {
            'st_sharpe': st_sharpes,
            'lt_sharpe' : lt_sharpes
          }

      sharpes_df= pd.DataFrame(sharpes, index = sharpes['st_sharpe'].keys())

      st_pivot=sharpes_df.loc[pivot].st_sharpe
      lt_pivot=sharpes_df.loc[pivot].lt_sharpe

      sharpes_df['cuadrante']=sharpes_df.apply(lambda row:
                              0 if row['st_sharpe'] == st_pivot and row['lt_sharpe'] == lt_pivot else
                                           1 if row['st_sharpe'] >st_pivot and row['lt_sharpe'] >lt_pivot else
                                           2 if row['st_sharpe'] <st_pivot and row['lt_sharpe'] >lt_pivot else
                                           3 if row['st_sharpe'] <st_pivot and row['lt_sharpe'] <lt_pivot else 4, axis=1)

      sharpes_df['points']=sharpes_df['st_sharpe']+sharpes_df['lt_sharpe'] #Aca algun calculo que meta puntos a cada stock
          
      return sharpes_df.sort_values(by='points',ascending=False)


  def get_sharpes_cuadrante(self,cuadrante=1, lt_years=5, st_years=2, pivot='SPY'):
        cuadro_df=self.get_sharpes(lt_years=lt_years, st_years=st_years,pivot=pivot)
        condition=cuadro_df['cuadrante']==cuadrante
        selected_stocks=cuadro_df[condition].index.tolist()
        return selected_stocks


  

