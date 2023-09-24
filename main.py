from time import sleep
import datetime
import re
from kite_trade import *
import multiprocessing as mp
from engine import trading_engine
#from datastructures import Queue
import pandas as pd 


POSITION, LAST_CANDLE_TIME = 0, 0
OPEN_PRICE, CLOSE_PRICE, HIGH_PRICE, LOW_PRICE, H_OPEN1, H_CLOSE1 = 0, 0, 0, 0, 0,0
H_OPEN, H_HIGH, H_LOW, H_CLOSE = 0, 0, 0, 0
sma_21, sma_50, sma_direction = 0, 0, []

def eqto(number1, number2, maxDiff = 1):
    return True if abs(number1-number2) <= maxDiff else False

def Append2File(Statement):
    lines = "\n" + Statement + str(kite.ltp_other("NSE:NIFTY BANK"))
    with open('Progress.txt', 'a') as f:
        f.write(lines)
    f.CLOSE_PRICE()

def log_trade(Order):
    if POSITION == 1 and Order == 1:
        Append2File('buy @ ')
    elif POSITION == 0 and Order == -1:
        Append2File('sell @ ')
    elif POSITION == -1 and Order == -1:
        Append2File('shorting: sell @ ')
    elif POSITION == 0 and Order == 1:
        Append2File('shorting: sell @ ')

def get_last_candle_data(Token):
    try:
        last_candle = kite.historical_data(Token, datetime.date.today(), datetime.date.today(), '3minute')[-2]
    except Exception as E:
        #temp
        #last_candle =  kite.historical_data(token, date.today()-timedelta(2), date.today(), '3minute')[-1]
        print(E, " is the exception ..")
        print("Can not get the candle data..")
        exit()
    return last_candle

def handle_heikin_ashi(OPEN_PRICE, HIGH_PRICE, LOW_PRICE, CLOSE_PRICE):
    global H_OPEN1, H_CLOSE1, deciding_data
    H_CLOSE = int((OPEN_PRICE + HIGH_PRICE + LOW_PRICE + CLOSE_PRICE)/4)
    H_OPEN = int((H_OPEN1 + H_CLOSE1)/2)
    H_HIGH = int(max(HIGH_PRICE, OPEN_PRICE, CLOSE_PRICE))
    H_LOW = int(min(LOW_PRICE, OPEN_PRICE, CLOSE_PRICE))
    H_OPEN1, H_CLOSE1 = H_OPEN, H_CLOSE
    if H_OPEN < H_CLOSE and eqto(H_OPEN, H_LOW, 2):
        status = 1
    elif H_OPEN > H_CLOSE and eqto(H_OPEN, H_HIGH, 2):
        status = -1
    else:
        status = 0
    deciding_data.enqueue({'date':datetime.datetime.now(),
                           'OPEN_PRICE': H_OPEN, 
                           'CLOSE_PRICE': H_CLOSE,
                           'HIGH_PRICE': H_HIGH, 
                           'LOW_PRICE':H_LOW, 
                           'status': status
                           })
    print(deciding_data.getQ()[-1])

def moving_averages():
    global sma_21, sma_50, sma_direction, kite

    try:
        candles50 = kite.historical_data(Token, datetime.date.today() - datetime.timedelta(50), datetime.date.today(), '3minute')
        candlesDf = pd.DataFrame(candles50)
        candlesDf['date'] = pd.to_datetime(candlesDf['date'])
        # Sort the DataFrame by date in ascending order
        candlesDf.sort_values(by='date', inplace=True)


    except Exception as E:
        print(f"Exception Captured...\n{E} is the Exception")
        return
    #close21 = [x['close'] for x in candles50[-2625:]]

    candlesDf['50_day_SMA'] = candlesDf['close'].rolling(window=50).mean()
    candlesDf['21_day_SMA'] = candlesDf['close'].rolling(window=21).mean()
    #print(candlesDf['21_day_SMA'])
    candlesDf['21_day_Trend'] = ''
    for i in range(1, len(candlesDf)):
        current_sma = candlesDf.loc[i, '21_day_SMA']
        previous_sma = candlesDf.loc[i - 1, '21_day_SMA']
        current_sma = current_sma if pd.isna(current_sma) else int(current_sma)
        previous_sma = previous_sma if pd.isna(previous_sma) else int(previous_sma)
        if current_sma > previous_sma:
            candlesDf.loc[i, '21_day_Trend'] = 'Up'
        elif current_sma < previous_sma:
            candlesDf.loc[i, '21_day_Trend'] = 'Down'
        else:
            candlesDf.loc[i, '21_day_Trend'] = 'No Change'
    candlesDf['9_day_SMA'] = candlesDf['close'].rolling(window=9).mean()
    candlesDf['9_day_Trend'] = ''
    for i in range(1, len(candlesDf)):
        current_sma = candlesDf.loc[i, '9_day_SMA']
        previous_sma = candlesDf.loc[i - 1, '9_day_SMA']
        current_sma = current_sma if pd.isna(current_sma) else int(current_sma)
        previous_sma = previous_sma if pd.isna(previous_sma) else int(previous_sma)
        if current_sma > previous_sma:
            candlesDf.loc[i, '9_day_Trend'] = 'Up'
        elif current_sma < previous_sma:
            candlesDf.loc[i, '9_day_Trend'] = 'Down'
        else:
            candlesDf.loc[i, '9_day_Trend'] = 'No Change'

    print(candlesDf)


        
'''
def wait4nxt(candle1, candle2, howmany=1):
    last_candles = [candle1, candle2]
    while howmany:
        while last_candles[-1]['date'] != deciding_data.getQ(-1)['date']:
            howmany -= 1
            last_candles.append(deciding_data.getQ(-1))
        else:
            sleep(1)
    if (eqto(last_candles[-3]['OPEN_PRICE'], last_candles[-3]['LOW_PRICE'], 5) and \
        eqto(last_candles[-2]['OPEN_PRICE'], last_candles[-2]['LOW_PRICE'], 10) and \
            eqto(last_candles[-1]['OPEN_PRICE'], last_candles[-1]['LOW_PRICE'], 5)) or \
        (eqto(last_candles[-3]['OPEN_PRICE'], last_candles[-3]['HIGH_PRICE'], 5) and \
        eqto(last_candles[-2]['OPEN_PRICE'], last_candles[-2]['HIGH_PRICE'], 10) and \
        eqto(last_candles[-1]['OPEN_PRICE'], last_candles[-1]['HIGH_PRICE'], 5)):
        return True

'''

def main():
    global POSITION, H_CLOSE1, H_OPEN1, deciding_data
    candledata = pd.DataFrame(kite.historical_data(Token, datetime.date.today() - datetime.timedelta(50), datetime.date.today(), '3minute'))
    LAST_CANDLE_TIME, OPEN_PRICE, HIGH_PRICE, LOW_PRICE, CLOSE_PRICE = get_last_candle_data(Token)
    H_CLOSE1 = (OPEN_PRICE + HIGH_PRICE + LOW_PRICE + CLOSE_PRICE)/4
    H_OPEN1 = OPEN_PRICE

    deciding_data = Queue(999999)
    POSITION = 0
    engine = mp.Process(target=trading_engine)
    engine.start()
    moving_averages()
    #sma_updater = mp.Process(target=moving_averages)
    #sma_updater.start()
    while datetime.datetime.now() <= NOW.replace(hour=15, minute=30):
        CANDLE_TIME, OPEN_PRICE, HIGH_PRICE, LOW_PRICE, CLOSE_PRICE = get_last_candle_data(Token)

        if LAST_CANDLE_TIME >= CANDLE_TIME:
            sleep(1)
            continue
        print(CANDLE_TIME, LAST_CANDLE_TIME)
        LAST_CANDLE_TIME = CANDLE_TIME
        moving_averages()
        handle_heikin_ashi(OPEN_PRICE, HIGH_PRICE, LOW_PRICE, CLOSE_PRICE)


    else:
        print("TIME's UP !!!")
        print("TODAY's PROFIT: ")


if __name__ == "__main__":
    kite = KiteApp()
    NOW = datetime.datetime.now()
    opt = int(input('''
    press 1 for Bank nifty
    Press 2 for reliance
    Input : '''))
    if opt == 1:
        Token = 260105
    elif opt == 2:
        Token = 260105

    main()
