#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  8 19:06:44 2017

@author: rhdzmota
"""

# %% Imports 

import numpy as  np
import pandas as pd

from data_operations import referenceNames

# %% 

def availableStocks():
    """
    text = "Available Stocks"
    """
    n = len(list(referenceNames()['ticker2yahoo'].keys()))
    m = 20 
    return 'You can find most stocks in the BMV. Some examples: \n\n'+', '.join(list(pd.DataFrame({'names':list(referenceNames()['ticker2yahoo'].keys())}).iloc[np.random.randint(0,n,10)].values.reshape((10,))))
# %% 


# %% 


# %% 
list(pd.DataFrame({'names':list(referenceNames()['ticker2yahoo'].keys())}).iloc[np.random.randint(0,n,10)].values.reshape((10,)))

# %% 


# %% 


# %% 


# %% 


# %% 


# %% 