'''
Created on Sep 9, 2018

@author: Danny
'''

import wallet, analyzer2


class Decider2(object):
    '''
    classdocs
    '''

    #initilizer method for objects
    def __init__(self, start_val, ty, USD, CRY, qua, thresh, auth=None):
        #set crypto type for obeject
        self.type = ty
        #set analyzer
        self.ana2 = analyzer2.Analyzer2(start_val)
        #set wallet
        self.USDstart = USD
        self.wal = wallet.Wallet(ty, USD, CRY, start_val)
        #set quantity to be traded
        self.quantity = qua
        #set client to trade with
        self.client = auth
        #set internal count
        self.count = 0 
        #set the threshhold
        self.thresh = thresh
        self.buyTrack = 0
    
    
    #evaluate the analyzer variables, the incoming ticker price and the threshholds
    def trade(self):
        if(self.ana2.changelist[0] is -1):
            self.count = 0
            for i in range(self.buyTrack):
                self.sell(self.quantity, self.ana2.prev)
            self.buyTrack = 0
        elif(self.count >= 1 or self.ana2.changelist[1] is 1):
            self.count += 1

            
        if(self.count >= 18 ):
            # print("COUNTED 18 IN ROW")
            success = self.buy(self.quantity, self.ana2.prev)
            if success:
                self.buyTrack += 1


         #       #print('not enough difference')
          #  print('||| DECIDER: thresh,' + str(self.thresh) + " | quant," + str(self.quantity))
            #print(self.wal.toString() + " Total Value: "+  str(self.wal.total(self.ana.prev)))
            #print(self.ana.toString())
            
            
    #sell crypto. Adjust wallet prices
    def sell(self, quant, price):
        
        if self.wal.crypto_value >= quant:#if i have the money and a tigger hasn't been set.
            print("------------ SELL ------------")
            self.wal.crypto_value -= quant
            self.wal.USD_value += (quant * price)
            self.wal.fee_total += (quant * price * .003)
            return True
        return False
            # self.sellList.append([price, self.ana.third, quant])
            
            #print('sold ' + self.type )
        #                     self.client.sell(price=str(self.prev),
        #                                      size= self.quantity,
        #                                      product_id=self.type)
            # self.trade_value = price
            # self.status = 'sold'

    
    #buy crypto. Adjust wallet prices
    def buy(self, quant, price):
        # print([self.wal.USD_value, (quant * price)])
        if self.wal.USD_value >= (quant * price): #if i have the money and a tigger hasn't been set
            print("------------ BUY ------------")
            self.wal.crypto_value += quant
            self.wal.USD_value -= (quant * price)
            self.wal.fee_total += (quant * price * .003)
            return True
        return False
            # self.buyList.append([price, self.ana.third, quant])
            #print('bought ' + self.type)
    #         self.client.buy(price=str(self.prev),
    #                                       size= self.quantity,
    #                                       product_id=self.type)
            # self.trade_value = price
            # self.status = 'bought'        

        
    def anaAdd(self, val):
        self.ana2.add(val)

    def toString(self):
        ret = "\nHolding on to :" + str(self.buyTrack) +  " \nChangeList Value 1: " + str(self.ana2.changelist[0]) 
        ret += "  || " + str(self.count) + "\nChangeList Value: " + str(self.ana2.changelist[0:9])
        return  ret  + "\n" + self.wal.toString()