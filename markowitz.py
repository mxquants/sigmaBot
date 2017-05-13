#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  7 17:59:56 2017

@author: rhdzmota
"""

# %% Imports 

import numpy as np
import pandas as pd

from data_operations import referenceNames

# %% Change directory 

#os.chdir("/media/rhdzmota/Data/Files/github_mxquants/sigmaBot")

# %% Functions to handle markowitz portfolio 

def randomPortfolio(returns):
    w = np.asmatrix(np.random.dirichlet(np.ones(returns.shape[1]),size=1)[0])#np.asmatrix(randomProp(returns.shape[1]))
    rp = w.dot(np.asmatrix(returns.mean().values).T)
    rp = np.asscalar(rp)
    
    varp = w.dot(np.asmatrix(returns.cov().values)).dot(w.T)
    varp = np.asscalar(varp)
    
    return rp, np.sqrt(varp)

def generateMultiplePortfolios(m,returns):
    results = {'rp':[],'std':[]}
    
    for i in range(m):
        temp = randomPortfolio(returns)
        results['rp'].append(100*temp[0])
        results['std'].append(100*temp[1])
        
    return pd.DataFrame(results)

def calculatePortfolio(w,returns):
    rp = w.dot(np.asmatrix(returns.mean().values).T)
    rp = np.asscalar(rp)
    
    varp = w.dot(np.asmatrix(returns.cov().values)).dot(w.T)
    varp = np.asscalar(varp)
    
    return 100*rp, 100*np.sqrt(varp)

# %%

def readReturns():
    return pd.read_pickle("db/returns.pickle")

# %% Marko

class Markowitz(object):
    
    def __init__(self):
        self.alpha2range = np.arange(1,500)
        self.port_opt    = None 
        
            
    def getSolutionMkw(self,returns,alpha_1=1,alpha_2=1):
        """
        Returns an optim.porfolio f
        """
        from cvxopt import matrix, solvers 
        
        solvers.options['show_progress'] = False
    
        # number of variables
        r = returns.shape[1]
        
        # mean and covariance
        _mean = returns.mean()
        _cov  = returns.cov()
    
        # parameters
        P = matrix(alpha_2*_cov.values)
        Q = matrix(-alpha_1*_mean.values)
        G = matrix(-1.*np.identity(r))
        h = matrix([0. for i in range(r)])
        A = matrix([1. for i in range(r)], (1,r))
        b = matrix(1.)
        
        # get solution
        sol = solvers.qp(P,Q,G,h,A,b)
        
        return np.asmatrix([i for i in sol['x']])
        
        
    def iterativeSelectionProcess(self,returns,w_opt_list=None,tolerance=0.05,alpha2range=np.arange(1,250)):
    
        if w_opt_list is None: 
            w_opt_list =  [self.getSolutionMkw(returns,alpha_2=a2) for a2 in alpha2range]
        
        save_sum = []
        for i in w_opt_list:
            temp = [i[0,j] for j in range(np.shape(i)[1])]
            save_sum = (save_sum + np.array(temp)) if len(save_sum)!=0 else np.array(temp)
    
        selection = pd.DataFrame(save_sum).apply(lambda x: x>tolerance).values
        cont = len(selection) - np.sum(selection)
        selection = [j for i,j in zip(selection,returns.columns) if i]
        self.selection = selection
        return returns[selection],cont,save_sum
    
    def getWeights(self,tickers='all'):
        condition = True
        w_opt_list = None 
        returns = pd.read_pickle("db/returns.pickle") if tickers=='all' else pd.read_pickle("db/returns.pickle")[tickers]
        while(condition):
            returns, cond, ss = self.iterativeSelectionProcess(returns,w_opt_list,tolerance=0.05*500)
            w_opt_list = [self.getSolutionMkw(returns,alpha_2=a2) for a2 in np.arange(1,500)]
            condition = False if cond == 0 else condition
        
        self.returns = returns
        self.w_opt_list = w_opt_list
    
    def simulateRandPort(self):
        self.portfolios = generateMultiplePortfolios(2000,self.returns)
        
    def generateEfficientFrontier(self):
        port_opt = []
        for i in self.w_opt_list:
            port_opt.append(calculatePortfolio(i,self.returns))
            
        self.port_opt = pd.DataFrame(port_opt)
        self.port_opt.columns = ['returns','volatility']
        self.port_opt.index = self.alpha2range
        
    def getItDone(self,tickers='all'):
        self.getWeights(tickers)
        self.simulateRandPort()
        self.generateEfficientFrontier()
        
    def getEfficientPortfolio(self,tickers='all',percentile=100,_as="text"):
        
        if self.port_opt is None or type(tickers) != "all": 
            self.getItDone(tickers)
            
        lenght = len(self.port_opt)
        select = int(np.percentile(np.arange(lenght),percentile))
        
        # portfolio charateristics
        desc = self.port_opt.iloc[[select]]
        weights = pd.DataFrame(100*self.w_opt_list[select],columns=self.returns.columns,index=[select])
        
        if _as == "text":
            title  = "{} percentile of the Markowitz efficient frontier (orderded from more risky to least risky).\n\n"
            intro  = "From the stocks you provided, this are the most relevant ones with their correpondent weight: \n\n"
            middle = "\n\nDaily  returns and volatility:\n"
            middle2= "\n\nAnnual return and colatility:\n"
            return title.format(percentile)+intro+str(weights)+middle+str(desc)+middle2+str(360*desc)
        return None
        
        
        
    def plot(self,tickers='all',filename=''):
        import matplotlib.pyplot as plt 
        
        if self.port_opt is None: 
            self.getItDone(tickers)
        
        fig = plt.figure(figsize=(10,7))
        ax = fig.add_subplot(111)
        
        fig.suptitle('Markowitz Portfolio Theory - Combinations and Efficient Frontier', fontsize=14, fontweight='bold')
        #self.portfolios.plot(kind='scatter',x='std',y='rp',grid=True,figsize=(10,7))
        ax.scatter(self.portfolios['std'],self.portfolios['rp'],s=7) # ,'b.',alpha=0.6
        ax.plot(self.port_opt['volatility'],self.port_opt['returns'],'r-')
        ax.scatter(self.port_opt['volatility'].iloc[0], self.port_opt['returns'].iloc[0], c='g',s=100)
        ax.scatter(self.port_opt['volatility'].iloc[-1],self.port_opt['returns'].iloc[-1],c='y',s=100)
        
        plt.title('Relevant stocks used: {}'.format(str(self.selection)))
        plt.xlabel('Daily Volatility (%)')
        plt.ylabel('Daily log-returns (%)')
        plt.grid()
        
        plt.savefig(filename,dpi=500) 
        plt.close()
        #plt.show()
        
# %% Test
def markowitzSimplePlotWrapper(text,sender):
    """
    text = "create markowitz plot with ALSEA, GRUMAB, ... / all data"
    text = "get efficient portfolio using ALSEA, GRUMAB, ..."
    text = "get p from efficient frontier using ALSEA, GRUMAB"
    """
    
    def getYahoo(ticker):
        if '.MX' in ticker:
            return ticker
        return referenceNames()['ticker2yahoo'][ticker]
    
    def getStockList(text):
        if "all data" in text:
            return "all"
        return [getYahoo(i.upper()) for i in text.lower().split('with')[-1].replace(',',' ').split(' ') if i != ""]
    
    
    
    # create filename 
    filename = 'markplot_{}.png'.format(str(sender))
    
    try:
        Mark = Markowitz()
        Mark.plot(tickers=getStockList(text),filename=filename)
    except:
        filename = None 
    
    return filename 


# %%

def getMarkowitzPortfolioFromFrontier(text):
    """
    Get percentile 10 portfolio from efficient fronteir using all data. 
    """
    
    def getYahoo(ticker):
        if '.MX' in ticker:
            return ticker
        return referenceNames()['ticker2yahoo'][ticker]
    
    def getStockList(text):
        if "all data" in text:
            return "all"
        return [getYahoo(i.upper()) for i in text.lower().split('using')[-1].replace(',',' ').split(' ') if i != ""]
   
    def getPercentile(text):
        return int(text.split("percentile")[-1].split("port")[0].replace(" ",""))
        
    try:
        Mark = Markowitz()
        res = Mark.getEfficientPortfolio(tickers=getStockList(text),percentile=getPercentile(text))
    except: 
        res = "Something went wrong and I couldn't handle your request!"
        
    return res 

def getEfficientPort(text):
    """
    Get markowitz efficient portfolio using all data .
    """
    
    def changeString(text):
        return "percentile 100 "+"port"+text.split("port")[-1]
    
    return getMarkowitzPortfolioFromFrontier(changeString(text))
# %% 

# %% 