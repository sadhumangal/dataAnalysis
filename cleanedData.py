# encoding: UTF-8


import numpy as np
import pandas as pd
from pandas import Series, DataFrame
import matplotlib.pyplot as plt
from dateutil.parser import parse
# %matplotlib inline

dataMINU_IC1505 = pd.read_csv('MINU_IC1505.csv')
# dataMINU_IC1505.describe()
dataMINU_IC1505[dataMINU_IC1505['Last.Buy1quantity'] > 4] = np.nan
# dataMINU_IC1505.dropna()
# dataMINU_IC1505.dropna().describe()
dataMINU_IC1505[dataMINU_IC1505['Last.Sell1quantity']>3] = np.nan
# dataMINU_IC1505.dropna().describe()
cleanedDataMINU_IC1505 = dataMINU_IC1505.dropna()


dateList = []
for date in cleanedDataMINU_IC1505['Date']:
    dateNeed = parse(date).strftime('%Y%m%d %H:%M')
    dateList.append(dateNeed)
cleanedDataMINU_IC1505['Date'] = dateList
    # print dateList[:10]

# figure = plt.figure(1)
# ax = figure.add_subplot(111)
# cleanedDataMINU_IC1505['Latestprice'].plot(ax=ax,c='r')
# ax.set_xticklabels(dateList[::400],rotation=30)
# ax.set_xlabel('datetime')
# ax.set_title('2015-5-15')



# figure = plt.figure(1)
# ax = figure.add_subplot(111)
# cleanedDataMINU_IC1505['Latestprice'].plot(ax=ax,c='r')
# ax.set_xticklabels(dateList[::400],rotation=30)
# ax.set_xlabel('datetime')
# ax.set_title('2015-5-15')
# plt.grid(True)
# plt.scatter(range(0,6000),['8200']*6000)
# plt.text('100','8250','8200')   



# x = []
# for date in dateList:
#     x.append(date[:8])

# for a in Series(cleanedDataMINU_IC1505['Date'])[:]:
#     print a[:8]

# b = []
# for a in Series(cleanedDataMINU_IC1505['Date'])[:]: 
#     b.append(int(a[:8])==20150417)
# cleanedDataMINU_IC150416 = cleanedDataMINU_IC1505[b]  
# figure = plt.figure(1)
# ax = figure.add_subplot(111)
# cleanedDataMINU_IC150416['MaxPrice'].plot(ax=ax,grid=True,style='g--')
# ax.set_xticklabels((cleanedDataMINU_IC150416['Date'])[::25],rotation=30)

# b = []
# for a in Series(cleanedDataMINU_IC1505['Date'])[:]: 
#     b.append(int(a[:8])==20150420)
# cleanedDataMINU_IC150416 = cleanedDataMINU_IC1505[b]  
# figure = plt.figure(1)
# ax = figure.add_subplot(111)
# cleanedDataMINU_IC150416['MaxPrice'].plot(ax=ax,grid=True,style='g--')
# ax.set_xticklabels((cleanedDataMINU_IC150416['Date'])[::10],rotation=30)
# ax.set_xlabel('datetime')
# ax.set_title('20150420')
# ax.set_ylabel('MaxPrice')

# b = []
# for a in Series(cleanedDataMINU_IC1505['Date'])[:]: 
#     b.append(int(a[:8])==20150421)
# cleanedDataMINU_IC150416 = cleanedDataMINU_IC1505[b]  
# figure = plt.figure(1,figsize=(18,5))
# ax = figure.add_subplot(121)
# cleanedDataMINU_IC150416['MaxPrice'].plot(ax=ax,grid=True,style='g--')
# ax.set_xticklabels((cleanedDataMINU_IC150416['Date'])[::10],rotation=30)
# ax.set_xlabel('datetime')
# ax.set_title('20150421')
# ax.set_ylabel('MaxPrice')
# ax = figure.add_subplot(122)

# c = []
# for d in Series(cleanedDataMINU_IC1505['Date'])[:]: 
#     c.append(int(d[:8])==20150422)
# cleanedDataMINU_IC150416 = cleanedDataMINU_IC1505[c] 
# cleanedDataMINU_IC150416['MaxPrice'].plot(ax=ax,grid=True,style='r--')
# ax.set_xticklabels((cleanedDataMINU_IC150416['Date'])[::5],rotation=30)
# ax.set_xlabel('datetime')
# ax.set_title('20150422')
# ax.set_ylabel('MaxPrice')


def myPlot(myDate,figNumber,myStyle='g--'):
    b = []
    for a in Series(cleanedDataMINU_IC1505['Date'])[:]: 
        b.append(int(a[:8])==int(myDate))
    cleanedDataMINU_IC150416 = cleanedDataMINU_IC1505[b]  
    figure = plt.figure(1,figsize=(18,5))
    ax = figure.add_subplot(int(figNumber))
    cleanedDataMINU_IC150416['MaxPrice'].plot(ax=ax,grid=True,style=myStyle)
    ax.set_xticklabels((cleanedDataMINU_IC150416['Date'])[::10],rotation=30)
    ax.set_xlabel('datetime')
    ax.set_title(myDate)
    ax.set_ylabel('MaxPrice')

