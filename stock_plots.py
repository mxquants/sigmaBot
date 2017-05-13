#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  8 19:06:44 2017

@author: rhdzmota
"""

# %% Imports 

import numpy as  np
import pandas as pd

from data_operations import referenceNames,trulyAvailableStocks

# %% 

def availableStocks():
    """
    text = "Available Stocks"
    """
    n = len(trulyAvailableStocks())#len(list(referenceNames()['ticker2yahoo'].keys()))
    m = 20 
    return 'You can find most stocks in the BMV. Some examples: \n\n'+', '.join(list(pd.DataFrame({'names':list(referenceNames()['ticker2yahoo'].keys())}).iloc[np.random.randint(0,n,m)].values.reshape((m,))))


# %% 

def stockPlot(tickers,filename):
    import matplotlib.pyplot as plt 
    
    def getYahoo(ticker):
        ticker = ticker.upper()
        if '.MX' in ticker:
            return ticker
        return referenceNames()['ticker2yahoo'][ticker]  
    
    prices  = pd.read_pickle("db/prices.pickle")[list(map(getYahoo,tickers))]
    returns = pd.read_pickle("db/returns.pickle")[list(map(getYahoo,tickers))]
    
    fig, ax = plt.subplots(nrows=2,ncols=1,figsize=(10,7))
    
    
    #fig.suptitle('Historic prices for: {}'.format(tickers), fontsize=14, fontweight='bold')
    
    # FIRST PLOT 
    plt.subplot(2,1,1)
    for col in prices:
        plt.plot(prices.index,prices[col].values,label=col)
        
    plt.title('Historic prices for: {}'.format(tickers))
    plt.legend()
    #plt.xlabel('Date')
    plt.ylabel('MXN')
    plt.grid()
    
    # SECOND PLOT 
    plt.subplot(4,1,3)
    for col in prices:
        plt.plot(returns.index,returns[col].values,label=col)
    #plt.plot(prices.index,prices[col].values,label=col)
    
    #plt.legend()
    #plt.title("Log-Returns for selected stocks")
    plt.xlabel('Date')
    plt.ylabel('log-returns')
    plt.grid()
    
    # Information 
    plt.subplot(4,1,4)
    plt.text(0.5,0.5,'Last price: \n{}'.format(prices.iloc[-1]),verticalalignment='center', horizontalalignment='center')
    plt.axis('off')
    
    #plt.show()
    
    
    plt.savefig(filename,dpi=100) 
    plt.close()
    
    return 1 
    
    
    

# %% 

def stockPlotWrapper(text,sender):
    """
    plot STOCK
    """
    
    def getStockNames(text):
        return [i.upper() for i in text.lower().replace('plot','').replace(',',' ').split(' ') if i != ""]
        
    # create filename 
    filename = 'stockplot_{}.png'.format(str(sender))
    
    try:
        status = stockPlot(tickers=getStockNames(text),filename=filename)
    except:
        status = 0
        
    filename = filename if status else None 
    return filename


# %% 
"""
def covariancePlot():
    stocks = ['GENTERA.MX', 'GFINBURO.MX', 'GFINTERO.MX']
    
    # read returns 
    returns = pd.read_pickle("db/returns.pickle")[stocks]

    # calculate covariance matrix
    covar = returns.cov()
    
    plt.imshow(covar,cmap='hoy')
"""
# %% 

def covarPlot(tickers,filename):
    """
    Plot covariance of ALSEA GMEXICO 
    """
    import seaborn as sns
    import matplotlib.pyplot as plt
    

    
    # read returns and calulate covar
    returns = pd.read_pickle("db/returns.pickle")[tickers]
    covar   = returns.cov()
    
    # create heatmap 
    sns.heatmap(covar)
    plt.title("Covariance Heat Plot")
    
    # save figure
    plt.savefig(filename,dpi=500) 
    plt.close()
    
    return 1
    

def covarPlotWrapper(text,sender):
    """
    plot STOCK
    """
    
    # translator
    ticker2yahoo = np.load("ticker2yahoo.npy").item()
    
    def getStocks(text):
        return [ticker2yahoo[i.upper()] for i in text.
                             lower().split("of ")[-1].replace(","," ").
                             split(" ") if i != ""]
        
    # create filename 
    filename = 'covarplot_{}.png'.format(str(sender))
    
    try:
        status = covarPlot(tickers=getStocks(text),filename=filename)
    except:
        status = 0
        
    filename = filename if status else None 
    return filename
# %% 


# %% 


# %% 


# %% 


# %% 