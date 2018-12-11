# -*- coding: utf-8 -*-
"""
Created on Tue Dec 11 21:30:27 2018

@author: fumi
"""

from time import time
import glob
import pandas as pd
from multiprocessing import Pool
import pickle

def main():
    #初回のみ実行要
    CSV = readCSVs()
    pickle.dump(CSV, open(r'./data/usd_jpy_2017_protocol1.pkl', 'wb'), protocol=1)
    
    #バイト配列に変換されたcsvファイルを読み込む
    CSV1 = calcTime(lambda: pickle.load(open(r'./data/usd_jpy_2017_protocol1.pkl', 'rb')))
    print('pickleのプロトコルバージョン1で読み込むと{}秒かかりました。'.format(CSV1['time']))

    
    
def readCSVs():
    #csvファイルのパスを取得
    searchPath = r".\data\*.csv"
    pathArray = glob.glob(searchPath)
    
    #5つにマルチスレッド化させる
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
    

if __name__ == '__main__':
    main()
