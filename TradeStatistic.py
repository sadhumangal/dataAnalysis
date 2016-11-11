#coding:utf-8

from __future__ import division
import numpy as np
import pandas as pd


data = pd.read_csv('121.csv',encoding='gb2312')  #读取交易记录，进行统计
myPrice = []
myDirection = []
for x,y in zip(data.price,data.direction):
    myPrice.append(x)
    myDirection.append(y)
myPrice = myPrice[::-1]
myDirection = myDirection[::-1]
winPointsSum = []
lostPointsSum =[]
countDuo = 0
countKong = 0
countKongWin = 0
countKongLost = 0
countPing = 0
countDuoWin = 0
countDuoLost = 0
for price,index,direction in zip(myPrice,range(len(myPrice)),myDirection):
    if index % 2 == 0:
        if direction == u'空':
            countKong += 1
            if price - myPrice[index+1] > 0:
                print u'第%s笔'%(int(index/2 + 1)), u'买空赚了', price - myPrice[index+1], u'个点', u'胜'
                winPointsSum.append(price-myPrice[index+1])
                countKongWin += 1
            elif price - myPrice[index+1] == 0:
                countPing += 1
            else:
                print u'第%s笔'%(int(index/2 + 1)), u'买空赔了', -(price - myPrice[index+1]), u'个点', u'败'
                lostPointsSum.append(price - myPrice[index+1])
                countKongLost += 1
        if direction == u'多':
            countDuo += 1
            if price - myPrice[index+1] > 0:
                print u'第%s笔'%(int(index/2 + 1)), u'买多赔了', price - myPrice[index+1], u'个点', u'败'
                lostPointsSum.append(price - myPrice[index+1])
                countDuoLost += 1
            elif price - myPrice[index+1] ==0:
                countPing += 1
            else:
                print u'第%s笔'%(int(index/2 + 1)), u'买多赚了',-(price - myPrice[index+1]), u'个点',  u'胜'
                winPointsSum.append(-(price-myPrice[index+1]))
                countDuoWin +=1
    else:
        pass
winPointsSum = np.array(winPointsSum).sum()
lostPointsSum = np.array(lostPointsSum).sum()
print u'今日胜点数', winPointsSum
print u'今日败点数', lostPointsSum
print u'今日交易次数', int(len(myPrice)/2)
print u'今日建多仓次数', countDuo
print u'今日监空仓次数', countKong
print u'建多仓胜次数', countDuoWin
print u'建空仓胜次数', countKongWin
print u'平次数', countPing
print u'今日胜率', (countKongWin + countDuoWin) / (len(myPrice)/2)