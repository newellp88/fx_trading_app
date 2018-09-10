import json
import requests
import pandas as pd

class API:

    def __init__(self, token, accountID):
        self.url = 'https://api-fxpractice.oanda.com'
        self.session = requests.Session()
        self.token = token
        self.accountID = accountID

    def account_summary(self):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {}'.format(self.token)
        }
        r = "%s/v3/accounts/%s/summary" % (self.url, self.accountID)
        summary = self.session.get(r, headers=headers)

        summary = json.loads(summary.content.decode('utf-8'))['account']

        account_summary = {
            'margin_used': summary['marginUsed'],
            'nav': summary['NAV'],
            'carry_costs': summary['financing'],
            'n_open_pos': summary['openPositionCount'],
            'total_pnl': summary['pl'],
            'open_pnl': summary['unrealizedPL'],
            'balance': summary['balance']
        }
        return account_summary

    def get_ticker(self, symbol, window):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {}'.format(self.token)
        }
        params = {
            "granularity": window
        }
        r = "%s/v3/instruments/%s/candles" % (self.url, symbol)
        try:
            return self.session.get(r, headers=headers, params=params)
        except:
            print('Connection error')

    def get_candles(self, symbol, window):
        ticker = self.get_ticker(symbol, window)
        try:
            candles = json.loads(ticker.content.decode('utf-8'))
            data = list()
            for candle in candles['candles']:
                dt = candle['time'].apply(lambda x: x[0].timestamp(), axis=1).astype(int)
                Open = candle['mid']['o']
                High = candle['mid']['h']
                Low = candle['mid']['l']
                Close = candle['mid']['c']
                Volume = candle['volume']
                update = [dt, Open, High, Low, Close, Volume]
                data.append(update)
            df = pd.DataFrame(data, columns=['Time', 'Open', 'High', 'Low', 'Close', 'Volume'])
            return df
        except:
            print("Error getting candles")

    def order(self, instrument, units, price, stop_loss, take_profit, _type='MARKET'):
        """
         {
            "order": {
                "price": "1.5000",
                "stopLossOnFill": {
                    "timeInForce": "GTC",
                    "price": "1.7000"
                },
                "takeProfitOnFill": {
                    "price": "1.14530"
                },
                "timeInForce": "GTC",
                "instrument": "USD_CAD",
                "units": "-1000",
                "type": "LIMIT",
                "positionFill": "DEFAULT"
            }
        }

        :return:
        """
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {}'.format(self.token)
        }
        params = {
            "order": {
                    "price": price,
                    "stopLossOnFill": {
                        "timeInForce": "GTC",
                        "price": stop_loss
                    },
                    "takeProfitOnFill": {
                        "price": take_profit
                    },
                    "timeInForce": "FOK",
                    "instrument": instrument,
                    "units": units,
                    "type": _type,
                    "positionFill": "DEFAULT"
                    }
        }
        r = "%s/v3/accounts/%s/orders" % (self.url, self.accountID)
        return self.session.post(r, headers=headers, data=json.dumps(params)).json()

    def openOrders(self):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {}'.format(self.token)
        }
        r = "%s/v3/accounts/%s/openPositions" % (self.url, self.accountID)
        oo = self.session.get(r, headers=headers)
        oo = json.loads(oo.content.decode('utf-8'))['positions']
        open_orders = dict()
        for pos in oo:
            if float(pos['long']['units']) > 0:
                bias = 'Long'
                tradeIDs = pos['long']['tradeIDs']
            elif float(pos['short']['units']) < 0:
                bias = 'Short'
                tradeIDs = pos['short']['tradeIDs']
            else:
                pass

            open_orders[pos['instrument']] = {
                'margin_used': pos['marginUsed'],
                'open_pnl': pos['unrealizedPL'],
                'Bias': bias,
                'tradeIDs': tradeIDs
            }
        return open_orders

    def close(self, instrument):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {}'.format(self.token)
        }
        params = {
            "longUnits": "ALL",
            "shortUnits": "ALL"
        }
        r = "%s/v3/accounts/%s/positions/%s/close" % (self.url, self.accountID, instrument)
        return self.session.get(r, headers=headers, params=params)

    def transactions(self):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {}'.format(self.token)
        }
        params = {
            "from": 1,
            "to": 10000
        }
        r = "%s/v3/accounts/%s/transactions/idrange" % (self.url, self.accountID)
        return self.session.get(r, headers=headers, params=params)

    def update_order(self, tradeID, price, endpoint="trailingStopLoss"):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {}'.format(self.token)
        }
        if endpoint == 'stopLoss':
            params = {'stopLoss': {'timeInForce': 'GTC', 'price': price}}
        elif endpoint == 'takeProfit':
            params = {'takeProfit': {'timeInForce': 'GTC', 'price': price}}
        elif endpoint == 'trailingStopLoss':
            d = int(len(str(price).split('.')[1]))
            if d == 3 or d == 4:
                distance = 0.02
            if d == 5:
                distance = 0.002
            else:
                distance = 0.20
            params = {'trailingStopLoss': {'distance': str(distance)}}
        r = "%s/v3/accounts/%s/trades/%s/orders" % (self.url, self.accountID, tradeID)
        return self.session.put(r, headers=headers, data=json.dumps(params)).json()