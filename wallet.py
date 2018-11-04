'''
Created on Jul 19, 2018

@author: dpolyakov
'''

class Wallet(object):
    '''
    Keeps track of money amount. Can make multuple instances for multiple types of crypto
    '''
    def __init__(self, ty, USD, CRY, initial): # type of crypto, usd value, crypto value
        self.crypto_type = ty                       #set types of crypto
        self.USD_value = USD                        #set USD value
        self.crypto_value = CRY                     #set crypto value
        self.fee_total = 0.0                        #keep track of accumulated fees
        self.initial_value = USD + (initial * CRY)  #inital total value of wallet
        self.market_start = initial                 #inital price of currency on market
        self.totalVal = self.initial_value          #temporarily set the total value of the wallet to starting value
        
        
    def toString(self):
        #returns information about the wallet
        return(self.crypto_type + " wallet contains: " + str(self.USD_value) + " dollars and " + str(self.crypto_value) + " " +
        self.crypto_type + " with " + str(self.fee_total) +
         " in fees || Wallet Start: " + str(self.initial_value) + " | Wallet Curr: " + str(self.totalVal))
    
    def total(self, market):
        #recalculate total value of the wallet given the current market value
        self.totalVal = self.USD_value + (self.crypto_value * market) - self.fee_total
        return(self.totalVal)
        #return(" Total Value: " + str(self.totalVal))
    def realtime_reload(self, authClient):
        #get realtime wallet information
        #USD - '42803a4f-33a9-45b2-af4a-9fd3c374fe80'
        #LTC - '4d9356d7-76ac-4b6f-8e4e-f4417b51b42e'
        self.USD_value = authClient.get_account('42803a4f-33a9-45b2-af4a-9fd3c374fe80')
        self.crypto_value = authClient.get_account('4d9356d7-76ac-4b6f-8e4e-f4417b51b42e')