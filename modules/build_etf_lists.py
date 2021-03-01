# -*- coding: utf-8 -*-
"""

@author: timpr
"""
import yfinance as yf
from datetime import datetime
from datetime import timedelta

def build_etf_lists(order_value_list):
    """
    Determines the equivalent number of ETFs purchased or sold at the same time as orders were completed in the order
    value list. Using the following ETFs as representative of market indexes
        DOW JONES: State Street Global Advisors SPDR Dow Jones Industrial Average ETF (DIA)
        S&P500: State Street Global Advisors SPDR S&P 500 ETF Trust (SPY)
        NASDAQ: Invesco QQQ ETF (QQQ)
        TOTAL MARKET: Vanguard Total Stock Market ETF (VTI)
    
    Parameters
    ----------
    order_value_list (List<List<String>): A list containing all order details. Each order represented in a tuple of the
                                           form (Date, Value). Negative values represent a sale.

    Returns
    -------
    sp500_orders (List<List<string, float>>): A list containing a list of equivalent SPY ETF purchases/sales. 
                                              Embedded lists are of the form [Date, No. Shares]. Negative value indicates a sale
    dow_orders (List<List<string, float>>):   A list containing a list of equivalent DIA ETF purchases/sales. 
                                              Embedded lists are of the form [Date, No. Shares]. Negative value indicates a sale
    nasdaq_orders (List<List<string, float>>): A list containing a list of equivalent QQQ ETF purchases/sales. 
                                               Embedded lists are of the form [Date, No. Shares]. Negative value indicates a sale
    totalmarket_orders (List<List<string, float>>): A list containing a list of equivalent VTI ETF purchases/sales. 
                                                    Embedded lists are of the form [Date, No. Shares]. Negative value indicates a sale 
 
    """
    # Using yahoo finance instead of robin_stocks here as it is better for pulling specific
    # historical stock prices from period > 5years ago
    
    dow_orders = []
    sp500_orders = []
    nasdaq_orders = []
    totalmarket_orders = []
    
    # Store daily prices in a dictionary to avoid duplicate yfinance calls for trades on the same day
    price_history_dict = {}
    
    for order in order_value_list:
        start_time = order[0][0:10]
        end_time = datetime.strptime(start_time, "%Y-%m-%d") + timedelta(days=1)
        end_time = end_time.strftime("%Y-%m-%d")
        
        if start_time not in price_history_dict:        
            # Find historical ETF prices for a day if that day's data hasn't been obtained yet
            dow_hist = yf.Ticker("DIA").history(prepost = True, start = start_time, end = end_time)
            sp500_hist = yf.Ticker("SPY").history(prepost = True, start = start_time, end = end_time)
            nasdaq_hist = yf.Ticker("QQQ").history(prepost = True, start = start_time, end = end_time)
            total_hist = yf.Ticker("VTI").history(prepost = True, start = start_time, end = end_time)
                        
            # Calculate the equivalent number of index shares that could be bought/sold for the purchase/sale price
            # of the stock from the order list
            dow_orders.append([order[0], order[1]/dow_hist.iloc[0]["High"]])
            sp500_orders.append([order[0], order[1]/sp500_hist.iloc[0]["High"]])
            nasdaq_orders.append([order[0], order[1]/nasdaq_hist.iloc[0]["High"]])
            totalmarket_orders.append([order[0], order[1]/total_hist.iloc[0]["High"]])
            price_history_dict[start_time] = [
                                      dow_hist.iloc[0]["High"],
                                      sp500_hist.iloc[0]["High"],
                                      nasdaq_hist.iloc[0]["High"],
                                      total_hist.iloc[0]["High"]
                                      ]
        else:
            dow_orders.append([order[0], order[1]/price_history_dict[start_time][0]])
            sp500_orders.append([order[0], order[1]/price_history_dict[start_time][1]])
            nasdaq_orders.append([order[0], order[1]/price_history_dict[start_time][2]])
            totalmarket_orders.append([order[0], order[1]/price_history_dict[start_time][3]])
        
    return (dow_orders, sp500_orders, nasdaq_orders, totalmarket_orders)
