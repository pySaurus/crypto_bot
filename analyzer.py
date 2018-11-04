'''
Created on Jun 6, 2018

@author: dpolyakov


'''

class Analyzer(object):
    '''
    Class for keeping track of various values from the data.
    Intended to work by being fed one data point at a time and do calculations based on that
    '''
    def __init__(self, val):
        #declare some class variables
        self.data = []
        self.data.append(val)
        self.id_count = 0
        self.count = 0
        self.prev = val
        self.graphOut = False

        self.fourth = 0
        self.fifth = 0
        self.sixth = 0
        self.tracker = 0
        
        self.first = 0 
        self.firstROC = 0
        self.firstROCset = False
        self.firstROCAcc = 0
        
        self.second = 0
        self.secondROC = 0
        self.secondROCset = False
        self.secondROCAcc = 0
        
        self.third = 0
        self.thirdROC = 0
        self.thirdROCset = False
        self.thirdROCAcc = 0
                      
    
    def add(self, val):  
        #add a new ticker value to the analyzer and 
        #if self.data[0] != val and (val > (self.prev * .7) and val < (self.prev * 1.3)): #this line is to do something that doesnt need to happen anymore
        self.data.insert(0, val)    #put the incoming value into the data List
        self.prev = val             #set incoming value as prev value
        if(len(self.data) > 10000): #list max length is 10000
            self.data.pop(len(self.data)-1)
        self.count += 1             #keep track of entry
        self.compute()              #run compute function
            
            
            
    def compute(self):              #computes various averages
        if len(self.data) >= 10:
            self.first_avg()
        if len(self.data) >= 60:
            self.second_avg()
        if len(self.data) >= 500:
            self.third_avg()
        if len(self.data) >= 1000:
            self.fourth_avg()
        if len(self.data) >= 5000:
            self.fifth_avg()
        if len(self.data) >= 10000:
            self.sixth_avg()
            self.tracker_avg()
    
    #averages
    def first_avg(self): # 10 tick (very short term)
        sums = 0.0
        prev = self.first
        for i in range(10):
            sums += self.data[i]
        self.first = sums / 10
        if self.firstROCset:
            self.firstROC = (prev - self.first)
            self.firstROCAcc = self.firstROCAcc + self.firstROC
        else:
            self.firstROCset = True
            self.firstROC = self.first
    def second_avg(self):# 60 tick (short term)
        sums = 0.0
        prev = self.second
        for i in range(60):
            sums += self.data[i]
        self.second = sums / 60
        if self.secondROCset:
            self.secondROC = (prev - self.second)
            self.secondROCAcc = self.secondROCAcc + self.secondROC
        else:
            self.secondROCset = True
            self.secondROC = self.second
        
    def third_avg(self): # 500 tick
        sums = 0.0
        prev = self.third
        for i in range(500):
            sums += self.data[i]
        self.third = sums / 500
        if self.thirdROCset:
            self.thirdROC = (prev - self.third)
            self.thirdROCAcc = self.thirdROCAcc + self.thirdROC
        else:
            self.thirdROCset = True
            self.thirdROC = self.third
        #print('set roc?????? ---------------------------------')
        
    def fourth_avg(self): # 1000 tick
        sums = 0.0
        for i in range(1000):
            sums += self.data[i]
        self.fourth = sums / 1000
    def fifth_avg(self): # 5000 tick
        sums = 0.0
        for i in range(5000):
            sums += self.data[i]
        self.fifth = sums / 5000
    def sixth_avg(self): # 10000 tick
        sums = 0.0
        for i in range(10000):
            sums += self.data[i]
        self.sixth = sums / 10000
        
    def tracker_avg(self):
        self.tracker = (self.first +self.second+self.third+self.fourth+self.fifth+self.sixth) / 6.0
    
    def toString(self):
#         return ("10 tick: " + str(self.first) + "      ||    10  tick ROC: " + str(self.firstROC) + "      ||    Accumulated: "+str(self.firstROCAcc)+"\n60 tick: " + str(self.second) +"\n500 tick: " + 
#                 str(self.third)+ "      ||    500 tick ROC: " + str(self.thirdROC) + "      ||    Accumulated: " +str(self.thirdROCAcc)+"\n1000 tick: "+ str(self.fourth) + "\n5000 tick: "+ str(self.fifth) + 
#                 "\n10000 tick: "+ str(self.sixth) + "\nTracker: "+ str(self.tracker) +"\n")
        
        return ("10 tick: " + str(self.first) + "      ||    10  tick ROC: " + str(self.firstROC) + "      ||    Accumulated: "+str(self.firstROCAcc) +
                "\n60 tick: " + str(self.second)+ "      ||    60 tick ROC: " + str(self.secondROC) + "      ||    Accumulated: " +str(self.secondROCAcc)+
                "\n500 tick: " + str(self.third)+ "      ||    500 tick ROC: " + str(self.thirdROC) + "      ||    Accumulated: " +str(self.thirdROCAcc)+"\n")
        
    def grapher(self):
        pass
        
        
        