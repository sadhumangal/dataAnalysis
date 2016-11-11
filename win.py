# coding:utf-8


import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 
from pandas import Series, DataFrame

plt.rcParams['font.sans-serif'] = ['SimHei']  #用来显示中文
plt.rcParams['axes.unicode_minus'] = False  #用来正常显示负号

list1 = [0.143,0.29,0.17,0.8]
list2 = range(4)
data = DataFrame(list1,index=list2,columns=[u'胜率'])

fig,ax = plt.subplots(1,1,figsize=(15,8))
data.plot(ax=ax,color='red')
data.plot(kind='bar',ax=ax)
#data.plot(ax=ax,drawstyle='steps-post')
ax.set_xticks([0,1,2,3])
ax.set_xticklabels(['1107','1108','1109','1110'],rotation=0,fontsize='small')
ax.set_title(u'交易胜率统计')
ax.set_xlabel(u'时间')
ax.set_ylabel(u'胜率')
plt.savefig('win.png',bbox_inches='tight')

plt.show()