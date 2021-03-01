# -*- coding: utf-8 -*-
"""

@author: timpr
"""

import robin_stocks as r

def login():
    """
    Logins in to robinhood account using username and password. If multi-factor authentication
    is enabled, will send a message to users MFA device (e.g. phone)

    Parameters
    ----------
    None

    Returns
    -------
    None

    """
    
    username = input("Please enter your RH username: ")
    password = input("Please enter your RH password: ")
    r.authentication.login(username, password)

    return

