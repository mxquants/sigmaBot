#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 13 23:24:19 2017

@author: rhdzmota
"""

# %%  Imports 

import numpy as np
import pandas as pd
import scipy.optimize as sco

rf = 0.0629
# %% Objective functions 

def getPortfolioParameters(tickers,weights):
    
    # translator
    ticker2yahoo = np.load("ticker2yahoo.npy").item()
    
    # read returns 
    returns = pd.read_pickle("db/returns.pickle")[[ticker2yahoo[tic] for tic in tickers]]
    
    # mean returns
    rp = 360*sum(weights*returns.mean().values)
    sd = np.sqrt(360*np.asscalar((np.asmatrix(weights).dot(np.asmatrix(returns.cov()))).dot(np.asmatrix(weights).T)))
    
    return rp,sd

def simpleSharpe(rp,sd,rf=rf):
    return (rp-rf)/sd

def sharpeFunction(weights,tickers):
    
    rp,sd = getPortfolioParameters(tickers,weights)
    return simpleSharpe(rp,sd,rf)

# %% 

def objective(x,tickers):
    return -sharpeFunction(weights=x,tickers=tickers)

def cut2decimals(z):
    return int(100*z)/100

def findMaxSharpe(tickers):
    
    n = len(tickers)
    
    # args 
    args = (tickers)
    # constraints 
    constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    
    # bounds
    bounds = tuple( (0,1) for i in range(n))
    
    opts = sco.minimize(objective, n*[1./n,], method='SLSQP', bounds=bounds, constraints=constraints,args=args)
    
    result_string = """\

Maximum Sharpe portfolio 

>> Sharpe: {:0.4f}

>> Stocks: {}
>> Proportions: {} % 

""".format(sharpeFunction(opts.x,tickers=tickers),tickers,[cut2decimals(100*i) for i in opts.x])

    return result_string 

# %% 

def sharpeWrapper(text):
    """
    Get sharpe optimal portafolio using ALSEA ALFA GRUMA GMEXICO 
    """
    
    def getTickers(text):
        return [i.upper() for i in text.lower().split("using")[-1].replace(","," ").split(" ") if i != ""]
    
    tickers = getTickers(text)
    
    try:
        result = findMaxSharpe(tickers)
    except:
        result = "Error. Check your syntax."
        
    return result 

# %% 



# %% 



# %% 



# %% 



# %% 



# %% 



# %% 
