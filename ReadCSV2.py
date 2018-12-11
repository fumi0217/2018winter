# -*- coding: utf-8 -*-
"""
Created on Tue Dec 11 02:00:27 2018

@author: fumi
"""

from time import time
import glob
import pandas as pd

def main():
    CSV = calcTime(readCSVs)
    print('普通にCエンジンのread_csvメソッドを使って読み込むと{}秒かかりました。'.format(CSV['time']))       


    
def readCSVs():
    #csvファイルのパスを取得
    searchPath = r".\data\*.csv"
    pathArray = glob.glob(searchPath)
    
    #pythonエンジンのread_csvを用いて、csvファイルを読み込む
    for path in pathArray:
        tmpCSV = pd.read_csv(path, encoding="SHIFT-JIS", index_col='DateTime', names=['Tid', 'Dealable', 'Pair', 'DateTime', 'Buy', 'Sell'], skiprows=1, engine="c")
        
        if 'CSV' in locals():
            CSV = pd.concat([CSV, tmpCSV])
            
        else:
            CSV = tmpCSV
    return CSV


#関数を引数に渡して、関数の実行時間を測るメソッドです。
def calcTime(func):
    start = time()
    r = func()
    return {'value' : r, 'time' : time()-start}
    

if __name__ == '__main__':
    main()