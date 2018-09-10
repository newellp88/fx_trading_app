import numpy as np
import pandas as pd
from api import API
from config import trading_app

def heikin_ashi(df):
    data = []
    df['Open'] = df['Open'].astype(float)
    df['High'] = df['High'].astype(float)
    df['Low'] = df['Low'].astype(float)
    df['Close'] = df['Close'].astype(float)
    d = len(str(df['Close'][0]).split('.')[1])

    for n in range(len(df)-1):
        if n < 2:
            pass
        else:
            Time = df['Time'][n] #.timestamp()
            Close = round(((df['Open'][n] + df['High'][n] + df['Low'][n] + df['Close'][n]) / 4), d)
            Open = round(((df['Open'][n - 1] + df['Close'][n - 1]) / 2), d)
            High = round(max([df['Open'][n], df['High'][n], df['Close'][n]]), d)
            Low = round(min([df['Low'][n], df['Open'][n], df['Close'][n]]), d)
            data.append([Time, Open, High, Low, Close])
    df = pd.DataFrame(data=data, columns=['Time', 'Open', 'High', 'Low', 'Close'])
    df['up'] = (df['Close'] - df['Open']) > 0
    df['down'] = (df['Close'] - df['Open']) < 0
    df['color'] = None
    df.loc[df['up'], 'color'] = 'green'
    df.loc[df['down'], 'color'] = 'red'
    df["up_trend"] = df["color"].groupby((df["color"] == 'red').cumsum()).cumcount()
    df['down_trend'] = df["color"].groupby((df["color"] == 'green').cumsum()).cumcount()
    return df

@trading_app.task
def SimpleHeikinStrategy(accountID, token, instr, window, weight):
    api = API(token, accountID)
    try:
        candles = api.get_candles(instr, window)
        df = heikin_ashi(candles)
        d = len(str(df['Close'][0]).split('.')[1])
        n = len(df) - 1

        sl = df['Open'][n]
        stop_loss = str(round(float(sl), d))
        p = (df['Open'][n] + df['Close'][n]) / 2
        price = round(p, d)

        open_orders = api.openOrders()

        if instr in open_orders:
            pnl = open_orders[instr]['open_pnl']
            tradeIDs = open_orders[instr]['tradeIDs']
            for _id in tradeIDs:
                tsl = api.update_order(_id, price, endpoint="trailingStopLoss")
                print("HEIKIN TRAILING STOP UPDATED")

            # close orders if this candle's color doesn't match the direction
            if open_orders[instr]['Bias'] == 'Long' and df['color'][n] == 'red':
                api.close(instr)
            elif open_orders[instr]['Bias'] == 'Short' and df['color'][n] == 'green':
                api.close(instr)

        else:
            if df['color'][n] == 'green': # go long
                #tp = price + (price - float(stop_loss) * 20)
                take_profit = str(round(float((price + (np.abs(float(stop_loss) - price) * 3))), d))
                try:
                    mo = api.order(instr, weight, price, stop_loss, take_profit)
                    print("HEIKIN LONG ORDER: %s" % instr)
                except Exception as e:
                    print(e)

            elif df['color'][n] == 'red': # go short
                #tp = price - ((stop_loss - price) * 20)
                take_profit = str(round(float((price - (np.abs(float(stop_loss) - price) * 3))), d))
                try:
                    mo = api.order(instr, -weight, price, stop_loss, take_profit)
                    print("HEIKIN SHORT ORDER: %s" % instr)
                except Exception as e:
                    print(e)
    except:
        print("canldes not available right now: %s" % instr)


