from indicators import Ichimoku
from config import trading_app
from api import API
import numpy as np

@trading_app.task
def IchimokuStrategy(accountID, token, instrument, window, weight):

    api = API(token, accountID)

    try:
        history = api.get_candles(instrument, window)
        ichi = Ichimoku(history)

        n = len(history) - 1
        price = history['Close'][n]
        decimal = len(price.split('.')[1])
        price = float(price)

        # open orders
        oo = api.openOrders()

        # long logic
        if price > ichi['senkou_spanA'][n] and price > ichi['senkou_spanB'][n]:
            # price is above the cloud

            if instrument in oo:
                if oo[instrument]['Bias'] == 'Short':
                    api.close(instrument)
                elif oo[instrument]['Bias'] == 'Long':
                    tradeID = oo[instrument]['tradeIDs'][0]
                    tsl = api.update_order(tradeID, price, endpoint='trailingStopLoss')
                    print("ICHIMOKU TRAILING STOP LOSS UPDATED")

            else:
                if ichi['tenkan_sen'][n] > ichi['kijun_sen'][n]: # omit chikou span signal
                    stop_loss = str(round(float(ichi['kijun_sen'][n]), decimal))
                    take_profit = str(round(float((price + (np.abs(float(stop_loss) - price) * 3))), decimal))
                    try:
                        mo = api.order(instrument, weight, price, stop_loss, take_profit)
                        print("ICHIMOKU went long %s" % instrument)
                    except Exception as e:
                        print(e)

        # short logic
        if price < ichi['senkou_spanA'][n] and price < ichi['senkou_spanB'][n]:

            # check to see if there's already a position
            if instrument in oo:
                if oo[instrument]['Bias'] == 'Long':
                    api.close(instrument)
                elif oo[instrument]['Bias'] == 'Short':
                    tradeID = oo[instrument]['tradeIDs'][0]
                    tsl = api.update_order(tradeID, price, endpoint='trailingStopLoss')
                    print("ICHIMOKU TRAILING STOP LOSS UPDATED")

            else:
                # if not, let's look for an opportunity
                if ichi['tenkan_sen'][n] < ichi['kijun_sen'][n]:
                    stop_loss = str(round(float(ichi['kijun_sen'][n]), decimal))
                    take_profit = str(round(float((price - (np.abs(float(stop_loss) - price) * 3))), decimal))
                    try:
                        mo = api.order(instrument, -weight, price, stop_loss, take_profit)
                        print("ICHIMOKU went short %s" % instrument)
                    except Exception as e:
                        print(e)
    except:
        print("candles unavailable right now: %s" % instrument)