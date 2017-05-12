#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 15:01:34 2017

@author: rhdzmota
"""

from jokes import *
from stock_plots import *
from markowitz import *


# %% Sample message

def generateSampleData(message='integrate x from 0 to 5'):
    
    data =     {
                "object":"page",
                "entry":[
                    {
                        "messaging":[
                            {
                                "message":{
                                    "text":message,
                                    "seq":20,
                                    "mid":"mid.1466015596912:7348aba4de4cfddf91"
                                },
                                "timestamp":1466015596919,
                                "sender":{
                                    "id":"885721401551027"
                                },
                                "recipient":{
                                    "id":"260317677677806"
                                }
                            }
                        ],
                        "time":1466015596947,
                        "id":"260317677677806"
                    }
                ]
            }
    
    return data

def messagingEvent(message='#pycode print("hey")'):
    msg = {
                                "message":{
                                    "text":message,
                                    "seq":20,
                                    "mid":"mid.1466015596912:7348aba4de4cfddf91"
                                },
                                "timestamp":1466015596919,
                                "sender":{
                                    "id":"885721401551027"
                                },
                                "recipient":{
                                    "id":"260317677677806"
                                }
                            }
    return msg 

def simulateEntry(n=1,message='#pycode print("hey")'):
    
    entry = {
                        "messaging":[
                            {
                                "message":{
                                    "text":message,
                                    "seq":20,
                                    "mid":"mid.1466015596912:7348aba4de4cfddf91"
                                },
                                "timestamp":1466015596919,
                                "sender":{
                                    "id":"885721401551027"
                                },
                                "recipient":{
                                    "id":"260317677677806"
                                }
                            }
                        ]*n,
                        "time":1466015596947,
                        "id":"260317677677806"
                    }
    return entry 
    

# %% Interpret


def getUserInfo(sender_id='1657838257577411'):
    import requests
    pat = 'EAADMZBDhEKOoBAOZCgvKHj6tlf8lQTMNB6MUvPTQQEgluJCXt4VZAH7zTx25NnPD25TOp1ZAG5p0ayksyfjGUMrmeIfVy5tqQq7yMKM27LWx1nfZBVEpn4zQfLXrIzo8FC5RmKywQumyswxp1dDcjqvyFqaNoKFnuq0ucfvGv6QZDZD'
    userprofile_api = 'https://graph.facebook.com/v2.6/{USER_ID}?fields=first_name,profile_pic,gender&access_token={PAGE_ACCESS_TOKEN}'
    return eval(requests.get(userprofile_api.format(USER_ID=sender_id,PAGE_ACCESS_TOKEN=pat)).text)

def firstGreetingMessage(sender):
    _user = getUserInfo(sender).get('first_name')
    user_name =  _user if _user is not None else 'there'
    _text = """\
Hi {}! 

My name is Sigma, your personal financial assistant!
    """
    return _text.format(user_name)

def deleteFirstWhitespace(text):
    return (text if text[0] != ' ' else deleteFirstWhitespace(text[1:])) 

def identifyShortMessageAndGreeting(text):
    n = len(text)
    if n > 25:
        return 0
    if 'hola' in text.lower():
        return 1
    if 'que onda' in text.lower():
        return 1
    if 'que tal' in text.lower():
        return 1
    if 'saludos' in text.lower():
        return 1
    if 'hello' in text.lower():
        return 1
    if 'hi' in text.lower():
        return 1
    if 'hey' in text.lower():
        return 1
    return 0

def identifyWhoYouAre(text):
    if 'quien eres' in text.lower():
        return 1
    if 'que eres' in  text.lower():
        return 1
    if 'quién eres' in text.lower():
        return 1
    if 'qué eres' in  text.lower():
        return 1
    return 0

def identifyWhatsYourName(text):
    if 'nombre' in text.lower():
        return 1
    if 'name' in text.lower():
        return 1
    if ('como' in text.lower() or 'cómo' in text.lower()) and 'llamas' in text.lower():
        return 1
    if 'apodo' in text.lower():
        return 1
    return 0


def identifyHowAreYou(text):
    if 'how' in text.lower() and 'are' in text.lower() and 'you' in text.lower():
        return 1
    if 'how' in text.lower() and 'its' in text.lower() and 'going' in text.lower():
        return 1
    if 'cómo' in text.lower() and ('estas' in text.lower() or 'andas' in text.lower()):
        return 1
    if 'fine' in text.lower() or 'good' in text.lower() or 'great' in text.lower():
        return 1
    return 0

def getResponseForHowAreYouAndOkays():
    import numpy as np 
    
    possible_responses={}
    
    possible_responses[1] = """\
    Great! 
    """
    possible_responses[2] = """\
    Perfect. :)
    """
    possible_responses[3] = """\
    Fine, good to know! 
    """
    possible_responses[4] = """\
    Everything is perfect. 
    """
    possible_responses[5] = """\
    Good, just chilling. 
    """
    possible_responses[6] = """\
    Okay ;)
    """
    possible_responses[7] = """\
    Awsome! 
    """
    possible_responses[8] = """\
    Pyfanstastic! 
    """
    possible_responses[9] = """\
    Like a pandas in jupyter. (:
    """
    possible_responses[10] = """\
    Same here!
    """
    _index = np.random.uniform()
    _list  = list(possible_responses.keys())
    return possible_responses[_list[int(len(_list)*_index)]]
    

# Jokes 

def identifyJoke(text):
    if 'chiste' in text.lower():
        return 1
    if 'joke' in text.lower():
        return 1
    if 'humor' in text.lower():
        return 1
    if 'relax' in text.lower():
        return 1
    return 0

def getOneJoke():
    _text = "I've got a joke for you: \n\n"
    return _text+chooseJoke()

def myNameIs():
    return 'My name is... Heissenberg!\n\nJK, you can call me sigma.' 

# generic message 

def genericGreetingMesasge(sender):
    import numpy as np
    _user = getUserInfo(sender).get('first_name')
    user_name =  _user if _user is not None else 'Wolf of WallStreet'
    
    generic_message = {}
    generic_message[1] = """\
    Hey {}! Good to hear about you. 
    """.format(user_name)
    
    generic_message[2] = """\
    Hello {}! :)
    """.format(user_name)
    
    generic_message[3] = """\
    Hi there. How is it going?
    """
    generic_message[4] = """\
    Er... Huh... Hello. ;) 
    """
    _index = np.random.uniform()
    _list  = list(generic_message.keys())
    return generic_message[_list[int(len(_list)*_index)]]
    


def identifySendNudes(text):
    if 'send nudes' in text.lower():
        return 1
    if 'pack' in text.lower():
        return 1
    return 0

def sendNudes():
    return "https://scontent-dft4-2.xx.fbcdn.net/v/t34.0-12/18051760_10156149925989966_1903532741_n.png?oh=d54e7de3f9776a37d92ecd402d1f97a6&oe=58FFBAD0"

def identifyMe(text):
    if "me" == text.lower():
        return 1
    return 0

def getProfilePic(sender):
    pic = getUserInfo(sender).get('profile_pic')
    if pic is None:
        return "https://lh3.googleusercontent.com/UBz80Hwz87KC4Aw3q1_F9gZjLz3NyDagC52GtubICL84ERRrq6vwOPZcMULqaSJFcjaOWBA1KEUNPW6y4VrfqkzsZrxEX6xZyhzGnJ6u_u50CVlgIGA6oTSml2TucDvZ7MvcfyY7mK99QH3Ug2G7sHt3Kfx6uZX_YNfe-rN_kECdoQCz1MHjx3w0NflEcoc0muX3CTVcMUnrVjJQvEP5DaheeApIJEKCNNIrvfFt5DChj1VPtaitFyYejfuQKc2OjlBrMPELpanQPADvoKUepxRiVAyn-xmUSw_xcdLbbGu8y8r9mz2dVyiasepnakwZNzuRRHbC4Byv66kQ_Pqv4S2lHo5OIK65pnQN0RxJNnkWXDgelmrvmAVL4E4vcrg90QhYuL4GNyH7AsCKNegTPE5kjNvmrfNpY-DxDjVyCQMBkxg9rcpmvtEKTx3BYyPnWi0w9l8WjugPjPMSrgZNiFclD7i3DLgTCzLtf0PSksLmv6exPHswnTA5JKU200yIgQKhf3b3THCF4YpqMUVQvlyxRL6KVbH0uJN_un5ZfbXuuppcauvs1O_XEYoOHTkbgSPMGuAWMjT2CuTDRpmQ3P_rGNiEanQtM-Ypx-e5Ax0Xrkc=s170-no"
    return getUserProfilePic(sender)

def IDontUnserstand(sender):
    _user = getUserInfo(sender).get('first_name')
    user_name =  _user if _user is not None else 'Pythonist'
    _text = """\
I'm sorry {}, still learning to talk here. 

I didn't understand! 

...maybe you can ask me some jokes. ;)
    """
    return _text.format(user_name)

def identifySimpleMarkowitzPlot(text):
    if ("markowitz" in text.lower()) and ("plot" in text.lower()) and ("with" in text.lower()):
        return 1
    return 0 

def makeMarkPlot(text,sender):
    import image_hosting as ih
    import os 
    
    # get filename
    filename = markowitzSimplePlotWrapper(text,sender)
    
    if filename is None:
        return "https://photos-5.dropbox.com/t/2/AABa7EHptD0MRtyFW9rmTPbhOw70Y3faibAesnAKYU6zTA/12/666157048/png/32x32/3/1494226800/0/2/No_tick.png/ELfo6LsFGAQgBygH/cbbniVcsZ49xuZIemtI12r8l0S1zr5Qp1QaT8ilNDs8?dl=0&size=2048x1536&size_mode=3"
    
    DBM = ih.DropBoxManager()
    
    # delete file 
    DBM.deleteFile(path="/markowitz_plots",filename=filename)
    DBM.uploadFile(path="/markowitz_plots",filename=filename)
    temo = DBM.getTemporaryUrl(path="/markowitz_plots",filename=filename)
    os.remove(filename)
    return temo['url']


def identifyStockPlot(text):
    if ('plot' in text.lower()) and ('marko' not in text.lower()):
        return 1
    
def makeStockPlot(text,sender):
    import image_hosting as ih
    import os 
    
    # get filename
    filename = stockPlotWrapper(text,sender)
    
    if filename is None:
        return "https://photos-5.dropbox.com/t/2/AABa7EHptD0MRtyFW9rmTPbhOw70Y3faibAesnAKYU6zTA/12/666157048/png/32x32/3/1494226800/0/2/No_tick.png/ELfo6LsFGAQgBygH/cbbniVcsZ49xuZIemtI12r8l0S1zr5Qp1QaT8ilNDs8?dl=0&size=2048x1536&size_mode=3"
    
    DBM = ih.DropBoxManager()
    
    # delete file 
    DBM.deleteFile(path="/stock_plots",filename=filename)
    DBM.uploadFile(path="/stock_plots",filename=filename)
    temo = DBM.getTemporaryUrl(path="/stock_plots",filename=filename)
    os.remove(filename)
    return temo['url']

def identifyAvailableRequest(text):
    if "available" in text.lower():
        return 1
    
def identifyDescriptionRequest(text):
    if "describe" in text.lower():
        return 1 
    
def satisfyDescription(text):
    from data_operations import referenceNames
    import pandas as pd
    import numpy  as np
    ticker = [i.upper() for i in text.lower().replace("describe", "").replace(","," ").split(" ") if i != ""]
    
    if len(ticker) != 1:
        return "Hey there, you enter an invalid command. Try just: Describe <TICKER>\nNote, replace <TICKER> with the stockname (e.g. ALSEA, SANMEX)"
    ticker = ticker[0]
    
    def getYahoo(ticker):
        ticker = ticker.upper()
        if '.MX' in ticker:
            return ticker
        return referenceNames()['ticker2yahoo'][ticker] 
    
    try:
        desc = referenceNames()["name2desc"][ticker]
        yho  = getYahoo(ticker)
        prices =  pd.read_pickle("db/prices.pickle")[[yho]]
        returns = pd.read_pickle("db/returns.pickle")[[yho]]
    except:
        return "Warning: There is an error regarding the stock-name (ticker) provided."
    price_description = """\
    
\n
Using 2y of historical data. 
    
    Price Desc.
    
>> Actual price: {actual} MXN     
>> Min. price recorded: {_min} MXN 
>> Max. price recordad: {_max} MXN 
>> Last 10 prices average: {avrg} MXN

""".format(actual=np.asscalar(prices.values[-1]),_min=np.min(prices.values),_max=np.max(prices.values),avrg=np.mean(prices.values[-10:]))
    
    return_description = """\
    
    Returns Desc. 
    
>> Daily mean return: {}
>> Daily volatility: {}
    
>> Annual mean return: {}
>> Annual volatility: {}
""".format(np.mean(returns.values),np.std(returns.values),360*np.mean(returns.values),np.sqrt(360)*np.std(returns.values))

    return "According to the BMV: \n\n"+desc+price_description+return_description


def identifyEfficientPort(text):
    # Get percentile 10 portfolio from efficient fronteir using all data.
    if ("percentile" in text.lower()) and ("port" in text.lower()) and ("efficient" in text.lower()) and ("using" in text.lower()):
        return 1
    return 0


def identifySingleEfficient(text):
    # Get markowitz efficient portfolio using all data
    if ("markowitz" in text.lower()) and ("port" in text.lower()) and ("efficient" in text.lower()) and ("using" in text.lower()):
        return 1
    return 0
        
        
# %% Generate Response

def generateResponse(text,sender):
    
    
    if identifyShortMessageAndGreeting(text):
        return firstGreetingMessage(sender),'text'
    
    if identifyWhoYouAre(text):
        return firstGreetingMessage(sender),'text'
    
    if identifyWhatsYourName(text):
        return myNameIs(),'text'
    
    if identifyHowAreYou(text):
        return getResponseForHowAreYouAndOkays(),'text'
    
    if identifyJoke(text):
        return getOneJoke(),'text'
    
    if identifySendNudes(text):
        return sendNudes(),'image'
        
    if identifySimpleMarkowitzPlot(text):
        return makeMarkPlot(text,sender),'image'
        
    if identifyAvailableRequest(text):
        return availableStocks(),'text'
    
    if identifyStockPlot(text):
        return makeStockPlot(text,sender),'image'
        
    if identifyDescriptionRequest(text):
        return satisfyDescription(text), 'text'
        
    if identifyEfficientPort(text):
        return getMarkowitzPortfolioFromFrontier(text), 'text'
        
    if identifySingleEfficient(text):
        return getEfficientPort(text), 'text'
        
    return IDontUnserstand(sender),'text'

# %% 

class RespondEntryMessages(object):
    
    def __init__(self,entry):
        self.entry = entry
        #self.message_list = [mevent for mevent in entry['messaging'] if mevent.get('message')]
        self.message_list,self.delivery_list,self.optin_list,self.postback_list = [],[],[],[]
        for mevent in entry['messaging']:
            
            if mevent.get('message'):
                self.message_list.append(mevent)
                
            if mevent.get('delivery'):
                self.delivery_list.append(mevent)
                
            if mevent.get('optin'):
                self.optin_list.append(mevent)
                
            if mevent.get('postback'):
                self.postback_list.append(mevent)
        
    def now(self):
        
        def getSenderAndText(mevent):
            sender = mevent['sender']['id']
            text   = mevent['message'].get('text')
            if not text:
                response,_type = 'Nice '+str(mevent['message']['attachments'][0]['type']),"text"
            else: 
                response,_type = generateResponse(text,sender)
            if "text" in _type:
                return {'Sender':sender,'OriginalText':text, 'Text':response,'_type':_type}
            if "image" in _type:
                return {'Sender':sender,'OriginalText':text, 'ImageURL':response,'_type':_type}
            
        #if len(self.message_list):
        #    return 'Okay!'
            
        self.respond_list = map(getSenderAndText,self.message_list)
        return self.respond_list

# %% 