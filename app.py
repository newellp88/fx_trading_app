from flask import Flask, render_template
import pandas as pd
import numpy as np
import os

app = Flask(__name__)

def find_csv(instr):
    folder = 'oanda/data/'
    for files in os.walk(folder):
        for file in files[2]:
            if instr in file:
                return folder + file

@app.route('/<instr>')
def index(instr):
    file = find_csv(instr)
    df = pd.read_csv(file)
    candle_data = list()
    for idx, row in df.iterrows():
        t = int(pd.to_datetime(row['Time']).timestamp())
        candle_data.append([t, [row['Open'], row['High'], row['Low'], row['Close']]])
    candle_high = df['High'].max()
    candle_low = df['Low'].min()
    candle_range = "%.f:%f:0.1" % (candle_low, candle_high)
    volume_high = df['Volume'].max()
    volume_low = df['Volume'].min()
    volume_data = list(df['Volume'])
    ohlcv_title = "%s H1 Chart" % instr
    data = list(df['Close'].astype(float))
    return render_template("bootstrap_template.html", ohlcv_title=ohlcv_title, candle_range=candle_range,
                            candle_data=candle_data, volume_data=volume_data,
                           data=data, candle_high=candle_high, candle_low=candle_low, volume_high=volume_high,
                           volume_low=volume_low)
