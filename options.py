#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 14 01:15:57 2017

@author: rhdzmota
"""
# %% Imports 



#import os
#os.chdir('/media/rhdzmota/Data/Files/github_mxquants/sigmaBot')

import numpy as np
import pandas as pd

from montecarlo_methos import *
from scipy.stats import norm


# %% 


# %% 

"""
text = "Calculate barrier option (type) price for ALSEA stock with maturity in 1 y, strike of 50, barrier of 60, volatility of 0.2"

text_european = "Calculate european option price for ALSEA stock with maturity in 1 y, strike of 50"
text_barrier  = "Calculate barrier option (type) price for ALSEA stock with maturity in 1 y, strike of 50, barrier of 60, volatility of 0.2"
text_binary   = "calculate binary option (asset_or_nothing) price for ALSEA stock with maturity in 1 y, strike of 50"

text_generic1 = "Hola quiero calcular opciones option que tal. Sobre stock ALSEA." 
text_generic2 = "" 
"""

# %% Identify option 

def identifyGenericOption(text):
    if ("option" in text.lower()) and ("stock" in text.lower()):
        return 1
    return 0

def identifyEuropean(text):
    if ("option" in text.lower()) and ("european" in text.lower()) and ("stock" in text.lower()):
        return 1
    return 0

def identifyBarrier(text):
    if ("option" in text.lower()) and ("barrier" in text.lower()) and ("stock" in text.lower()):
        return 1
    return 0
    
def identifyBinary(text):
    if ("option" in text.lower()) and ("binary" in text.lower()) and ("stock" in text.lower()):
        return 1
    return 0 


# %% Identify parameters 
# .split("t")
# .replace("t")
# .lower()
# .upper()
# [i for i in range(10)]

def extractParameters(text):
    
    def getStrike(text):
        strike =  [i for i in text.split("stock")[-1].split(",") if "strike" in i][0].replace("strike of","").replace(" ","")
        return np.float(strike)
        
    def getBarrier(text):
        if "barrier" not in text.lower():
            return None
        barrier = [i for i in text.split("stock")[-1].split(",") if "barrier" in i][0].replace("barrier of","").replace(" ","")
        return np.float(barrier)
        
    def getMaturity(text):
        maturity = [i for i in text.split("stock")[-1].split(",") if "maturity" in i][0].replace("with maturity in","").replace(" y","").replace(" ","")
        return np.float(maturity)
        
    #def getVolatility(text):
    #    volatility = [i for i in text.split("stock")[-1].split(",") if "volatility" in i][0].replace("volatility of","").replace(" ","")
    #    return np.float(volatility)
    
    def getStock(text):
        return text.lower().split("stock")[0].split("for")[-1].replace(" ","").upper()
    
    ticker2yahoo = np.load("ticker2yahoo.npy").item()
    last_price = np.asscalar(pd.read_pickle("db/prices.pickle")[[ticker2yahoo[getStock(text)]]].values[-1])
    volatility = np.sqrt(360)*np.asscalar(pd.read_pickle("db/returns.pickle")[[ticker2yahoo[getStock(text)]]].values.std())
    
    parameters={
        'stock':getStock(text),
        'St':last_price,
        'K':getStrike(text),
        'B':getBarrier(text),
        'T':getMaturity(text),
        't':0,
        'r':0.0629,
        'sigma':volatility,#getVolatility(text),
        'n':360*getMaturity(text),
        'm':1000
    }
    return parameters
    
def getParameters():
    return extractParameters(text)

# %%
#Function to calculate "d"
def d(num=0):
    if num == 0:
        return None 
    
    p = getParameters()
    if num<=2:
        d1 = (np.log(p["St"]/p["K"])+(p["r"]+p["sigma"]**2/2)*(p["T"]))/(p["sigma"]*np.sqrt(p["T"]))
        d2 = d1-p["sigma"]*np.sqrt(p["T"])
        return (d1 if num==1 else d2)
    if num<=4:
        d3 = (np.log(p['St']/p['B'])+(p['r']+p['sigma']**2/2)*(p['T']))/(p['sigma']*np.sqrt(p['T']))
        d4 = d3-p['sigma']*np.sqrt(p['T'])
        return (d3 if num==1 else d4)
    if num<=6:
        d5 = (np.log(p['St']/p['B'])-(p['r']-p['sigma']**2/2)*(p['T']))/(p['sigma']*np.sqrt(p['T']))
        d6 = d5-p['sigma']*np.sqrt(p['T'])
        return (d5 if num==1 else d6)
    if num<=8:
        d7 = (np.log(p['St']*p['K']/p['B']**2)-(p['r']-p['sigma']**2/2)*(p['T']))/(p['sigma']*np.sqrt(p['T']))
        d8 = d7-p['sigma']*np.sqrt(p['T'])
        return (d7 if num==1 else d8)
    return None

# %% European 


def europeanBS(_kind='call'):
    p = getParameters()
    
    if _kind == 'call':
        return p['St']*norm.cdf(d(1))-p['K']*np.exp(-p['r']*(p['T']))*norm.cdf(d(2))
    
    if _kind == 'put':
        return -p['St']*norm.cdf(-d(1))+p['K']*np.exp(-p['r']*(p['T']))*norm.cdf(-d(2))

# %% Binary

def cashOrNothingBS(_kind='call'):
    p = getParameters()
    
    if _kind == 'call':
        return np.exp(-p['r']*(p['T']))*norm.cdf(d(2))
    
    if _kind == 'put':
        return np.exp(-p['r']*(p['T']))*norm.cdf(-d(2))
        
def assetOrNothingBS(_kind='call'):
    p = getParameters()
    
    if _kind == 'call':
        return p['St']*norm.cdf(d(1))
    
    if _kind == 'put':
        return p['St']*norm.cdf(-d(1))

# %% Any option with BS

def getBlackScholesValuation(_type, _kind):
    
    if 'european' in _type:
        return europeanBS(_kind)
    
    if 'cash_or_nothing' in _type:
        return cashOrNothingBS(_kind)
    
    if 'asset_or_nothing' in _type:
        return assetOrNothingBS(_kind)
        
    return "Option not detected!"

# %% MonteCarlo Method for each option


def europeanMC(_kind,_simul):
    
    p = getParameters()
    
    if _simul == "kde":
        f = mTrajectoriesKde
    else:
        f = mTrajectoriesNormal
        
    
    df = f(p["stock"],n=360*p["T"],m=500,zero_mean=True)
    
    if _kind=='call':
        return np.exp(-p['r']*(p['T']))*((df.iloc[-1]-p["K"]).apply(lambda x: 0 if x <=0 else x).mean())
    if _kind=='put':
        return np.exp(-p["r"]*(p["T"]))*((p["K"]-df.iloc[-1]).apply(lambda x: 0 if x <=0 else x).mean())


def cashOrNothingMC(_kind='call',_simul="norm"):
    p = getParameters()
    
    if _simul == "kde":
        f = mTrajectoriesKde
    else:
        f = mTrajectoriesNormal
    
    
    df = f(p["stock"],n=360*p["T"],m=500,zero_mean=True)
    
    if _kind == 'call':
        return np.exp(-p['r']*(p['T']))*((df.iloc[-1]>p["K"]).apply(lambda x: 0 if x <=0 else x).mean())
    
    if _kind == 'put':
        return np.exp(-p["r"]*(p["T"]))*((p["K"]>df.iloc[-1]).apply(lambda x: 0 if x <=0 else x).mean())

    return 1
        
def assetOrNothingMC(_kind='call',_simul="norm"):
    p = getParameters()
    
    if _simul == "kde":
        f = mTrajectoriesKde
    else:
        f = mTrajectoriesNormal
    
    
    df = f(p["stock"],n=360*p["T"],m=500,zero_mean=True)
    
    if _kind == 'call':
        return np.exp(-p['r']*(p['T']))*((p['St']*(df.iloc[-1]>p["K"])).apply(lambda x: 0 if x <=0 else x).mean())
    
    if _kind == 'put':
        return np.exp(-p["r"]*(p["T"]))*((p['St']*(p["K"]>df.iloc[-1])).apply(lambda x: 0 if x <=0 else x).mean())
    
    return 1

def upAndOutMC(_kind='call',_simul="norm"):
    p = getParameters()
    e = np.exp(-p['r']*p['T'])
    
    
    if _simul == "kde":
        f = mTrajectoriesKde
    else:
        f = mTrajectoriesNormal
    
    
    df = f(p["stock"],n=360*p["T"],m=500,zero_mean=True)
    
    if _kind == 'call':
        if p['B']>p['K']:
            return 1
        return None
    
    if _kind == 'put':
        if p['B']>p['K']:
            return 1
        return 1

def upAndInMC(_kind='call',_simul="norm"):
    p = getParameters()
    e = np.exp(-p['r']*p['T'])
    
    if _kind == 'call':
        if p['B']>p['K']:
            return 1
        return None 
    
    if _kind == 'put':
        if p['B']>p['K']:
            return 1
        return 1
        
def downAndOutMC(_kind='call',_simul="norm"):
    p = getParameters()
    e = np.exp(-p['r']*p['T'])
    
    if _kind == 'call':
        if p['B']>p['K']:
            return 1
        return 1
    
    if _kind == 'put':
        if p['B']>p['K']:
            return 1
        return None 
        
def downAndInMC(_kind='call',_simul="norm"):
    p = getParameters()
    e = np.exp(-p['r']*p['T'])
    
    if _kind == 'call':
        if p['B']>p['K']:
            return 1
        return 1
    
    if _kind == 'put':
        if p['B']>p['K']:
            return 1
        return None
    

# %% Any option with MonteCarlo

def getMonteCarloValuation(_type, _kind,_simul):
    
    if 'european' in _type:
        return europeanMC(_kind,_simul)
    
    if 'cash_or_nothing' in _type:
        return cashOrNothingMC(_kind,_simul)
    
    if 'asset_or_nothing' in _type:
        return assetOrNothingMC(_kind,_simul)
        
    if 'barrier_down_and_out' in _type:
        return downAndOutMC(_kind,_simul)
    
    if 'barrier_up_and_out' in _type:
        return upAndOutMC(_kind,_simul)    
    
    if 'barrier_down_and_in' in _type:
        return downAndInMC(_kind,_simul)
        
    if 'barrier_up_and_in' in _type:
        return upAndInMC(_kind,_simul)

    
    return "Option not detected!"    

# %% Option wrapper

def optionWrapper(t_xt):
    global text
    text = t_xt 
    
    _type = None 
    def detectBinaryType(text):
        return text.lower().split("(")[-1].split(")")[0].replace(" ","")
    
    def detectBarrierType(text):
        return text.lower().split("(")[-1].split(")")[0].replace(" ","")    
    
    if identifyEuropean(text):
        _type = "european"
        
    if identifyBinary(text):
        _type = detectBinaryType(text)
        if ("_" not in _type):
            return "Hey, there's something wrong! Remember that binary opotions must be written as: cash_or_nothing or asset_or_nothing"
     
    if identifyBarrier(text):
        _type = detectBarrierType(text)
        if ("_" not in _type):
            return "Hey, there's something wrong! Remember that barrier opotions must be written as: barrier_down_and_out, barrier_down_and_in, barrier_up_and_out or barrier_up_and_in"    
        
    if _type is None:
        return "Option not found!"
    # get option premium BS
    try:
        bs_call = getBlackScholesValuation(_type, _kind="call")
        bs_put  = getBlackScholesValuation(_type, _kind="put")
    except:
        bs_call = '--'
        bs_put = '--'
    
    # get option premium MC
    try:
        mc_call_norm = getMonteCarloValuation(_type, _kind="call",_simul="norm")
        mc_call_kde = getMonteCarloValuation(_type, _kind="call",_simul="kde")
    except: 
        mc_call_norm = '--'
        mc_call_kde  = '--'
    try:
        mc_put_norm  = getMonteCarloValuation(_type, _kind="put",_simul="norm")
        mc_put_kde   = getMonteCarloValuation(_type, _kind="put",_simul="kde")
    except:
        mc_put_norm = '--'
        mc_put_kde  = '--'
    
    def setLen24(txt):
        if type(txt) == type(txt):
            return txt
        return int(100*txt)/100
    
    # format the result 
    result = """\
The option price is:

Using BlackScholes    
    Call: {bs_call}
    Put : {bs_put}

Using MonteCarlo Simulation (norm | kde)
    Call: {mc_call_norm} | {mc_call_kde}
    Put : {mc_put_norm} | {mc_put_kde} 

""".format(bs_call=setLen24(bs_call),
           bs_put=setLen24(bs_put),
           mc_call_norm=setLen24(mc_call_norm),
           mc_put_norm=setLen24(mc_put_norm),
           mc_put_kde=setLen24(mc_put_kde),
           mc_call_kde=setLen24(mc_call_kde))
    
    return result 
# %% 
"""
text_european = "Calculate european option price for ALSEA stock with maturity in 1 y, strike of 50, volatility of 0.2"
text = text_european
# %%

text = "Calculate binary option (asset_or_nothing) price for ALSEA stock with maturity in 1 y, strike of 50, volatility of 0.2"
if identifyGenericOption(text):
    res = optionWrapper(text)
    
print(res)
"""