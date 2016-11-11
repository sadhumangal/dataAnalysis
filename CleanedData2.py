#-*- encoding: utf-8 -*-

import pandas as pd
from pandas import Series, DataFrame
import numpy as np
import matplotlib.pyplot as plt
# %matplotlib inline
from dateutil.parser import parse
from datetime import datetime


plotListChoice = ['Latestprice','MaxPrice','MinPrice','Last.Buy1price','Last.Sell1price']
plotList1 = ['Last.Buy1price','Last.Sell1price']
plotList2 = ['Last.Buy1price','Last.Sell1price','MinPrice']
plotList3 = ['Last.Buy1price','Last.Sell1price','MaxPrice']
plotList4 = ['Last.Buy1price','Last.Sell1price','Latestprice']
myList = [plotList1,plotList2,plotList3,plotList4]

def myCleanedData(mypath,mydate):
    try:
        data  = pd.read_csv(mypath)
        dateList = [date for date in data.Date]
        dateListNeed = [parse(date).strftime('%Y%m%d%H%M') for date in dateList]
        panDuan = [date[:8] for date in dateListNeed]       
        dataMINU_IF160420160222 = data[[np.where(panduan[:8]==mydate,True,False) for panduan in panDuan]]      
        return dataMINU_IF160420160222
    except:
        print u'输入路径或时间错误，请确认后重新输入'
    
def myFigure(mypath,mydate,plotList):
    fig = plt.figure(figsize=(15,5))
    ax = fig.add_subplot(111)
    myCleanedData(mypath,mydate)[plotList].plot(ax=ax)
    ax.set_xticks((myCleanedData(mypath,mydate).index.values)[::10])
    ax.set_xticklabels([date[12:16] for date in myCleanedData(mypath,mydate).Date][::10],rotation=30)
    ax.set_xlabel('datetime: %s'% mydate)
    ax.set_ylabel('price')
    ax.set_title(u'%s price trend'% mydate)
    ax.legend(loc='best')