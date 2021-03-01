# -*- coding: utf-8 -*-
"""

@author: timpr
"""
import matplotlib.pyplot as plt
import robin_stocks as r
import yfinance as yf
from datetime import datetime
from datetime import timedelta

def add_dividends(date, dividend_list, units, date_cutoff, ticker):
    """
    Adds etf units to hypothetical portfolio based on the etf price at the time of dividend payment (simulate dividend reinvestment)
    
    Parameters
    ----------
    date (Datetime): The current date (that we want to check if a dividend has been paid within the past 4 weeks of)
    dividend_list (List<List<string, float>>): A list containing entries for each dividend for a particulare ETF.
                                               Embedded lists are of the form [Date, Unit Dividend Price]
    units (float): Number of units of etf
    date_cutoff (Datetime): The start date of the analysis, any dividends paid before this can be removed from dividend_list

    Returns
    -------
    units (float): As above
    dividend_list (List<List<string, float>>): As above

    """
    # Copy list to allow for dividends to be deleted during iteration
    dividend_list_copy = dividend_list.copy()

    for i in range(len(dividend_list_copy)):
        # Remove all dividends from before the analysis start time
        if datetime.strptime(dividend_list_copy[i][0],"%Y-%m-%d") < date_cutoff:
            dividend_list.remove(dividend_list_copy[i])
        # Add etfs for dividends that have recently been issued, then remove them from the list
        elif datetime.strptime(dividend_list_copy[i][0],"%Y-%m-%d") <= date:
            # Pull etf price from yfinance and add the number that could be bought with reinvested dividend
            end_time = datetime.strptime(dividend_list_copy[i][0], "%Y-%m-%d") + timedelta(days=1)
            end_time = end_time.strftime("%Y-%m-%d")
            current_price = ticker.history(prepost = True, start = dividend_list_copy[i][0], end = end_time).iloc[0]["High"]
            units += dividend_list_copy[i][1]/current_price
            dividend_list.remove(dividend_list_copy[i])
        else:
            break

    return (units, dividend_list)

def generate_plots(dow_orders, 
                    sp500_orders, 
                    nasdaq_orders, 
                    totalmarket_orders,
                    dow_dividends, 
                    sp500_dividends, 
                    nasdaq_dividends, 
                    totalmarket_dividends,
                    dow_fees, 
                    sp500_fees, 
                    nasdaq_fees, 
                    totalmarket_fees,
                    portfolio_dict,
                    portfolio_dividend_dict
                    ):
    """
    Creates plots showing the performance of the investment strategy over time relative to the ETF portfolios,
    and outputs summary statistics

    
    Parameters
    ----------
    sp500_orders (List<List<string, float>>): A list containing a list of equivalent SPY ETF purchases/sales. 
                                              Embedded lists are of the form [Date, No. Shares]. Negative value indicates a sale
    dow_orders (List<List<string, float>>):   A list containing a list of equivalent DIA ETF purchases/sales. 
                                              Embedded lists are of the form [Date, No. Shares]. Negative value indicates a sale
    nasdaq_orders (List<List<string, float>>): A list containing a list of equivalent QQQ ETF purchases/sales. 
                                               Embedded lists are of the form [Date, No. Shares]. Negative value indicates a sale
    totalmarket_orders (List<List<string, float>>): A list containing a list of equivalent VTI ETF purchases/sales. 
                                                    Embedded lists are of the form [Date, No. Shares]. Negative value indicates a sale 
    sp500_dividends (List<List<string, float>>): A list containing a list for each SPY dividend payment.
                                                 Embedded lists are of the form [Date, Unit Dividend Price]
    dow_dividends (List<List<string, float>>):      A list containing a list for each DIA dividend payment.
                                                 Embedded lists are of the form [Date, Unit Dividend Price]
    nasdaq_dividends (List<List<string, float>>):   A list containing a list for each QQQ dividend payment.
                                                 Embedded lists are of the form [Date, Unit Dividend Price]
    totalmarket_dividends (List<List<string, float>>): A list containing a list for each VTI dividend payment.
                                                    Embedded lists are of the form [Date, Unit Dividend Price]  
    dow_fees (float): the annual fee percentage (expressed as a proportion) charged for DIA ETFs
    sp500_fees (float): the annual fee percentage (expressed as a proportion) charged for DIA ETFs
    nasdaq_fees (float): the annual fee percentage (expressed as a proportion) charged for DIA ETFs
    totalmarket_fees (float): the annual fee percentage (expressed as a proportion) charged for DIA ETFs
    portfolio_dividend_dict (Dict<String:List<List<String, Float>>>): A dictionary with dividend details for each holding
                                                                      in portfolio, same format as for etfs
    portfolio_dict (Dict<string:float): A dictionary with stock tickers as keys and number of stock holdings as values
    
    Returns
    -------
    None
 
    """
    # Get the start date of the investment history
    start_date = datetime.strptime(dow_orders[-1][0],"%Y-%m-%d")
    end_date = datetime.today()
    dividend_cutoff = start_date
    
    # Initiate lists to store graph points
    dow_performance_values = []
    sp500_performance_values = []
    nasdaq_performance_values = []
    totalmarket_performance_values = []
    plot_dates = []
    
    # Intitiate portfolio tracking variables
    dow_units = 0
    sp500_units = 0
    nasdaq_units = 0
    totalmarket_units = 0
    current_portfolio = dict.fromkeys(portfolio_dict.keys(),0)
      
    while (start_date <= end_date):
        # Check to see if the market is open on the current date, skip if it is closed
        if r.get_market_hours("XNYS", start_date.strftime("%Y-%m-%d"))["is_open"] == False:
            start_date += datetime.timedelta(days=28)
            continue
      
        # Add or remove stocks from current portfolio based on recent orders
        portfolio_dict_copy = portfolio_dict.copy()
        portfolio_dividend_dict_copy = portfolio_dividend_dict.copy()
        for key in portfolio_dict_copy:
            # Add or remove stocks from current portfolio based on recent orders
            for i in range(len(portfolio_dict_copy[key])-1,-1,-1):
                if datetime.strptime(portfolio_dict_copy[key][i][0],"%Y-%m-%d") <= start_date:
                    if key not in current_portfolio:
                        current_portfolio[key] = portfolio_dict_copy[key][i][1]
                    else:
                        current_portfolio[key] += portfolio_dict_copy[key][i][1]
                    portfolio_dict[key].remove(portfolio_dict_copy[key][i])
         
            # Add recent dividends to current portfolio
            if key not in current_portfolio or len(portfolio_dividend_dict_copy[key]) == 0:
                continue
            current_portfolio[key], portfolio_dividend_dict[key] = add_dividends(start_date, 
                                                                                 portfolio_dividend_dict_copy[key], 
                                                                                 current_portfolio[key], 
                                                                                 dividend_cutoff, 
                                                                                 yf.Ticker(key))     
        # Calculate current portfolio value
        current_portfolio_val = 0
        check_date = (start_date + timedelta(days=1)).strftime("%Y-%m-%d")
        for key in current_portfolio:
            if current_portfolio[key] != 0:
                current_portfolio_val += current_portfolio[key]*(yf.Ticker(key)).history(prepost = True, start = start_date, end = check_date).iloc[0]["High"]

        # Add/Subtract etfs if orders were made in the time period 
        # Create list copies so values can be removed from lists during iteration
        dow_orders_copy = dow_orders.copy()
        sp500_orders_copy = sp500_orders.copy()
        nasdaq_orders_copy = nasdaq_orders.copy()
        totalmarket_orders_copy = totalmarket_orders.copy()
        
        # Loop through orders lists in reverse order to start with the earliest dates
        for i in range(len(dow_orders_copy)-1, -1,-1):
            if datetime.strptime(dow_orders_copy[i][0],"%Y-%m-%d") <= start_date:
                dow_units += dow_orders_copy[i][1]
                sp500_units += sp500_orders_copy[i][1]
                nasdaq_units += nasdaq_orders_copy[i][1]
                totalmarket_units += totalmarket_orders_copy[i][1]
               
                # Remove orders from lists after they have been added
                dow_orders.remove(dow_orders_copy[i])
                sp500_orders.remove(sp500_orders_copy[i])
                nasdaq_orders.remove(nasdaq_orders_copy[i])
                totalmarket_orders.remove(totalmarket_orders_copy[i])
            else:
                break
        
        # Add etfs units if dividend events occured in the time period 
        dow_units, dow_dividends = add_dividends(start_date, dow_dividends, dow_units, dividend_cutoff, yf.Ticker("DIA"))
        sp500_units, sp500_dividends = add_dividends(start_date, sp500_dividends, sp500_units, dividend_cutoff, yf.Ticker("SPY"))
        nasdaq_units, nasdaq_dividends = add_dividends(start_date, nasdaq_dividends, nasdaq_units, dividend_cutoff, yf.Ticker("QQQ"))
        totalmarket_units, totalmarket_dividends = add_dividends(start_date, totalmarket_dividends, totalmarket_units, dividend_cutoff, yf.Ticker("VTI"))
        
        # Apply etf fees on the first week of each year
        if start_date.year != (start_date - timedelta(days=28)):
            dow_units *= (1-dow_fees)
            sp500_units *= (1-sp500_fees)
            nasdaq_units *= (1-nasdaq_fees)
            totalmarket_units *= (1-totalmarket_fees)
        
        # Calculate current etf portfolio values and compare to RH portfolio
        dow_val = dow_units*yf.Ticker("DIA").history(prepost = True, start = start_date, end = check_date).iloc[0]["High"]
        sp500_val = sp500_units*yf.Ticker("SPY").history(prepost = True, start = start_date, end = check_date).iloc[0]["High"]
        nasdaq_val = nasdaq_units*yf.Ticker("QQQ").history(prepost = True, start = start_date, end = check_date).iloc[0]["High"]
        totalmarket_val = totalmarket_units*yf.Ticker("VTI").history(prepost = True, start = start_date, end = check_date).iloc[0]["High"]
        
        dow_performance_values.append(100*(current_portfolio_val - dow_val)/current_portfolio_val)
        sp500_performance_values.append(100*(current_portfolio_val - sp500_val)/current_portfolio_val)
        nasdaq_performance_values.append(100*(current_portfolio_val - nasdaq_val)/current_portfolio_val)
        totalmarket_performance_values.append(100*(current_portfolio_val - totalmarket_val)/current_portfolio_val)
        plot_dates.append(start_date)
        
        # Plot at 4 week increments
        start_date += timedelta(days=28)
    
    # Plot performance graphs
    plt.plot(plot_dates, dow_performance_values, label = "Dow")
    plt.plot(plot_dates, sp500_performance_values, label = "S&P 500")
    plt.plot(plot_dates, nasdaq_performance_values, label = "NASDAQ")
    plt.plot(plot_dates, totalmarket_performance_values, label = "Total Market")
    plt.xlabel('Date') 
    plt.ylabel('Performance Relative to ETF Portfolios (%)') 
    plt.title('Investment Strategy Performance Assessment') 
    plt.legend()
    plt.show()
    
    
    # Output summary statistics
    print("Current Portfolio Value: $" + str(round(current_portfolio_val,3)))
    print("Current DIA Hypothetical Portfolio Value: $" + str(round(dow_val,3)))
    print("Current SPY Hypothetical Portfolio Value: $" + str(round(sp500_val,3)))
    print("Current QQQ Hypothetical Portfolio Value: $" + str(round(nasdaq_val,3)))
    print("Current VTI Hypothetical Portfolio Value: $" + str(round(totalmarket_val,3)))
    
    return