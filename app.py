#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# %% Requirements 

import os
import sys
import json

import requests
from flask import Flask, request, render_template
from interact import * 


from generate_html import returnHTML

# %% 


def readJson(filename):
    import json
    with open(filename) as file:
        data = json.load(file)
    return data 

def saveJson(variable,filename):
    import io, json
    with io.open(filename, 'w', encoding='utf-8') as f:
      f.write(json.dumps(variable, ensure_ascii=False))
      
      
# %% Declare App 

app = Flask(__name__)

# %% GET and verify() function 

@app.route('/', methods=['GET'])
def verify():

    
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return returnHTML(), 200 

# %% POST 

@app.route('/', methods=['POST'])
def webhook():

    # endpoint for processing incoming messaging events

    data = request.get_json()
    log(data)  # you may not want to log every incoming message in production, but it's good for testing
    
    data = generalFilter(data)
    log('>> Now with filter: \n{}'.format(data))
    
    if data["object"] == "page":
        

        for entry in data["entry"]:
            
            Respond = RespondEntryMessages(entry)
            temp = list(map(sendMessage, Respond.now()))
            

    return "ok", 200



@app.route('/images', methods=['GET'])
def getUrl():
    import image_hosting as ih  
    
    # get filename 
    filename = request.args.get("filename")
    
    # get temporal url 
    try:
        DBM = ih.DropBoxManager()
        tempo = DBM.getTemporaryUrl(path="/web-images",filename=filename)
        return str(tempo['url']),200
    except:
        return "Not found",200
    
# %% 


def generalFilter(data):
    import numpy as np
    import datetime as dt
    
    #run_time = dt.datetime.now().strftime('%Y%m%d %H:%M:%S')
    
    def createEntryLog():
        #entry_log =[]
        #np.save('entry_log.npy',entry_log)
        entry_log = {}
        saveJson(entry_log,'entry_log.txt')
        
    # read logs 
    try:
        entry_log = readJson('entry_log.txt')#list(np.load('entry_log.npy'))
    except:
        createEntryLog()
        entry_log = entry_log = readJson('entry_log.txt')#list(np.load('entry_log.npy'))
        
    # get entries 
    entries = data.get('entry')
    if entries is None:
        return data
    
    # get new ids 
    good_entries = [entry for entry in entries if (str(entry) not in entry_log.keys())]
    #entry_log = list(entry_log)+[str(entry) for entry in entries]
    for entry in entries:
        entry_log[str(entry)] = dt.datetime.now().strftime('%Y%m%d %H:%M:%S')
        
    # save 
    #np.save('entry_log.npy',entry_log)
    saveJson(entry_log,'entry_log.txt')
    data['entry'] = good_entries
    return data

# %% sendMessage 

def generatePostJsonData(response_info):
    _type = response_info['_type']
    recipient_id = response_info["Sender"]
    if "text" in _type:
        message_text = response_info["Text"]
        data = json.dumps({
                            "recipient": {"id": recipient_id},
                            "message": {"text": message_text}
                            })
        return data
    if "image" in _type:
        image_url = response_info["ImageURL"]
        data = json.dumps({
                            "recipient": {"id": recipient_id},
                            "message": {"attachment": {
                                    "type": "image",
                                    "payload": {
                                            "url":image_url,
                                            "is_reusable":True}}}})
        return data 

def sendMessage(response_info):
    
    
    #log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=response_info))

    params  = {"access_token": os.environ["PAGE_ACCESS_TOKEN"]}
    headers = {"Content-Type": "application/json"}
    data    = generatePostJsonData(response_info)
    log(data)
    
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", 
                      params=params, 
                      headers=headers, 
                      data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)
        

# %% Log function -- simple wrapper for logging to stdout on heroku

def log(message):
    print(str(message))
    sys.stdout.flush()



# %% Test  

@app.route('/test', methods=['GET'])
def returnTestImage():
    html = """\ 
<!DOCTYPE html>
<html>
<body>
<h2>The Incredible pyBot!</h2>
<img src="https://scontent-dft4-2.xx.fbcdn.net/v/t34.0-12/18051760_10156149925989966_1903532741_n.png?oh=d54e7de3f9776a37d92ecd402d1f97a6&oe=58FFBAD0">
</body>
</html>
    """
    return html 
# %% 

if __name__ == '__main__':
    app.run(debug=True)
