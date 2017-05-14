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
horizontal_limit = 1000

# max number of years 
years = 1

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
    kde = KernelDensity(kernel='gaussian',bandwidth=0.000001).fit(
        datapoints.reshape(-1, 1))
    
    return kde

def getKDE(returns):
    random_variable = returns.plot(kind='kde')
    x_val, y_val    = random_variable.get_children()[0]._x, random_variable.get_children()[0]._y
    random_variable = pd.DataFrame({'x':x_val,'density':y_val})
        
    # Calculate the cummulative distribution 
    acum = 0
    acum_vect = []
    for d in random_variable.density:
        acum += d
        acum_vect.append(acum)
    
    # Save into dataframe 
    random_variable['cumulative'] = np.array(acum_vect)/acum
                   
    plt.close()
    return random_variable
        
def getRandomValue(reference):
    unif = np.random.uniform()
    index = sum(reference.cumulative < unif)
    return reference.x.iloc[index]

def getRandomVect(n,reference):
    return np.array([getRandomValue(reference) for i in range(n)])

# %% Monte-Carlo Simulations 
# pd.DataFrame({"k":kde.sample(1000).reshape(1000,)}).plot() 
def mTrajectoriesKde(stock,S0=None,T=years,n=years*360,m=horizontal_limit,zero_mean=False):
    
    n = int(n)
    # import translator
    ticker2yahoo = np.load("ticker2yahoo.npy").item()
    
    # get the stock historic return 
    returns = pd.read_pickle("db/returns.pickle")[ticker2yahoo[stock]]
    returns_mean = returns.values.mean()
    kde = getTheKDE(returns.values - (zero_mean*returns_mean))
    
    S0 = (pd.read_pickle("db/prices.pickle")[ticker2yahoo[stock]].values[-1] if S0 is None else S0)
    
    def generateRandom(n,x):
        return list(kde.sample(n,random_state=x).reshape(n,))
    
    # generate random numbers 
    rnd = list(map(lambda x: generateRandom(n,x=x),range(m)))
    #reference = getKDE(returns)
    #rnd = list(map(lambda x: getRandomVect(n,reference),range(m)))
    
    # logarithmic increment and path 
    log_increment = [np.concatenate([np.array([np.log(S0)]),i]) for i in rnd]
    log_path      = [np.cumsum(i) for i in log_increment]
    
    return pd.DataFrame(np.asmatrix([np.exp(i) for i in log_path]).T) 

def mTrajectoriesNormal(stock,S0=None,mu=None,sigma=None,n=years*360,m=horizontal_limit,zero_mean=False):
    
    n = int(n)
    # import translator
    ticker2yahoo = np.load("ticker2yahoo.npy").item()
    
    # get the stock historic return 
    returns = pd.read_pickle("db/returns.pickle")[ticker2yahoo[stock]]
    mu = 360*returns.mean() if not zero_mean else 0
    sigma = np.sqrt(360)*returns.std() if sigma is None else sigma 
    
    # last price 
    S0 = (pd.read_pickle("db/prices.pickle")[ticker2yahoo[stock]].values[-1] if S0 is None else S0)
    
    T = n/360
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
    read_file = False 
    if read_file:
        filename = "db/future_simulations/{}_based/{}.pickle".format(kind,ticker)
        random_choice = np.random.randint(0,horizontal_limit,m)
        df = pd.read_pickle(filename)[list(random_choice)].iloc[:n]
        df.columns = np.arange(0,m)
        return df 
    
    if kind=="normal":
        f = mTrajectoriesNormal
    else:
        f = mTrajectoriesKde
        
    return f(stock=ticker,n=n,m=m)

# %% Create plot

def simulateStock(ticker,kind,n=50,m=15,filename="montecarlo_stock_test.png"):
    import matplotlib.pyplot as plt 
    # translate 2 yho
    ticker2yahoo = np.load("ticker2yahoo.npy").item()
    
    # read data
    prices  = pd.read_pickle("db/prices.pickle")[[ticker2yahoo[ticker]]].iloc[-100:]
    returns = pd.read_pickle("db/returns.pickle")[[ticker2yahoo[ticker]]]
    # simulation
    simul = getSimulation(ticker,kind,n,m)
    
    # x-axis
    x = np.arange(len(prices.values))
    x = x - len(prices.values) + 1
               
    # mean trajectories
    mean_tr = simul.mean(1).values
    desvest = simul.std(1).values
    str_res = """\
Using {} trajectories under {} dist.
the expected value at {} days is
$ {:0.4f} MXN with a standard 
deviation of $ {:0.4f} MXN. 
    """.format(m,kind,n,mean_tr[-1],desvest[-1])
    
    #'The expected value in {} days is: $ {:0.4f} MXN\nwith a standard deviation of: $ {:0.4f} MXN'.format(n,mean_tr[-1],desvest[-1])
    
    # parameters to plot 
    ymin = np.min([simul.min().min(),prices.values.min()])*0.75
    ymax = np.min([simul.max().max(),prices.values.max()])*1.25
    
    fig, ax = plt.subplots(nrows=2,ncols=1,figsize=(7,5))
    
    # FIRST PLOT 
    plt.subplot(2,1,1)
    
    plt.plot(x,prices.values)
    plt.grid()
    plt.axvline(x=0, alpha = 0.85, ls = '--')
    for i in simul:
        plt.plot(np.arange(len(mean_tr)),simul[i].values, '-b', alpha = 0.3)
    plt.plot(np.arange(len(mean_tr)),mean_tr, '-r', linewidth = 1)
    plt.ylim([ymin, ymax])
    plt.title("Monte-Carlo Simulation for {} using: {} distr.".format(ticker,kind))
    plt.ylabel("Price-level")
    
    # SECOND PLOT  
    plt.subplot(3,2,6)
    plt.text(0.5,0.5,str_res,verticalalignment='center', horizontalalignment='center')
    plt.axis('off')
    
    # THIRD SUBPLOT
    plt.subplot(3,2,5)
    plt.hist(returns.values,bins=50)
    plt.title("Histogram of returns")
    plt.xlabel("Log-Returns")
    plt.ylabel("Frequency")
    #plt.grid()
    #plt.show()
    plt.savefig(filename,dpi=500) 
    plt.close()
    
    return 1

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
        return text.split(" ")[1].upper()
    
    # create filename 
    filename = 'montecarloStock_{}.png'.format(str(sender))
    warning  = None 
    try:
        
        # get dates and number of trajectories 
        trj  = 20 if not (("traj" in text.lower()) or ("with" in text.lower())) else int(text.split("with")[-1].split("using")[0].replace("trajectories","").replace(" ",""))    
        days = 30 if not (("days" in text.lower()) or ("for" in text.lower())) else int(text.split("for")[-1].split("days")[0].replace(" ","")) 
        
        if (trj > horizontal_limit) or (days > 360*years):
            warning = "Hey, I can only simulates {} trajectories for {} days max! Try again with lower parameters.".format(horizontal_limit,360*years)
        
        if warning is None:
            status = simulateStock(ticker=getStockName(text),kind=kind,
                                   n=days,m=trj,filename=filename)
        else:
            status = 0
    except:
        warning = "Something happened."
        status = 0
        
    filename = filename if status else None 
    return filename, warning
# %% PORTFOLIO SIMULATION NORMAL

def simulateNormalPort(tickers,T=years,m=horizontal_limit):
    
    n = int(360*T)
    
    # translate 2 yho
    ticker2yahoo = np.load("ticker2yahoo.npy").item()
    
    # get stock names 
    stocks = list(map(lambda x: ticker2yahoo[x],tickers))
    
    # read initial prices and returns 
    returns = pd.read_pickle("db/returns.pickle")[stocks]
    S0 = list(pd.read_pickle("db/prices.pickle")[stocks].iloc[[-1]].values[0])
    
    # get mean, covariance
    mu = returns.mean().values
    cov= returns.cov().values
    
    
    sigma = [np.sqrt(cov[i][i]) for i in range(len(mu))]
    v = np.linalg.cholesky(cov)
    
    # calculate correlated random numbers
    def generateCorrNumbers(v,nvar,length):
        z_corr = np.asmatrix(v).T.dot(np.asmatrix(np.random.normal(0,1,size=(nvar,length))))
        return np.asarray(z_corr)
    
    # function to generate a single trajectory 
    def generateTraj(S0,mu,sigma,T,n,random_list):
        dt = T/n
        mu_t, sigma_t = (mu-sigma**2/2)*dt, sigma*np.sqrt(dt)
        random_list = mu_t + sigma_t*np.asarray(random_list)
        log_increment = [np.log(S0)]+[i for i in random_list]#np.concatenate([np.array([np.log(S0)]),np.array()])
        log_path      = np.cumsum(log_increment)
        return np.exp(log_path)
      
    random_numbers=[generateCorrNumbers(v,len(mu),n) for i in range(m)]
    
    _stocks = [[] for i in range(len(mu))]
    for rnd in random_numbers:
        for i in range(len(mu)):
            _stocks[i].append(generateTraj(S0[i],mu[i],sigma[i],T,n,rnd[i]))
            
        
    return [pd.DataFrame(np.asmatrix(s).T) for s in _stocks]

def plotNormalPort(capital,tickers,weights,T=years,m=horizontal_limit):
    import matplotlib.pyplot as plt
    
    # get simulated stocks 
    simulation = simulateNormalPort(tickers,T,m)
    
    # get initial number of stocks
    ticker2yahoo = np.load("ticker2yahoo.npy").item()
    stocks = list(map(lambda x: ticker2yahoo[x],tickers))
    last_prices = pd.read_pickle("db/prices.pickle")[stocks].iloc[[-1]].values[0]
    n_stocks = list(map(lambda x: np.int(x),np.array(weights)*capital / last_prices))
    
    # get remanent
    remanent = capital - np.sum(np.array(n_stocks)*last_prices)
    
    # get values 
    port_value = np.array(m*[0])
    port_vect = []
    c = 1
    for i,j in zip(simulation,n_stocks):
        if len(port_vect) == 0:
            port_vect  = j*i
        else:
            port_vect = port_vect+j*i
        port_value = port_value + j*i.iloc[-1,:].values
        c += 1
    
    temp = port_vect.iloc[-1] + remanent
    result_string = 'Information at maturity.\n\n\t> Min value: {}\n\t> Max value: {}\n\t> Mean: {}\n\t> Std: {}'.format(
            temp.min(),temp.max(),temp.mean(),temp.std())
    
    for tr in port_vect:
        one = port_vect[tr] + remanent
        plt.plot(np.arange(len(one)),one,alpha=0.7)
    plt.plot(port_vect.mean(1).values+remanent,'r')
    plt.title('Portfolio Simulation assuming normal correlated variables')
    plt.xlabel("Days")
    plt.ylabel("Value (in MXN)")
    plt.grid(True)
    
    plt.show()
    
    
# Simulate porfolio given by [] with weights [] and initial capital of []    
# %% 
def mTrajectoriesPortKde(data,T=years,n=years*360,m=horizontal_limit):
    

    kde = getTheKDE(data["port_return"])
    
    S0 = data['port_value'][-1]
    
    def generateRandom(n,x):
        return list(kde.sample(n,random_state=x).reshape(n,))
    
    # generate random numbers 
    rnd = list(map(lambda x: generateRandom(n,x=x),range(m)))
    #reference = getKDE(returns)
    #rnd = list(map(lambda x: getRandomVect(n,reference),range(m)))
    
    # logarithmic increment and path 
    log_increment = [np.concatenate([np.array([np.log(S0)]),i]) for i in rnd]
    log_path      = [np.cumsum(i) for i in log_increment]
    
    return pd.DataFrame(np.asmatrix([np.exp(i) for i in log_path]).T)


def simulateKdePort(tickers,n_stocks,T=years,m=horizontal_limit):
    
    n = int(360*T)
    
    # translate 2 yho
    ticker2yahoo = np.load("ticker2yahoo.npy").item()
    
    # get stock names 
    stocks = list(map(lambda x: ticker2yahoo[x],tickers))
    
    # get prices
    prices = pd.read_pickle("db/prices.pickle")[stocks]
    
    # get port value 
    port_value = prices.apply(lambda x: np.sum([i*j for i,j in zip(x,n_stocks)]),1).values
    port_return= np.log(port_value[1:]/port_value[:-1])
    
    # get simulations 
    data = {"port_value":port_value,"port_return":port_return}
    simulations = mTrajectoriesPortKde(data,T,n,m)
    
    return simulations

    

def plotKdePort(capital,tickers,weights,T=years,m=horizontal_limit):
    import matplotlib.pyplot as plt
    
    # get initial number of stocks
    ticker2yahoo = np.load("ticker2yahoo.npy").item()
    stocks = list(map(lambda x: ticker2yahoo[x],tickers))
    last_prices = pd.read_pickle("db/prices.pickle")[stocks].iloc[[-1]].values[0]
    n_stocks = list(map(lambda x: np.int(x),np.array(weights)*capital / last_prices))
    
    remanent = capital - np.sum(np.array(n_stocks)*last_prices)
    
    simulations = simulateKdePort(tickers,n_stocks,T,m)
    for tr in simulations:
        one = simulations[tr] + remanent
        plt.plot(np.arange(len(one)),one,alpha=0.7)
    plt.plot(simulations.mean(1).values + remanent,'r')
    plt.title('Portfolio Simulation with KDE estimation')
    plt.xlabel("Days")
    plt.ylabel("Value (in MXN)")
    plt.grid(True)
    
    plt.show()
    


# %%

def plotPortBothMethods(filename,capital,tickers,weights,T=years,m=horizontal_limit):
    import matplotlib.pyplot as plt
    
    # get initial number of stocks
    ticker2yahoo = np.load("ticker2yahoo.npy").item()
    stocks = list(map(lambda x: ticker2yahoo[x],tickers))
    last_prices = pd.read_pickle("db/prices.pickle")[stocks].iloc[[-1]].values[0]
    n_stocks = [int(np.float(w)*np.float(capital)/np.float(p)) for w,p in zip(weights,last_prices)]#list(map(lambda x: np.int(x),np.array(weights)*capital / last_prices))
    
    remanent = capital - np.sum(np.array(n_stocks)*last_prices)
    
    # get simulated stocks 
    normal_simulation = simulateNormalPort(tickers,T,m)
    kde_simulations = simulateKdePort(tickers,n_stocks,T,m)
    
    # Create plot     
    fig, ax = plt.subplots(nrows=2,ncols=1,figsize=(9,9))
    
    # Normal plot 
    plt.subplot(3,1,1)
    
    
    # get values 
    port_value = np.array(m*[0])
    port_vect = []
    c = 1
    for i,j in zip(normal_simulation,n_stocks):
        if len(port_vect) == 0:
            port_vect  = j*i
        else:
            port_vect = port_vect+j*i
        port_value = port_value + j*i.iloc[-1,:].values
        c += 1
    
    temp = port_vect.iloc[-1] + remanent
    #result_string = 'Information at maturity.\n\n\t> Min value: {}\n\t> Max value: {}\n\t> Mean: {}\n\t> Std: {}'.format(
    #        temp.min(),temp.max(),temp.mean(),temp.std())
    
    for tr in port_vect:
        one = port_vect[tr] + remanent
        plt.plot(np.arange(len(one)),one,alpha=0.7)
    plt.plot(port_vect.mean(1).values+remanent,'r')
    plt.title('Portfolio Simulation assuming normal correlated variables')
    plt.ylabel("Value (in MXN)")
    plt.grid(True)
    
    
    # KDE plot
    plt.subplot(3,1,2)
    
    for tr in kde_simulations:
        one = kde_simulations[tr] + remanent
        plt.plot(np.arange(len(one)),one,alpha=0.7)
    plt.plot(kde_simulations.mean(1).values + remanent,'b')
    plt.title('Portfolio Simulation with KDE estimation')
    plt.xlabel("Days")
    plt.ylabel("Value (in MXN)")
    plt.grid(True)
    
    
    plt.subplot(3,1,3)
    
    prop_normal = 100*np.sum(temp > capital) / m
    prop_kde    = 100*np.sum(kde_simulations.iloc[-1] > capital) / m
    
    res_str = """\
Probability of generating returns (final value > initial capital):
    
    Using Normal Assumptions: {:0.4f} %
    Using Kernel Density Estimatior: {:0.4f} %
""".format(prop_normal,prop_kde)
             
    plt.text(0.5,0.5,res_str,verticalalignment='center', horizontalalignment='center')
    plt.axis('off')             
                            
    plt.savefig(filename,dpi=100) 
    plt.close()
    
    return 1

def plotPortWithBothMethods(text,sender):
    """
    Simulate porfolio given by [] with weights [] and initial capital of []    
    """
    
    def getStockList(text):
        return [i.upper() for i in text.split("with")[0].split("by")[-1].replace(","," ").split(" ") if i != ""]
    
    def getWeights(text):
        return [i.upper() for i in text.split("and")[0].split("weights")[-1].replace(","," ").split(" ") if i != ""]
    
    def getCapital(text):
        return np.float(text.split(" of")[-1])
    
    
    filename = 'port_simul_{}.png'.format(str(sender))
    warning  = None
    
    try:
        
        capital  = getCapital(text)
        weights  = getWeights(text)
        tickers  = getStockList(text)
        
        status = plotPortBothMethods(filename,capital,tickers,weights,T=1/3,m=100)
        
    except: 
        warning = "Something happened."
        status = 0
        
    
    filename = filename if status else None 
    return filename, warning


# %% 
#plotBothMethods(capital,tickers,weights,T=1/2,m=500)

# %%  