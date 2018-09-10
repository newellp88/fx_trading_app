import numpy as np
import pandas as pd

def Ichimoku(df):
    highs = df['High']
    lows = df['Low']
    # Tenkan-sen (conversion line): ((9 period high + 9 period low)/2)
    period9_high = highs.rolling(9).max()
    period9_low = lows.rolling(9).min()
    tenkan_sen = (period9_high + period9_low) / 2

    # Kijun-sen (base line): ((26 period high + 26 period low)/2)
    period26_high = highs.rolling(26).max()
    period26_low = lows.rolling(26).min()
    kijun_sen = (period26_high + period26_low) / 2

    # Senkou Span A (leading span A): ((conversion line + base line) / 2)
    senkou_spanA = ((tenkan_sen + kijun_sen) / 2).shift(26)
    senkou_spanA = np.array(senkou_spanA)

    # Senkou Span B (leading span B): ((52 period high + 52 period low) / 2)
    period52_high = highs.rolling(52).max()
    period52_low = lows.rolling(52).min()
    senkou_spanB = ((period52_high + period52_low) / 2).shift(26)

    # most current closing price plotted 26 time periods behind
    chikou_span = df['Close'].shift(-26)
    chikou_span = np.array(chikou_span)

    data = {'tenkan_sen':tenkan_sen, 'kijun_sen':kijun_sen, 'senkou_spanA':senkou_spanA,
            'senkou_spanB':senkou_spanB, 'chikou_span':chikou_span}
    Ichimoku_df = pd.DataFrame(data)
    return Ichimoku_df

def ema(series, window):
    ema = series.ewm(span=window).mean()
    ema = np.array(ema)
    return ema

def rsi(series, window):
    series = series.astype(float)
    delta = series.diff()
    dUp, dDown = delta.copy(), delta.copy()
    dUp[dUp < 0] = 0
    dDown[dDown > 0] = 0
    RolUp = dUp.rolling(window).mean()
    RolDown = dDown.rolling(window).mean().abs()
    RS = RolUp / RolDown
    RSI = 100. - (100. / (1. + RS))
    return RSI