# -*- coding: utf-8 -*-
"""

@author: timpr
"""

import yfinance as yf
import pandas as pd
from datetime import datetime

def convert_df_to_list(dividend_df):
    """
    Converts dataframe entries into a list of lists, to maintain consistency with the format of other data
    used in the analysis

    Parameters
    ----------
    dividend_df (pandas.Dataframe) : A dataframe with a row index of datetimes in '%Y-%m-%d' format, and one column (Dividends) of floats

    Returns
    -------
    dividend_list (List<List<string, float>>): A list containing entries for each dividend for a particulare ETF.
                                               Embedded lists are of the form [Date, Unit Dividend Price]

    """
    dividend_list = []
    date_list = dividend_df.head(len(dividend_df)).index.strftime('%Y-%m-%d').tolist()
    dividend_val_list = dividend_df.tolist()
    for i in range (len(dividend_val_list)):
        dividend_list.append([date_list[i], dividend_val_list[i]])    
        
    return(dividend_list)

def lookup_dividends(ticker):
    """
    Looks up the dividend history for a stock or ETF ticker
    
    Parameters
    ----------
    ticker (yfinance Ticker object): The ticker for the stock of interest
    
    Returns
    -------
    dividend_list (List<List<String, Float>>):   A list containing a list for each stock/etf dividend payment.
                                                 Embedded lists are of the form [Date, Unit Dividend Price]
    """
    dividend_df = ticker.dividends
    return(convert_df_to_list(dividend_df))

def build_dividend_lists(portfolio_dict):
    """
    Creates lists of the histoical dividends for the following ETFs 
        DOW JONES: State Street Global Advisors SPDR Dow Jones Industrial Average ETF (DIA)
        S&P500: State Street Global Advisors SPDR S&P 500 ETF Trust (SPY)
        NASDAQ: Invesco QQQ ETF (QQQ)
        TOTAL MARKET: Vanguard Total Stock Market ETF (VTI)
    
    Parameters
    ----------
    portfolio_dict (Dict<string:float): A dictionary with stock tickers as keys and number of stock holdings as values

    Returns
    -------
    sp500_dividends (List<List<String, Float>>): A list containing a list for each SPY dividend payment.
                                                 Embedded lists are of the form [Date, Unit Dividend Price]
    dow_dividends (List<List<String, Float>>):      A list containing a list for each DIA dividend payment.
                                                 Embedded lists are of the form [Date, Unit Dividend Price]
    nasdaq_dividends (List<List<String, Float>>):   A list containing a list for each QQQ dividend payment.
                                                 Embedded lists are of the form [Date, Unit Dividend Price]
    totalmarket_dividends (List<List<String, Float>>): A list containing a list for each VTI dividend payment.
                                                    Embedded lists are of the form [Date, Unit Dividend Price]
    portfolio_dividend_dict (Dict<String:List<List<String, Float>>>): A dictionary with dividend details for each holding
                                                                      in portfolio, same format as for etfs
                                                    
    """
    # ETF dividend list
    dow_dividends = lookup_dividends(yf.Ticker("DIA")) 
    sp500_dividends = lookup_dividends(yf.Ticker("SPY")) 
    nasdaq_dividends = lookup_dividends(yf.Ticker("QQQ"))  
    totalmarket_dividends = lookup_dividends(yf.Ticker("VTI")) 
    
    # Portfolio dividends
    portfolio_dividend_dict = {}
    for key in portfolio_dict:
        portfolio_dividend_dict[key] = lookup_dividends(yf.Ticker(key))
    
    return (dow_dividends, sp500_dividends, nasdaq_dividends, totalmarket_dividends, portfolio_dividend_dict)
