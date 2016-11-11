# coding:utf-8


import pandas as pd
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from pandas import Series, DataFrame
from datetime import datetime
import random

plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来显示中文
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

datestr = datetime.now().strftime('%Y%m%d%H%M%S')
fig = plt.figure(1, figsize=(15, 5))
ax = fig.add_subplot(1, 1, 1)
todayLine = 3379.4

data = pd.read_csv('2.csv')
dataNeed = DataFrame({u'最高价': data['High'], u'最低价': data['Low']})
dataNeed.plot(ax=ax, linewidth=2.0)
_ = ax.scatter(range(len(data.High))[::2], ((
    ['%s' % todayLine]) * len(data.High))[::2], 2, color='r')  # 这个值根据同花顺网站调整


def getData():
    dataBuy = []
    dataSell = []
    data1 = pd.read_csv('1.csv', encoding="gb2312")  # 成交记录数据
    data2 = pd.read_csv('2.csv')  # 今日股指数据
    for time1, index in zip(data2.date, data2.index):
        for time2, price, panduan in zip(data1.tradeTime, data1.price, data1.offset):
            if time1[:-3] == time2[:-3]:
                if panduan == u'平仓':
                    dataSell.append((index, price))
                else:
                    dataBuy.append((index, price))
    return dataSell, dataBuy


# dataType = ['1','2','1','2','2','1']     #以1代表卖空仓平空仓，2代表建多仓平多仓
data1 = pd.read_csv('1.csv', encoding="gb2312")  # 此处必须加上encoding才能显示中文
data11 = data1.sort_index(by='orderID')
# print data11
dataType = []
for todayDirection, todayOffset in zip(data11.direction, data11.offset):
    if todayDirection == u'多' and todayOffset == u'开仓':
        dataType.append('2')
    elif todayDirection == u'空' and todayOffset == u'开仓':
        dataType.append('1')
# print dataType


dataSell = getData()[0]
dataBuy = getData()[1]
# print dataSell
# print dataBuy

for datasell, datatype in zip(dataSell, dataType):
    if datatype == '1':
        color, annotateText = 'red', 'cover'
    else:
        color, annotateText = 'black', 'sell'
    ax.annotate(annotateText, color=color, xy=datasell, xycoords='data',
                xytext=(-30, +35), textcoords='offset points',
                fontsize=20, arrowprops=dict(arrowstyle='->', color='red', linewidth=2.5))


for databuy, datatype in zip(dataBuy, dataType):
    if datatype == '1':
        color, annotateText = 'red', 'short'
    else:
        color, annotateText = 'black', 'buy'

    ax.annotate(annotateText, color=color, xy=databuy, xycoords='data',
                xytext=(-10, -40), textcoords='offset points',
                fontsize=20, arrowprops=dict(arrowstyle='->', linewidth=2.5))

ax.set_title('VNPY Trade Statistics')
ax.set_xlabel('datetime: %s' % datestr[:8])
ax.set_ylabel('price')
ax.set_xticks((data.index.values[1::20]))
# ax.set_xticks((data.index.values[1::20])[:-1])   #如果最后一个的时间点不对则用这两个
#ax.set_xticklabels(([date[:5] for date in ((data['date'][1::20]).values)])[:-1], rotation=30)
ax.set_xticklabels(
    ([date[:5] for date in ((data['date'][1::20]).values)]), rotation=30)
#print (data['date'][::20]).values

# plt.ylim(3310,3380)
# plt.legend(loc='lower left')
plt.legend(loc='upper right')
plt.text(2, int(todayLine) + 1, '%s' % todayLine)
plt.grid()  # 显示网格
# plt.autoscale(tight=True)
plt.savefig('%s.png' % datestr, bbox_inches='tight')
# plt.show()


######以下为用100阶多项式拟合的曲线################
dataPolyFitNeed = Series(data.High)  # [70:80]
x = dataPolyFitNeed.index
y = dataPolyFitNeed.values
fp1, residuals, rank, sv, rcond = sp.polyfit(x, y, 120, full=True)  # 拟合函数
f1 = sp.poly1d(fp1)
fx = sp.linspace(0, x[-1], 1000)
# def error(f,x,y):
# 	return sp.sum((f(x)-y)**2)
pngIndex = datestr + str(random.randint(0, 1000))
fig2 = plt.figure(2, figsize=(15, 5))
ax2 = fig2.add_subplot(1, 1, 1)
ax2.set_title(u'用多项式对交易进行拟合')
ax2.set_xlabel('datetime: %s' % datestr[:8])
ax2.set_ylabel('price')
ax2.set_xticks((data.index.values[1::20]))
ax2.scatter(range(len(data.High))[
            ::2], (['%s' % todayLine] * len(data.High))[::2], 2, color='green')
ax2.set_xticklabels(
    ([date[:5] for date in ((data['date'][1::20]).values)]), rotation=30)

plt.text(2, int(todayLine) + 1, '%s' % todayLine)
plt.grid()  # 显示网格
plt.plot(fx, f1(fx), linewidth=2.5, color='red', linestyle='-')
# plt.autoscale(tight=True)
plt.savefig('%s.png' % pngIndex, bbox_inches='tight')
plt.show((fig, fig2))
