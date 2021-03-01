# -*- coding: utf-8 -*-
"""

@author: timpr
"""
import robin_stocks as r
from datetime import datetime
from dateutil import tz

def convert_dates(order_value_list, portfolio_dict):
    """
    Converts the timezone of the dates to match the timezones of robin_stocks output and yfinance output, then truncates dates to
    to match format of yfinance dataframe

    Returns
    -------
    order_value_list (List<List<string>): A list containing all order details. Each order represented in a list of the
                                          form [Date, Value]. Negative values represent a sale.
    portfolio_dict (Dict<string:float): A dictionary with stock tickers as keys and number of stock holdings as values

    Returns
    -------
    order_value_list (List<List<string>): Same as input order_value_list, with dates converted into required format
    portfolio_dict (Dict<string:float): As above, with dates converted into required format
    """
    base_zone = tz.gettz('UTC')
    required_zone = tz.gettz('America/New_York')
    
    for order in order_value_list:
        base_date = datetime.strptime(order[0][0:10] + " " + order[0][11:17] + "00", '%Y-%m-%d %H:%M:%S')
        base_date = base_date.replace(tzinfo = base_zone)
        converted_date = base_date.astimezone(required_zone)
        order[0] = converted_date.strftime('%Y-%m-%d')
    
    for key in portfolio_dict:
        for order in portfolio_dict[key]:
            base_date = datetime.strptime(order[0][0:10] + " " + order[0][11:17] + "00", '%Y-%m-%d %H:%M:%S')
            base_date = base_date.replace(tzinfo = base_zone)
            converted_date = base_date.astimezone(required_zone)
            order[0] = converted_date.strftime('%Y-%m-%d')
    
    return (order_value_list, portfolio_dict)


def get_order_history():
    """
    Pulls user buy and sell history from Robinhood

    Returns
    -------
    order_value_list (List<List<string>): A list containing all order details. Each order represented in a tuple of the
                                           form (Date, Value). Negative values represent a sale.
    portfolio_dict (Dict<string:float): A dictionary with stock tickers as keys and number of stock holdings as values

    """
    # A list to store information on all filled stock buys and sells
    order_value_list = []   
    portfolio_dict = {}
    order_list = r.orders.get_all_stock_orders(info=None)

    for order in order_list:
        # Search the ticker of the stock order and add as key to portfolio if needed
        order_ticker = r.get_symbol_by_url(order['instrument'])
        if order_ticker not in portfolio_dict:
            portfolio_dict[order_ticker] = []
        
        # Only include orders that were filled
        if order["state"] == "filled" and order["drip_dividend_id"] == None:    
            if order["side"] == "buy":
                portfolio_dict[order_ticker].append([order["last_transaction_at"],
                                                     float(order["cumulative_quantity"])])        
                # Only add/remove etfs for orders that aren't dividend reinvestments
                if order["drip_dividend_id"] == None:
                    order_value_list.append([order["last_transaction_at"], 
                                            float(order["cumulative_quantity"])*float(order["average_price"])])
            elif order["side"] == "sell":
                portfolio_dict[order_ticker].append([order["last_transaction_at"],
                                                     - float(order["cumulative_quantity"])])  
                if order["drip_dividend_id"] == None:
                    order_value_list.append([order["last_transaction_at"], 
                                             - float(order["cumulative_quantity"])*float(order["average_price"])])

    return(convert_dates(order_value_list, portfolio_dict))
