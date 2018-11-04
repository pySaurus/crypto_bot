'''
Created on May 17, 2018

@author: Danny
'''

import cbpro, time 
#class that gets data from the GDAX ticker channel. Inherited GDAX written class
class TickerWebsocketClient(cbpro.WebsocketClient):
    
    #inherited method. Called when new instance is created
    def on_open(self):
        self.url = "wss://ws-feed.gdax.com/" #connect to GDAX
        #self.products =         #specify market
        self.message = {}                    #create empty dictionary
        
        self.channels = ['ticker']           #specify channel to pull data from
        self.type = 'ticker'                 # ^
        self.read = False

    #inherited method. Called every iteration
    def on_message(self, msg):
        self.message = msg                   #get incoming data
            

    #inherited method. Called on close
    def on_close(self):
        print("-- Goodbye! --")
        
    #custom method. Called to wait for ticker data at start of script
    def verify_data_loaded(self):
        noData = True 
        while noData:
            try:
                price = float(self.message['price'])
                noData = False
            except Exception:
                time.sleep(1)
                print("waiting for data....") 
        