from config import conn, trading_app
import matplotlib.pyplot as plt
from datetime import datetime
import pandas as pd
from api import API
import json

@trading_app.task
def save_account_summary(name, token, accountID):
    title = '%s_account_summary' % name
    api = API(token, accountID)
    summary = api.account_summary()
    summary['time'] = datetime.now()
    df = pd.DataFrame.from_dict(summary, orient='index').T
    df.to_sql(title, conn, if_exists='append')


"""
@app.task
def plot_account(token, accountID, key, _name):
    api = API(token, accountID)
    summary = api.account_summary()

    x = [datetime.now()]
    y = [summary[key]]

    i = 0
    plt.ion()
    while True:
        summary = api.account_summary()
        y.append(summary[key])
        x.append(datetime.now())
        plt.title(_name + ' ' + key)
        plt.plot(x, y, label=key if i == 0 else "", color='blue' if i == 0 else "")
        plt.legend()
        plt.draw()
        i += 1

    plt.show(block = True)



@app.task
def plot_nav_and_balance(token, accountID, t=60):

    api = API(token, accountID)
    summary = api.account_summary()

    x = [datetime.now()]
    nav = [summary['nav']]
    bal = [summary['balance']]

    plt.ion()

    i = 0
    while True:
        summary = api.account_summary()
        nav.append(summary['nav'])
        bal.append(summary['balance'])
        x.append(datetime.now())
        plt.title('NAV vs. Balance')
        plt.plot(x, nav, label='NAV' if i == 0 else "", color='blue' if i == 0 else "")
        plt.plot(x, bal, label='Balance' if i == 0 else "", color='red' if i == 0 else "")
        plt.legend()
        plt.draw()
        plt.pause(t)
        i += 1

    plt.show(block=True)
"""
