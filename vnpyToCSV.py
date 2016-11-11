# encoding: UTF-8


import datetime
import pymongo
import pandas as pd
from pymongo import MongoClient
from pandas import Series,DataFrame
client = MongoClient('localhost', 27017)


# 从MongoDB中读取分钟数据，并将其转换为DataFrame格式。
db_min = client['VnTrader_1Min_Db'].IF1611# 选择合约分钟数据库
data_df = DataFrame()
# datestr = "20161024" # 选择具体日期。
datestr = datetime.datetime.now().strftime('%Y%m%d')
datestr2 = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
for dataset in db_min.find({'date':datestr}): # 按具体日期查找数据
    dataset_x = {'datetime_stp':Series(dataset['datetime']),'Exchange':Series(dataset['exchange']),
    			'Symbol':Series(dataset['symbol']),'OpenInterest':Series(dataset['openInterest']),
    			'Close':Series(dataset['close']),'Open':Series(dataset['open']),
    			'date':Series(dataset['time'][:8]),'Volume':Series(dataset['volume']),
    			'High':Series(dataset['high']),'Low':Series(dataset['low'])}
    dataset_x_df = DataFrame(dataset_x)
    data_df = pd.concat([data_df, dataset_x_df], axis=0)


data_df.to_csv('MINU_IF1611_'+ datestr2 +'.csv',sep=',')
# print type(data_df.iloc[0]['datetime_stp'])
data_df
