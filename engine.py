from time import sleep
import datetime
from strategy import heikin_ashi_trading_strategy
global deciding_data
NOW = datetime.datetime.now()
def trading_engine():
    while datetime.datetime.now() <= NOW.replace(hour=15, minute=30):
        try:
            candle1 = deciding_data.getQ()[-2]
            candle2 = deciding_data.getQ()[-1]
            heikin_ashi_trading_strategy(candle1, candle2)

        except:
            sleep(4)

