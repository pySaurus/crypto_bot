'''
Created on Jun 6, 2018

@author: dpolyakov


'''
import statistics, math

class Analyzer2(object):
    '''
    Class for keeping track of various values from the data.
    Intended to work by being fed one data point at a time and do calculations based on that
    '''
    def __init__(self, val):
        #declare some class variables
        self.data = []
        self.data.append(val)

        self.count = 0
        self.prev = val


        #so we are gonna have a couple averages to be calculated out below.
        #we are gonna have moving averages over the last x ticks and a 
        #variable that tracks the first and second order derivative of 
        #the actual price
        self.changelist=[]
        self.first_order = 0
        self.second_order = 0

        self._5 = 0
        self._5roc = 0
        self._5roc2 = 0

        self._10 = 0
        self._10roc = 0
        self._10roc2 = 0
        
        self._30 = 0
        self._30roc = 0
        self._30roc2 = 0
        
        self._60 = 0
        self._60roc = 0
        self._60roc2 = 0

        self._300 = 0
        self._300roc = 0
        self._300roc2 = 0
        
        self._RMSD_5 = 0
        self._Var_5 = 0
        self._chisq_5 = 0

        
        
    def add(self, val):
        #add a new ticker value to the analyzer
        self.data.insert(0, val)    #put the incoming value into the data List
        self.prev = val             #set incoming value as prev value
        if(len(self.data) > 360): #list max length is 360. This translates to 6 hours of data since an entry is a minute
            self.data.pop(len(self.data)-1)
        self.count += 1             #keep track of entry
        self.compute()              #run compute function
        self.delta()                #run change function
        if(len(self.changelist) > 1000):
            self.changelist.pop(len(self.changelist)-1)
            
            
            
    def compute(self):              #computes various averages
        self.priceAverages()
        if len(self.data) >= 5:
            self.com_5()
        if len(self.data) >= 10:
            self.com_10()
        if len(self.data) >= 30:
            self.com_30()
        if len(self.data) >= 60:
            self.com_60()
        if len(self.data) >= 300:
            self.com_300()

                #change in value function
    def delta(self):
        if(self.first_order > 0):
            self.changelist.insert(0, 1)
        elif(self.first_order < 0):
            self.changelist.insert(0, -1)
        else:
            self.changelist.insert(0, 0)
        # maxperinc=0.05
        # lastval=self.data[0]
        # curval=self.data[1]
        # change=curval-lastval
        # perdif=change/(0.5*(curval+lastval))
        # if perdif>0 and perdif<=maxperinc:
        #     self.changelist.insert(0,1)
        # elif perdif<0:
        #     self.changelist.insert(0,-1)
        # else:
        #     self.changelist.insert(0,0)

    def specdelta(self): # Weighted Delta 
        maxperinc=0.05
        maxperdec=-0.05
        lastval=self.data[0]
        curval=self.data[1]
        perdif=(lastval-curval)/(0.5*(curval+lastval))
        if perdif>=maxperdec and perdif<=maxperinc:
            self.changelist.insert(0,perdif)
        else:
            self.changelist.insert(0,0)



    #averages
    
    def priceAverages(self):
        prev_roc = self.first_order     
        self.first_order   = (self.data[0] - self.data[1])
        self.second_order  = (prev_roc - self.first_order)
    
    def com_5(self): # 5 tick
        sums = 0.0
        prev = self._5
        prev_roc = self._5roc
        for i in range(5):
            sums += self.data[i]
        self._5 = sums / 5
        self._5roc   = (prev - self._5)
        self._5roc2  = (prev_roc - self._5roc)
        
        RMSD5=0.0
        for i in range(5):
            RMSD5 += (self.data[i]-self._5)
        self._RMSD_5 = (RMSD5/5)**.5

        self._var_5 = (self._5)**2

        sumdiff = 0.0
        for i in range(5):
            sumdiff += (self.data[i]-self._5)
        self._chisq_5 = sumdiff/self._5


    def com_10(self): # 10 tick
        sums = 0.0
        prev = self._10
        prev_roc = self._10roc
        for i in range(10):
            sums += self.data[i]
        self._10 = sums / 10
        self._10roc   = (prev - self._10)
        self._10roc2  = (prev_roc - self._10roc)
        
    def com_30(self): # 30 tick
        sums = 0.0
        prev = self._30
        prev_roc = self._30roc
        for i in range(30):
            sums += self.data[i]
        self._30 = sums / 30
        self._30roc   = (prev - self._30)
        self._30roc2  = (prev_roc - self._30roc)
            
    def com_60(self): # 60 tick
        sums = 0.0
        prev = self._60
        prev_roc = self._60roc
        for i in range(60):
            sums += self.data[i]
        self._60 = sums / 60
        self._60roc   = (prev - self._60)
        self._60roc2  = (prev_roc - self._60roc)

    def com_300(self): # 300 tick
        sums = 0.0
        prev = self._300
        prev_roc = self._300roc
        for i in range(300):
            sums += self.data[i]
        self._300 = sums / 300
        self._300roc   = (prev - self._300)
        self._300roc2  = (prev_roc - self._300roc)

    def toString(self):   
        return ("Price tick: " + str(self.prev) + "      ||    Price ROC: " + str(self.first_order) + "      ||     Price ROC 2: "+str(self.second_order) +
            #    "\n5 tick: " + str(self._5) + "      ||    5  tick ROC: " + str(self._5roc) + "      ||     5  tick ROC 2: "+str(self._5roc2) +
            #    "\n10 tick: " + str(self._10) + "      ||    10  tick ROC: " + str(self._10roc) + "      ||     10  tick ROC 2: "+str(self._10roc2) +  
            #    "\n30 tick: " + str(self._30) + "      ||    30  tick ROC: " + str(self._30roc) + "      ||     30  tick ROC 2: "+str(self._30roc2) +
            #    "\n60 tick: " + str(self._60) + "      ||    60  tick ROC: " + str(self._60roc) + "      ||     60  tick ROC 2: "+str(self._60roc2) +
                "\nLast 10 Entries:" + str(self.data[0:9]) +'\n\n')