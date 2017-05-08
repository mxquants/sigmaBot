#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  7 10:24:20 2017

@author: rhdzmota
"""

# %% Imports 

import numpy  as np
import pandas as pd 
import pandas_datareader.data as web

from time import sleep
from datetime import datetime, timedelta

# %% Load reference data 

def referenceNames():
    filenames = ['name2desc.npy','name2ticker.npy','ticker2yahoo.npy']
    temp = {}
    for k in filenames:
        temp[k.split('.')[0]] = np.load(k).item()
    return temp

def epsilon(sign=1):
    return sign*10**-10

# %% Download and save data 

def saveData():
    
    # time interval
    _to   = datetime.now()
    _from = _to - timedelta(days=360*2)
    
    # download function 
    def download(asset,df,recursive_limit=5):
        
        # recursive limit 
        if recursive_limit == 0:
            print('\t    Recursion Limit Reached. Data was not downloaded.\n')
            return df 
        
        # avoid Nones
        if asset is None:
            return df 
        
        # test if asset can be downloaded 
        try:
            if recursive_limit == 5:
                print('Downloading: {}'.format(asset))
            temp = web.DataReader(asset,"yahoo",_from,_to)
            temp = temp[["Adj Close"]]
            if np.std(temp.values) > epsilon(1):    
                temp.columns = [asset]
                df = pd.concat([df,temp],axis=1)
            print((' >> Variance cero! Problem!\n' if np.std(temp.values)==0 else ' >> :okay\n'))
        except:
            if recursive_limit == 5:
                print(" >> Something went wrong for: {}".format(asset))
                print(" >> Entering recursive download... ")
            print("\t >  iteration: {}".format(5-recursive_limit))
            sleep(2)
            df = download(asset,df,recursive_limit=recursive_limit-1)
            
        # return resulting dataframe
        return df
    
    prices = pd.DataFrame([])
    tickers= referenceNames()['ticker2yahoo']
    for k in tickers:
        prices = download(tickers[k],prices)
        
    # delete nans and save 
    prices.dropna(axis=1,inplace=True)
    prices.to_pickle("db/prices.pickle")
    return 1

# %% Get prices

def getPrices():
    
    # read from database
    prices = pd.read_pickle('db/prices.pickle')
    return prices

def getReturns():
    
    # Logarithmic returns 
    def calculateReturns(ordered_vector):
        ordered_vector = np.asarray(ordered_vector)
        return np.log(ordered_vector[1:]/ordered_vector[:-1])
    
    # stock prices
    prices = getPrices()
    
    # calculate returns and save into pandas dataframe
    core = {}
    for stock in prices:
        core[stock] = calculateReturns(prices[stock].values)
        
    returns = pd.DataFrame(core,index=prices.index[1:])
    
    # save as pickle 
    returns.to_pickle("db/returns.pickle")
    returns.cov().to_pickle("db/covariance.pickle")

    # save into log
    returns_data = {}
    returns_data['annual_mean'] = 360*returns.mean()
    returns_data['annual_volatility'] = np.sqrt(360)*returns.std()
    returns_data['available_stocks']  = np.asarray(returns.columns)
    returns_data['dim']  = returns.shape

    np.save('db/returns_data.npy',returns_data)
    return returns 

def saveAvailableStocks():
    
    prices = getPrices()
    
    # dict of available data 
    available_data = {}
    available_data['stocks'] = np.asarray(prices.columns)
    available_data['dim']    = prices.shape
    available_data['from']   = prices.index.min().strftime('%Y/%m/%d')
    available_data['to']     = prices.index.max().strftime('%Y/%m/%d')
    
    np.save("db/available_data",available_data)
    return 1 

# %% 



# %%


# %% 


# %%


# %% 

# %% 

# %% 

# %% 