from config import trading_app, conn
from indicators import ema, rsi
from api import API

@trading_app.task
def AmazingCrossoverStrategy(accountID, token, instrument, window, weight):

    api = API(token, accountID)
    history = api.get_candles(instrument, window)

    try:
        n = len(history) - 1
        price = history['Close'][n]
        decimal = len(price.split('.')[1])
        price = float(price)

        history['High'] = history['High'].astype(float)
        history['Low'] = history['Low'].astype(float)
        history['median_price'] = (history['High'] + history['Low']) / 2
        history['rsi'] = rsi(history['median_price'], 10)
        history['fast_sma'] = ema(history['Close'], 5)
        history['slow_sma'] = ema(history['Close'], 10)
        history[-1:].to_sql(instrument + '_' + window, conn, if_exists='append')

        oo = api.openOrders()

        # long logic
        if history['fast_sma'][n] > history['slow_sma'][n]:

            if instrument in oo:
                if oo[instrument]['Bias'] == 'Short':
                    api.close(instrument)
                else:
                    tradeID = oo[instrument]['tradeIDs'][0]
                    price = history['Close'][n]
                    tsl = api.update_order(tradeID, price, endpoint='trailingStopLoss')
                    print("AMAZING TRAILING STOP LOSS UPDATED")

            else:
                # if not look for an opportunity
                #if history['rsi'][n] > 50.0:
                stop_loss = str(round(float(price - (price * 0.002)), decimal))
                take_profit = str(round(float(price + (price * 0.02)), decimal))
                try:
                    mo = api.order(instrument, weight, price, stop_loss, take_profit)
                    print("AMAZING went long %s" % instrument)
                except Exception as e:
                    print(e)

        if history['fast_sma'][n] < history['slow_sma'][n]:

            if instrument in oo:
                if oo[instrument]['Bias'] == 'Long':
                    api.close(instrument)
                else:
                    tradeID = oo[instrument]['tradeIDs'][0]
                    price = history['Close'][n]
                    tsl = api.update_order(tradeID, price, endpoint='trailingStopLoss')
                    print("AMAZING TRAILING STOP LOSS UPDATED")

            else:
                #if history['rsi'][n] < 50.0:
                stop_loss = str(round(float(price + (price * 0.002)), decimal))
                take_profit = str(round(float(price - (price * 0.02)), decimal))
                try:
                    mo = api.order(instrument, -weight, price, stop_loss, take_profit)
                    print("AMAZING went short %s" % instrument)
                except Exception as e:
                    print(e)
    except:
        print("candles unavailable right now: %s" % instrument)
