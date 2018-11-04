'''
Created on Jun 6, 2018

@author: dpolyakov

This script will be the launching point of the bot overall. 

'''

#import a bunch of stuff that maybe i need.


import decider2 as dec
import ticker
import cbpro, time, datetime, _csv


def main():
    print("Bot Started")
    #excel recorder initialization
    with open("C:/Users/Danny/Documents/GitHub/bot/data/output.csv", 'w', encoding='utf8') as f:
        outputFile = _csv.writer(f, delimiter=',', lineterminator='\n')    
        
        #data for testing purposes
        
        btcRed = _csv.reader(open("C:/Users/Danny/Documents/GitHub/bot/data/coinbaseUSD_1-min_data_2014-12-01_to_2018-06-27.csv", 'r', encoding='utf8'), delimiter=',', lineterminator='/n')   
        tempBtcList = []
        for row in btcRed:
            tempBtcList.append(row)
        btcData = tempBtcList[900000 : (len(tempBtcList)  - 1)]

        # ethRed = _csv.reader(open("C:/Users/Danny/Documents/GitHub/bot/data/gemini_ETHUSD_2018_1min.csv", 'r', encoding='utf8'), delimiter=',', lineterminator='/n')
        # tempEthList = []
        # for row in ethRed:
        #     tempEthList.append(row)
        # ethData = tempBtcList[0 : (len(tempBtcList)  - 1)] 

        ''' 
        ltcData = _csv.reader(open("FILEPATH", 'r', encoding='utf8'), delimiter=',', lineterminator='\n')    
        ethData = _csv.reader(open("FILEPATH", 'r', encoding='utf8'), delimiter=',', lineterminator='\n')    
        etcData = _csv.reader(open("FILEPATH", 'r', encoding='utf8'), delimiter=',', lineterminator='\n')    
        bchData = _csv.reader(open("FILEPATH", 'r', encoding='utf8'), delimiter=',', lineterminator='\n')    
        
        data_dict = {'LTC-USD' : ltcData, 'BTC-USD' : btcData, 'ETH-USD' :  ethData, 'ETC-USD' : etcData, 'BCH-USD' : bchData}
        '''
        data_dict = {'BTC-USD' : btcData}#, 'ETH-USD' :  ethData}
    
        #end of data initialization
    
    
    
    
        #bitcoin
        decBTC = dec.Decider2(float(btcData[0][7]),        'BTC',     90.0, 0.0,   .005,       .024,             auth=None)
        #ether
        # decETH = dec.Decider2(float(ethData[0][1]),        'ETH',      50.0,        .5,   .25,       .024,              auth=None)


        '''
        #litecoin
        decLTC = dec.Decider2(initial_ana_values['LTC-USD'],        'LTC',      50.0,        .5,   .25,       .024,             auth_client)
        #                                initial val          crypto type     wal_usc    al_cryp   quant,      thresh            auth_client
        
        
        #ether
        decETH = dec.Decider2(initial_ana_values['ETH-USD'],        'ETH',      50.0,        .5,   .25,       .024,             auth_client)
        
        #ether classic
        decETC = dec.Decider2(initial_ana_values['ETC-USD'],        'ETC',      50.0,        .5,   .25,       .024,             auth_client)
        
        #bitcoin cash
        decBCH = dec.Decider2(initial_ana_values['BCH-USD'],        'BCH',      50.0,        .5,   .25,       .024,             auth_client)
        
        
        
        general_dict = {'LTC-USD' : decLTC, 'BTC-USD' : decBTC, 'ETH-USD' :  decETH, 'ETC-USD' : decETC, 'BCH-USD' : decBCH}
    
        '''

        general_dict = {'BTC-USD' : decBTC} #, 'ETH-USD' :  decETH
        #end of decider initlaization

        print('setup finished. Main loop Started.')
        dataPointIndex = 0
        maxDataLength = len(btcData)
        #run while we have datapoints to evaluate
        for entries in general_dict:
            print([dataPointIndex, general_dict[entries].ana2.prev, general_dict[entries].wal.totalVal, general_dict[entries].wal.USD_value, general_dict[entries].wal.crypto_value])

        while dataPointIndex < maxDataLength:
            #first, add data to the decider objects
            # if( ( (dataPointIndex / maxDataLength) * 100) % 5 is 0 ) :
            print(dataPointIndex / maxDataLength * 100)
            for entries in general_dict:
                # print(float(data_dict[entries][dataPointIndex][7]))
                general_dict[entries].ana2.add(float(data_dict[entries][dataPointIndex][7]))

                general_dict[entries].trade()

                
                
                temp = general_dict[entries].ana2
                general_dict[entries].wal.total(general_dict[entries].ana2.prev)
                
                # print("--------------------------------------------------------------------------------------------------------------------")
                # print([count, temp.prev, temp.first_order, temp.second_order, temp._5, temp._5roc, temp._5roc2, temp._10, temp._10, temp._10,
                                    #  temp._30, temp._30roc, temp._30roc2, temp._60, temp._60roc, temp._60roc2])
                # outputFile.writerow([dataPointIndex, temp.prev, temp.first_order, temp.second_order, temp._5, temp._5roc, temp._5roc2, temp._10, temp._10, temp._10,
                #                      temp._30, temp._30roc, temp._30roc2, temp._60, temp._60roc, temp._60roc2, general_dict[entries].wal.totalVal, general_dict[entries].wal.USD_value,
                #                      general_dict[entries].wal.crypto_value])
                # outputFile.writerow([dataPointIndex, temp.prev, general_dict[entries].wal.totalVal, general_dict[entries].wal.USD_value,
                                    # general_dict[entries].wal.crypto_value] )
            dataPointIndex += 1

        for entries in general_dict:
            general_dict[entries].wal.total(general_dict[entries].ana2.prev)
            print([dataPointIndex, general_dict[entries].ana2.prev, general_dict[entries].wal.totalVal, general_dict[entries].wal.USD_value, general_dict[entries].wal.crypto_value])

if __name__ == '__main__':
    main()