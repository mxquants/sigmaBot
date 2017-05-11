#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 10 18:46:32 2017

@author: rhdzmota
"""

# %% Imports and requ. 
import subprocess

try:
    import image_hosting as ih  
except:
    
    install_req = """\
pip install dropbox
pip install numpy
pip install matplotlib
    """
    
    output = subprocess.check_output(['bash','-c', install_req])
    import image_hosting as ih 

# %% 

def main():
    
    # drop box manager
    DBM = ih.DropBoxManager()
    
    # get desired image
    filename = input("Specify filename: ")
    
    # download temporal url 
    tempo = DBM.getTemporaryUrl(path="/web-images",filename=filename)
    print(tempo)
    return tempo 


# %% 

if __name__ == "__main__":
    main()
    
