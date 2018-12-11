# -*- coding: utf-8 -*-
"""
Created on Tue Dec 11 20:37:07 2018

@author: fumi
"""

from time import time
import glob
import pandas as pd
import numpy as np
from multiprocessing import Pool
import pickle
import matplotlib.pyplot as plt
import mpl_finance as mpf
from matplotlib import ticker
import matplotlib.dates as mdates

def main():
    #初回のみ実行要
    CSV = readCSVs()
    pickle.dump(CSV, open(r'./data/usd_jpy_2017_protocol4.pkl', 'wb'), protocol=3)
    
    #バイト配列に変換されたcsvファイルを読み込む
    CSV = calcTime(lambda: pickle.load(open(r'./data/usd_jpy_2017_protocol4.pkl', 'rb')))
    print('pickleのプロトコルバージョン4で読み込むと{}秒かかりました。'.format(CSV['time']))
    
    CSV['value'].index = pd.to_datetime(CSV['value'].index)

    del CSV['value']['Tid']
    del CSV['value']['Dealable']
    del CSV['value']['Pair']
    
    #ローソク足作成
    2017 = CSV['value'].resample('D', how='ohlc')
    2017 = 2017.xs('Buy', axis=1, drop_level=True)
    2017.plot()
    candleChart(2017)

    
    
def readCSVs():
    #csvファイルのパスを取得
    searchPath = r".\data\*.csv"
    pathArray = glob.glob(searchPath)
    
    #6つにマルチスレッド化させる
    pool = Pool(5)
    CSV = pd.concat(pool.map(readCSV,pathArray))
    return CSV

def readCSV(path):
    return pd.read_csv(path, encoding="SHIFT-JIS", index_col='DateTime', names=['Tid', 'Dealable', 'Pair', 'DateTime', 'Buy', 'Sell'], skiprows=1, engine="c")



#関数を引数に渡して、関数の実行時間を測るメソッドです。
def calcTime(func):
    start = time()
    r = func()
    return {'value' : r, 'time' : time()-start}

def candleChart(data, width=0.8):
    fig, ax = plt.subplots()
    
    mpf.candlestick2_ohlc(ax, opens=data.open.values, closes=data.close.values, lows=data.low.values, highs=data.high.values, width=width, colorup="r", colordown="b")
    xdate = data.index
    ax.xaxis.set_major_locator(ticker.MaxNLocator(6))
    
    def mydate(x, pos):
        try:
            return xdate[int(x)]
        except IndexError:
            return ''
        
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(mydate))
    ax.format_xdata = mdates.DateFormatter('%Y-%m-%d')
    
    fig.autofmt_xdate()
    fig.tight_layout()
    
    return fig,ax
    

if __name__ == '__main__':
    main()

