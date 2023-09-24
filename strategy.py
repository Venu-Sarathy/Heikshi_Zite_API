
def heikin_ashi_trading_strategy(candle1, candle2):
    global POSITION
    status1 = candle1['status']
    status2 = candle2['status']

    if POSITION == 0:
        if status1 == status2 == 1:
            if candle1['CLOSE'] < candle2['CLOSE'] and sma_21 > sma_50:
                POSITION = 1
                log_trade(1)
        elif status1 == status2 == -1:
            if candle1['CLOSE'] > candle2['CLOSE'] and sma_21 <= sma_50:
                POSITION = -1
                log_trade(1)

    elif POSITION == 1:
        if candle1['CLOSE'] < candle2['CLOSE'] and eqto(candle2['OPEN'], candle2['LOW'], 17):
            sleep(3)
            return
        POSITION = 0
        log_trade(-1)

    elif POSITION == -1:
        if candle1['CLOSE'] > candle2['CLOSE'] and eqto(candle2['OPEN'], candle2['HIGH'], 15):
            sleep(3)
            return
        POSITION = 0
        log_trade(1)

            
            


def Watcher():
    #_date1 = datetime.now() #_date2 = datetime.now()
    blc_avg, slc_avg = 0, 0
    while datetime.datetime.now() <= NOW.replace(hour=15, minute=27):
        global POSITION
        try:
            candle1 = deciding_data.getQ()[-2]
            candle2 = deciding_data.getQ()[-1]
            status0 = candle1['status']
            status1 = candle2['status']
            #if candle1 != candle2:
            #    sleep(4)
            #    continue
            #Buy Signal
            if POSITION == 0:
                
                if status0 == status1 == 1:
                    if candle1['CLOSE'] < candle2['CLOSE']:
                        #Take Long POsiiton
                        #global POSITION
                        POSITION = 1
                        log_trade(1)
                    else:
                        continue
                elif status0 == status1 == -1:
                    if candle1['CLOSE'] > candle2['CLOSE']:
                        #global POSITION
                        POSITION = -1
                        log_trade(1)
                    else:
                        continue
                #for buy signal
                elif eqto(candle1['OPEN'], candle1['LOW'], 7) and \
                        eqto(candle2['OPEN'], candle2['LOW'], 10):
                    if (candle1['CLOSE'], candle1['HIGH']) < (candle2['CLOSE'], candle2['HIGH']):
                        POSITION = 1
                        log_trade(1)

                #for sell signal
                elif eqto(candle1['OPEN'], candle1['HIGH'], 7) and \
                        eqto(candle2['OPEN'], candle2['HIGH'], 10):
                    if (candle1['CLOSE'], candle1['HIGH']) > (candle2['CLOSE'], candle2['HIGH']):
                        POSITION = -1
                        log_trade(-1)
                else:
                    continue

            elif POSITION == 1:
                if candle1['CLOSE'] < candle2['CLOSE'] and \
                        eqto(candle2['OPEN'], candle2['LOW'], 10):
                    sleep(3)
                    continue
                #sqroff positions blindly
                #global POSITION
                POSITION = 0
                log_trade(-1)

            elif POSITION == -1:
                #if candle1['OPEN'] > candle1['CLOSE']:
                if candle1['CLOSE'] > candle2['CLOSE'] and\
                    eqto(candle2['OPEN'], candle2['HIGH'], 10):
                    sleep(3)
                    continue

                #sqroff positions blindly
                #global POSITION
                POSITION = 0
                log_trade(1)

                #if status0 == status1 == 1:


                #elif (0 or -1) in status0, status1:
                    #Long POSITION Sell(Call long squre of)
                #    global POSITION
                #    POSITION = 0
            else:
                sleep(10)

        except:
            sleep(4)

