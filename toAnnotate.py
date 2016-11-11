#-*- encoding: utf-8 -*-


import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 
from pandas import Series, DataFrame
from datetime import datetime

plt.rcParams['font.sans-serif'] = ['SimHei']  #用来显示中文
plt.rcParams['axes.unicode_minus'] = False  #用来正常显示负号

datestr = datetime.now().strftime('%Y%m%d%H%M%S')
fig = plt.figure(figsize=(15,5))
ax = fig.add_subplot(1,1,1)

data = pd.read_csv('2.csv')
dataNeed = DataFrame({u'最高价':data['High'],u'最低价':data['Low']})
dataNeed.plot(ax=ax,linewidth=2.0)
_ = ax.scatter(range(len(data.High))[::2], (['3351.8']*len(data.High))[::2], 2, color='r')   #这个值根据同花顺网站调整

def getData():
    dataBuy  = []
    dataSell = []
    data1 = pd.read_csv('1.csv')   #成交记录数据
    data2 = pd.read_csv('2.csv')   #今日股指数据
    for time1,index in zip(data2.date,data2.index):
        for time2,price,panduan in zip(data1.tradeTime,data1.price,range(len(data1.price))):
            if time1[:-2] == time2[:-2]:
                if (panduan+1) % 2 == 0:
                    dataSell.append((index,price))
                else:
                    dataBuy.append((index,price))
    return dataSell, dataBuy

#dataType = ['1','2','1','2','2','1']    #以1代表卖空仓平空仓，2代表建多仓平多仓
data1 = pd.read_csv('1.csv',encoding="gb2312") #此处必须加上encoding才能显示中文
data11 = data1.sort_index(by='tradeTime')
dataType = []
for todayDirection,todayOffset in zip(data11.direction,data11.offset):
	if todayDirection == u'多' and todayOffset == u'开仓':
		dataType.append('2')
	elif todayDirection == u'空' and todayOffset == u'开仓':
		dataType.append('1')
print dataType

dataSell = getData()[0]
dataBuy = getData()[1]
for datasell,datatype in zip(dataSell,dataType):
	if datatype == '1':
		color,annotateText = 'red', 'cover'
	else:
		color,annotateText = 'black', 'sell'
	ax.annotate(annotateText, color=color, xy=datasell, xycoords='data',
				xytext=(-30,+30), textcoords='offset points',
				fontsize=20, arrowprops=dict(arrowstyle='->', color='red', linewidth=2.5))


for databuy,datatype in zip(dataBuy,dataType):
	if datatype == '1':
		color,annotateText = 'red', 'short'
	else:
		color,annotateText = 'black', 'buy'

	ax.annotate(annotateText, color=color, xy=databuy, xycoords='data',
				xytext=(+0,-40), textcoords='offset points',
				fontsize=20, arrowprops=dict(arrowstyle='->', linewidth=2.5))

ax.set_title('VNPY Trade Statistics')
ax.set_xlabel('datetime: %s'% datestr[:8])
ax.set_ylabel('price')	
ax.set_xticks((data.index.values[1::20]))
#ax.set_xticks((data.index.values[1::20])[:-1])   #如果最后一个的时间点不对则用这两个
#ax.set_xticklabels(([date[:5] for date in ((data['date'][1::20]).values)])[:-1], rotation=30)
ax.set_xticklabels(([date[:5] for date in ((data['date'][1::20]).values)]), rotation=30)
print (data['date'][::20]).values

# plt.ylim(3310,3380)
plt.legend(loc='upper left')
plt.text(2, 3352, '3351.8')
plt.grid()  #显示网格
# plt.autoscale(tight=True)
plt.savefig('%s.png'%datestr, bbox_inches='tight')
plt.show()