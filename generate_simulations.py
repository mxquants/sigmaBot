#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Montecarlo Simulations
Created on Thu May 11 22:50:24 2017

/future_simulations
    desc.npy
    /kde_based
    /normal_based

horizonal: 100000
vertical : 400
@author: rhdzmota
"""

# %% Imports

import numpy  as np
import pandas as pd

import data_operations as do 

from montecarlo_methos import mTrajectoriesKde, mTrajectoriesNormal

# %% Save as pickle
 

def save(df,filename,path):
    df.to_pickle(path+filename+".pickle")


# %% 

def generateKDE_files():
    
    def generateAndSave(x):
        try:
            file = mTrajectoriesKde(x)
            save(file,x,path="db/future_simulations/kde_based/")
            print("KDE simulaton generated for: {}".format(x))
        except: 
            print("Oops, something went wrong for: {}".format(x))
            errors = list(np.load("db/future_simulations/kde_based/errors.npy"))
            errors.append(x)
            np.save("db/future_simulations/kde_based/errors.npy",errors)
            
    list(map(lambda x: generateAndSave(x), do.trulyAvailableStocks()))
    return 1

def generateNormal_files():
    
    def generateAndSave(x):
        try:
            file = mTrajectoriesNormal(x)
            save(file,x,path="db/future_simulations/normal_based/")
            print("Normal simulaton generated for: {}".format(x))
        except: 
            print("Oops, something went wrong for: {}".format(x))
            errors = list(np.load("db/future_simulations/normal_based/errors.npy"))
            errors.append(x)
            np.save("db/future_simulations/normal_based/errors.npy",errors)
            
    list(map(lambda x: generateAndSave(x), do.trulyAvailableStocks()))
    return 1
# %% 

def main():
    
    # generate kde simulations
    print("\n\nGenerating KDE Simulations...")
    print(generateKDE_files())
    
    print("\n\nGenerating Normal Simulaions...")
    print(generateNormal_files())
    
# %% 

if __name__ == "__main__":
    
    main()

# %% 

# %% 

# %% 

# %% 

# %% 

# %% 

# %% 

# %% 

# %% 