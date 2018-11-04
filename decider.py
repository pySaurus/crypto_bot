'''
Created on Jul 23, 2018

@author: dpolyakov
'''

import analyzer, wallet

class Decider(object):
    '''
    Decider classes determine what trades are made where.
    
    
    '''

    #initilizer method for objects
    def __init__(self, start_val, type, USD, CRY, qua, thresh, analy, auth):
        #set analyzer
        self.ana = analy
        #set wallet
        self.wal = wallet.Wallet(type, USD, CRY, start_val)
        #set quantity to be traded
        self.quantity = qua
        #set client to trade with
        self.client = auth
        #set internal count
        self.pacer = 0 
        #set recenty trade price
        self.trade_value = 0.0
        #set last action status
        self.status = 'none'
        #set the threshhold
        self.thresh = thresh
        #upper thresh
        self.Uthreshhold = 1.0 + thresh
        #lower thresh 
        self.Lthreshhold = 1.0 - thresh
        
        #all orders are put on their respective lists for tracking
        self.buyList = []
        self.sellList = []
    
    
    #evaluate the analyzer variables, the incoming ticker price and the threshholds
    def trade(self):
        if (self.ana.third * self.Uthreshhold) <  (self.ana.prev): # sell because the incoming price is higher than the baseline
            self.sell(self.quantity, self.ana.prev)

        elif (self.ana.third * self.Lthreshhold) > (self.ana.prev): # buy because the incoming is lower than baseline
            self.buy(self.quantity, self.ana.prev)                    
                        
                #print('not enough difference')
            print('||| DECIDER: thresh,' + str(self.thresh) + " | quant," + str(self.quantity))
            print(self.wal.toString() + " Total Value: "+  str(self.wal.total(self.ana.prev)))
            print(self.ana.toString())
            print(self.buyList)
            print(self.sellList)
            

            
    #sell crypto. Adjust wallet prices
    def sell(self, quant, price):
        if self.wal.crypto_value >= self.quantity:#if i have the money and a tigger hasn't been set
            self.wal.crypto_value -= quant
            self.wal.USD_value += (quant * price)
            self.wal.fee_total += (quant * price * .003)
            self.sellList.append([price, self.ana.third, quant])
            
            #print('sold LTC')
        #                     self.client.sell(price=str(self.prev),
        #                                      size= self.quantity,
        #                                      product_id='LTC-USD')
            self.trade_value = price
            self.status = 'sold'
        else:
            #print('insufficient LTC')
            pass
    
    #buy crypto. Adjust wallet prices
    def buy(self, quant, price):
        if self.wal.USD_value >= (quant * price): #if i have the money and a tigger hasn't been set
            self.wal.crypto_value += quant
            self.wal.USD_value -= (quant * price)
            self.wal.fee_total += (quant * price * .003)
            self.buyList.append([price, self.ana.third, quant])
            #print('bought LTC')
    #         self.client.buy(price=str(self.prev),
    #                                       size= self.quantity,
    #                                       product_id='LTC-USD')
            self.trade_value = price
            self.status = 'bought'        
        else:
            #print('insufficient USD')
            pass