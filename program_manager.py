'''
Created on Jun 6, 2018

@author: dpolyakov

This script will be the launching point of the bot overall. 

'''

#import a bunch of stuff that maybe i need.


import decider2 as dec
import ticker
import cbpro, time, datetime, _csv
import numpy as np
import matplotlib.pyplot as plt

def main():
    print("Bot Started")
    #excel recorder initialization
    with open("C:/Users/Danny/Documents/GitHub/bot/output.csv", 'w', encoding='utf8') as f:
        outputFile = _csv.writer(f, delimiter=',', lineterminator='\n')           
        #data for testing purposes
        '''
        btcData = _csv.reader(open("FILEPATH", 'r', encoding='utf8'), delimiter=',', lineterminator='\n')    
        ltcData = _csv.reader(open("FILEPATH", 'r', encoding='utf8'), delimiter=',', lineterminator='\n')    
        ethData = _csv.reader(open("FILEPATH", 'r', encoding='utf8'), delimiter=',', lineterminator='\n')    
        etcData = _csv.reader(open("FILEPATH", 'r', encoding='utf8'), delimiter=',', lineterminator='\n')    
        bchData = _csv.reader(open("FILEPATH", 'r', encoding='utf8'), delimiter=',', lineterminator='\n')    
        '''
        
        
        #authorized client initialization
        #websocket client initializtion                         Litecoin    Bitcoin     Ether      Ether Classic     Bitcoin Cash
        
        #general_client = ticker.TickerWebsocketClient(message_type='ticker',products=["LTC-USD", "BTC-USD", "ETH-USD",    "ETC-USD",       "BCH-USD"])
        general_client = ticker.TickerWebsocketClient(message_type='ticker',products=["BTC-USD"])
        
        general_client.start()
        general_client.verify_data_loaded() #verification of data moved to api 
        
        initial_ana_values = {}
        print('getting initial analyzer values')
        while len(initial_ana_values) < 1: #change value to 5 when testing all currencies
            print(initial_ana_values)
    
            crypto = general_client.message['product_id']
            initial_ana_values[crypto] = float(general_client.message['price'])
                
        print(initial_ana_values)
    
        #                    initial val          crypto type     wal_usc    al_cryp   quant,      thresh            auth_client
        
        #bitcoin
        decBTC = dec.Decider2(initial_ana_values['BTC-USD'],        'BTC',      50.0,        .5,   .25,       .024             )
        

        '''
        Non litecoin analysis commented out for testing reasons
        
        #bitcoin
        decBTC = dec.Decider2(initial_ana_values['BTC-USD'],        'BTC',      50.0,        .5,   .25,       .024,             auth_client)
        
        #ether
        decETH = dec.Decider2(initial_ana_values['ETH-USD'],        'ETH',      50.0,        .5,   .25,       .024,             auth_client)
        
        #ether classic
        decETC = dec.Decider2(initial_ana_values['ETC-USD'],        'ETC',      50.0,        .5,   .25,       .024,             auth_client)
        
        #bitcoin cash
        decBCH = dec.Decider2(initial_ana_values['BCH-USD'],        'BCH',      50.0,        .5,   .25,       .024,             auth_client)
        
            
        #litecoin
        decLTC = dec.Decider2(initial_ana_values['LTC-USD'],        'LTC',      50.0,        .5,   .25,       .024,             auth_client)
        #  
        
        general_dict = {'LTC-USD' : decLTC, 'BTC-USD' : decBTC, 'ETH-USD' :  decETH, 'ETC-USD' : decETC, 'BCH-USD' : decBCH}
    
        '''
    
        general_dict = {'BTC-USD' : decBTC}
    
        #create a decider object with specified given variables
        #                                           initial val,  crypto type, start USD, start LTC, quant, threshhold, analyzer object, auth_client(for trading)
        #dec = decider.Decider(float(ws_client.message['price']),        'LTC',      50.0,        .5,   .25,       .024,           analy,             auth_client)
        
        print('setup finished. Main loop Started.')
        prev_prod =  general_client.message['trade_id']
        general_dict[general_client.message['product_id']].anaAdd(float(general_client.message['price']))
        print(general_client.message)
        #print(general_client.message)
        count = 1
        #run forever
        while True:
            if not prev_prod == general_client.message['trade_id']:
                prod = general_client.message['product_id']
                
                prev_prod =  general_client.message['trade_id']
                general_dict[prod].anaAdd(float(general_client.message['price']))
                general_dict[prod].trade()

                
                
                temp = general_dict[prod].ana2
                print("--------------------------------------------------------------------------------------------------------------------")
                # print([count, temp.prev, temp.first_order, temp.second_order, temp._5, temp._5roc, temp._5roc2, temp._10, temp._10, temp._10,
                                    #  temp._30, temp._30roc, temp._30roc2, temp._60, temp._60roc, temp._60roc2])
                # outputFile.writerow([count, temp.prev, temp.first_order, temp.second_order, temp._5, temp._5roc, temp._5roc2, temp._10, temp._10, temp._10,
                #                      temp._30, temp._30roc, temp._30roc2, temp._60, temp._60roc, temp._60roc2])
                outputFile.writerow([count, temp.prev, general_dict[prod].wal.totalVal, general_dict[prod].wal.USD_value,
                                    general_dict[prod].wal.crypto_value])
                print(count)
                # print(general_client.message)
                print(general_dict[prod].ana2.toString()) #10 entries
                general_dict[prod].wal.total(general_dict[prod].ana2.prev)
                print(general_dict[prod].toString())
                count +=1
                
                # toPlot = general_dict[prod].ana2.data[0:9]
                # print(toPlot)
                # plt.plot([0,1,2,3,4,5,6,7,8,9],toPlot)
                # plt.ylabel("Current Val")
                # plt.xlabel("Previous Ticks")
                # plt.show()



                print("--------------------------------------------------------------------------------------------------------------------")

            
if __name__ == '__main__':
    main()