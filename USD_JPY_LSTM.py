# -*- coding: utf-8 -*-


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import preprocessing

import glob
from multiprocessing import Pool
import pickle

from keras.models import Sequential
from keras.layers.core import Dense, Activation
from keras.layers.recurrent import LSTM
from keras.optimizers import Adam
from keras.callbacks import EarlyStopping

class Prediction:
    
    def __init__(self):
        self.length_of_sequences = 25
        self.in_neurons = 4
        self.out_neurons = 1
        self.hidden_neurons = 300
        
    def load_data(self, data, n_prev=10):
        X, Y = [], []
        target = data[['close']]
        for i in range(len(data)-n_prev):
            X.append(data.iloc[i:(i+n_prev)].as_matrix())
            Y.append(target.iloc[i+n_prev].as_matrix())
        retX = np.array(X)
        retY = np.array(Y)
        return retX, retY
    
    def create_model(self):
        model = Sequential()
        model.add(LSTM(self.hidden_neurons, batch_input_shape=(None, self.length_of_sequences, self.in_neurons), return_sequences=False))
        model.add(Dense(self.out_neurons))
        model.add(Activation("linear"))
        optimizer = Adam(lr=0.001, beta_1=0.9, beta_2=0.999)
        model.compile(loss="mape", optimizer=optimizer)
        return model
    
    def train(self, X_train, Y_train):
        early_stopping = EarlyStopping(monitor='loss', patience=10, verbose=1)
        model = self.create_model()
        model.fit(X_train, Y_train, batch_size=10, epochs=100, callbacks=[early_stopping])
        return model
    
def readCSVs():
    #csvファイルのパスを取得
    searchPath = r".\data\*.csv"
    pathArray = glob.glob(searchPath)
    
    #6つにマルチスレッド化させる
    pool = Pool(5)
    CSV = pd.concat(pool.map(readCSV,pathArray))
    return CSV

def readCSV(path):
    return pd.read_csv(path, encoding="SHIFT-JIS", engine="c")
    #return pd.read_csv(path, encoding="SHIFT-JIS", index_col='DateTime', names=['Tid', 'Dealable', 'Pair', 'DateTime', 'Buy', 'Sell'], skiprows=1, engine="c")
    
if __name__ == "__main__":
    
    prediction = Prediction()
    
    #初回のみ実行要
    #CSV = readCSVs()
    #CSV = readCSV(r"./data/USDJPY.csv")
    #pickle.dump(CSV, open(r'./data/usd_jpy_2007-2018_protocol4.pkl', 'wb'), protocol=3)
    
    #バイト配列に変換されたcsvファイルを読み込む
    data = pickle.load(open(r'./data/usd_jpy_2007-2018_protocol4.pkl', 'rb'))
    
    data.columns = ['date', 'open', 'high', 'low', 'close']
    data['date'] = pd.to_datetime(data['date'], format='%Y-%m-%d')
    
    data[['open', 'high', 'low', 'close']] = preprocessing.scale(data[['open', 'high', 'low', 'close']])
    data = data.sort_values(by='date')
    data = data.reset_index(drop=True)
    data = data.loc[:, ['open', 'high', 'low', 'close']]
    
    split_pos = int(len(data) * 0.8)
    x_train, y_train = prediction.load_data(data[['open', 'high', 'low', 'close']].iloc[0:split_pos], prediction.length_of_sequences)
    x_test, y_test = prediction.load_data(data[['open', 'high', 'low', 'close']].iloc[split_pos:], prediction.length_of_sequences)
    
    model = prediction.train(x_train, y_train)
    
    predicted = model.predict(x_test)
    result = pd.DataFrame(predicted)
    result.columns = ['predict']
    result['actual'] = y_test
    result.plot()
    plt.show()