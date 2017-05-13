#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 12 19:41:47 2017

@author: rhdzmota
"""

# %% imports 

import numpy  as np
import pandas as pd

import data_operations as do 


# %% Reference variables 

# max number of trajectories 
horizontal_limit = 50000

# max number of years 
years = 5

# %% KDE density estimator

def getTheKDE(datapoints):
    """
    Get the kernel density estimator of a given vector.
    
    -- inputs:
        datapoints: numpy array (1 dimension)
        
    -- outputs:
        kde: kernel estimator object
    """
    from sklearn.neighbors import KernelDensity
    
    # create and train the Kernel Density 
    kde = KernelDensity(kernel='gaussian',bandwidth=0.3).fit(
        datapoints.reshape(-1, 1))
    
    return kde


# %% Monte-Carlo Simulations 

def mTrajectoriesKde(stock,S0=None,T=years,n=years*360,m=horizontal_limit):
    
    # import translator
    ticker2yahoo = np.load("ticker2yahoo.npy").item()
    
    # get the stock historic return 
    returns = pd.read_pickle("db/returns.pickle")[ticker2yahoo[stock]]
    kde = getTheKDE(returns.values)
    
    S0 = (pd.read_pickle("db/prices.pickle")[ticker2yahoo[stock]].values[-1] if S0 is None else S0)
    
    def generateRandom(n):
        return list(kde.sample(n).reshape(n,))
    
    # generate random numbers 
    rnd = list(map(lambda x: generateRandom(n),range(m)))
    
    # logarithmic increment and path 
    log_increment = [np.concatenate([np.array([np.log(S0)]),i]) for i in rnd]
    log_path      = [np.cumsum(i) for i in log_increment]
    
    return pd.DataFrame(np.asmatrix([np.exp(i) for i in log_path]).T)

def mTrajectoriesNormal(stock,S0=None,mu=None,sigma=None,T=years,n=years*360,m=horizontal_limit):
    
    # import translator
    ticker2yahoo = np.load("ticker2yahoo.npy").item()
    
    # get the stock historic return 
    returns = pd.read_pickle("db/returns.pickle")[ticker2yahoo[stock]]
    mu = 360*returns.mean() if mu is None else mu
    sigma = np.sqrt(360)*returns.std() if sigma is None else sigma 
    
    # last price 
    S0 = (pd.read_pickle("db/prices.pickle")[ticker2yahoo[stock]].values[-1] if S0 is None else S0)
    
    dt = T/n
    mu_t, sigma_t = (mu-sigma**2/2)*dt, sigma*np.sqrt(dt)
    rnd = list(map(lambda x: np.random.normal(mu_t,sigma_t,n),range(m)))
    log_increment = [np.concatenate([np.array([np.log(S0)]),i]) for i in rnd]
    log_path      = [np.cumsum(i) for i in log_increment]
    return pd.DataFrame(np.asmatrix([np.exp(i) for i in log_path]).T) 

# %% Get simulations 

def getSimulation(ticker,kind='kde',n=360,m=100):
    """
    Assuming that the simulations files have been created. 
    """
    
    filename = "db/future_simulations/{}_based/{}.pickle".format(kind,ticker)
    random_choice = np.random.randint(0,horizontal_limit,m)
    df = pd.read_pickle(filename)[list(random_choice)].iloc[:n]
    df.columns = np.arange(0,m)
    return df 

# %% Create plot

def simulateStock(ticker,kind,n=50,m=15,filename="montecarlo_stock_test.png"):
    
    # translate 2 yho
    ticker2yahoo = np.load("ticker2yahoo.npy").item()
    
    # read data
    prices = pd.read_pickle("db/prices.pickle")[[ticker2yahoo[ticker]]].iloc[-100:]
    
    # simulation
    simul = getSimulation(ticker,kind,n,m)
    
    # x-axis
    x = np.arange(len(prices.values))
    x = x - len(prices.values) + 1
               
    # mean trajectories
    mean_tr = simul.mean(1).values
    desvest = simul.std(1).values
    str_res = 'The expected value in {} days is: $ {:0.4f} MXN\nwith a standard deviation of: $ {:0.4f} MXN'.format(n,mean_tr[-1],desvest[-1])
    
    # parameters to plot 
    ymin = np.min([simul.min().min(),prices.values.min()])*0.75
    ymax = np.min([simul.max().max(),prices.values.max()])*1.25
    
    fig, ax = plt.subplots(nrows=2,ncols=1,figsize=(6,5))
    
    # FIRST PLOT 
    plt.subplot(2,1,1)
    
    plt.plot(x,prices.values)
    plt.axvline(x=0, alpha = 0.5, ls = '--')
    for i in simul:
        plt.plot(np.arange(len(mean_tr)),simul[i].values, '-b', alpha = 0.3)
    plt.plot(np.arange(len(mean_tr)),mean_tr, '-r', linewidth = 1)
    plt.ylim([ymin, ymax])
    plt.title("Monte-Carlo Simulation for {} using: {} distr.".format(ticker,kind))
    
    # SECOND PLOT  
    plt.subplot(4,1,4)
    plt.text(0.5,0.5,str_res,verticalalignment='center', horizontalalignment='center')
    plt.axis('off')
    
    #plt.show()
    plt.savefig(filename,dpi=500) 
    plt.close()
    
    return 1
# %% 

def montecarloStockPlot(text,sender):
    """montecarlo stock plot
    
    Simulate ALSEA (using kde)
    Simulate ALSEA for 30 days with 20 trajectories 
    Simulate ALSEA for 30 days with 20 trajectories using kde 
    """
    def detectKde(text):
        return ("kde" in text.lower())
    
    kind = "kde" if detectKde(text) else "normal"
    
    def getStockName(text):
        return text.split(" ")[1]
    
    # create filename 
    filename = 'montecarloStock_{}.png'.format(str(sender))
    
    try:
        
        # get dates and number of trajectories 
        trj  = 20 if not (("traj" in text.lower()) or ("with" in text.lower())) else int(text.split("with")[-1].split("using")[0].replace("trajectories","").replace(" ",""))    
        days = 30 if not (("days" in text.lower()) or ("for" in text.lower())) else int(text.split("for")[-1].split("days")[0].replace(" ","")) 
        
        status = simulateStock(ticker=getStockName(text),kind=kind,
                               n=days,m=trj,filename=filename)
    except:
        status = 0
        
    filename = filename if status else None 
    return filename
# %% 


# %% 


# %% 