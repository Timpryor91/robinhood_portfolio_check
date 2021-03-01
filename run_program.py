# -*- coding: utf-8 -*-
"""

@author: timpr
"""
import robin_stocks as r

from modules.application_login import login
from modules.get_history import get_order_history
from modules.build_etf_lists import build_etf_lists
from modules.build_dividend_lists import build_dividend_lists
from modules.etf_fees import get_fee_data
from modules.plot_generator import generate_plots

# No interface for this one, only want users to be entering their RH password if they are comfortable with opening
# the code up in python and looking at it themself

if __name__ == "__main__":
    
    # Prompt user to enter login credentials to get access to the app
    login = login()    
    
    # Obtain purchase and sale history data, convert dates to required format
    order_value_list, portfolio_dict = get_order_history()
    
    # Obtain equivalent etf purchases/sales on dates of orders
    dow_orders, sp500_orders, nasdaq_orders, totalmarket_orders = build_etf_lists(order_value_list)
    
    # Obtain dividend history for ETFs
    dow_dividends, sp500_dividends, nasdaq_dividends, totalmarket_dividends, portfolio_dividend_dict = build_dividend_lists(portfolio_dict)
    
    # Obtain annual fee data for ETFs
    dow_fees, sp500_fees, nasdaq_fees, totalmarket_fees = get_fee_data()
        
    # Develop plot data and output summary statistics
    generate_plots(
                    dow_orders, 
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
                    )    
    
    r.authentication.logout()
    