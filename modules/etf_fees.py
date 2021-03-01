# -*- coding: utf-8 -*-
"""

@author: timpr
"""

def get_fee_data():
    """
    Returns the annual fee percentages for the ETFs. Was unable to find historical variation in these fees, so assuming current
    values for the full length of the analysis period

    Returns
    -------
    dow_fees (float): the annual fee percentage (expressed as a proportion) charged for DIA ETFs
    sp500_fees (float): the annual fee percentage (expressed as a proportion) charged for DIA ETFs
    nasdaq_fees (float): the annual fee percentage (expressed as a proportion) charged for DIA ETFs
    totalmarket_fees (float): the annual fee percentage (expressed as a proportion) charged for DIA ETFs

    """
    dow_fees = 0.16/100
    sp500_fees = 0.095/100
    nasdaq_fees = 0.2/100
    totalmarket_fees = 0.04/100
    
    return (dow_fees, sp500_fees, nasdaq_fees, totalmarket_fees)
