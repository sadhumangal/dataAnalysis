import pandas as pd
from pandas import Series, DataFrame
import numpy as np
from datetime import datetime
import time
import scipy as sp  
from scipy.optimize import leastsq #最小二乘函数
import pylab as pl

%bookmark db C:/Users/Administrator/Desktop/data160627
%cd db
regularization =0.0000  # 正则化系数lambda  
m = 7   #多项式的次数
charge = 0.4/10000 #交易手续费
mainif_mounth = 9
mainif_day = 15
cal_start_hour = 9
cal_start_min = 30
analytime_hour = 10
analytime_min = 15

#多项式求导
def diff_poly(coe_list):
    temp = np.arange(len(coe_list))
    result=coe_list*temp[::-1]
    return result[:-1]
#拟合函数
def fake_func(p, x):
    f = np.poly1d(p) #产生以p列表为参数的多项式函数
    return f(x)     #返回计算代入值
#残差函数
def residuals(p, y, x):
    ret = y - fake_func(p, x)
    ret = np.append(ret, np.sqrt(regularization)*p) #将lambda^(1/2) * p加在了返回的array的后面
    return ret
#将每天分割开来
def judge_day_number(data): #data为时间序列
    timeslength = len(data)
    day={}
    for i in range(timeslength):
        daystr = data.index[i].strftime('%Y-%m-%d')
        if daystr in day:
            day[daystr] += 1
        else:
            day[daystr]=1
    day=Series(day)
    return day
# 选择最大合约的月份
def judge_day_mounth(data):#data为时间序列
    timeslength = len(data)
    day={}
    for i in range(timeslength):
        daymounth = data.index[i].month
        dayday = data.index[i].day
        if daymounth == mainif_mounth and dayday == mainif_day :
            day=data[i:]
            break
    return day 
# 导入分钟数据
def timestamp_datetime(value):
    format = '%H:%M:%S'
    value = time.localtime(value)
    dt = time.strftime(format, value)
    return dt
# 判断一个时间是否属于某个具体的时间段
def choose_in_time(times): 
    timeslength = len(times)
    day={}
    for i in range(timeslength):
        if times.index[i].hour == cal_start_hour and times.index[i].minute >= cal_start_min:
            day = times[i:]
            break
    return day

def find_time(times): 
    timeslength = len(times)
    index = 0
    for i in range(timeslength):
        if times.index[i].hour == analytime_hour and times.index[i].minute == analytime_min :
            index = i
            break
    return index

def profitt(high,low):
    result = ( high * ( 1 - charge ) - low * ( 1 + charge) )/ (low * ( 1 + charge) )
    return result

data = pd.read_csv('MINU_IF1510.csv', header=0, sep=',') # 读取DAY_IF1506数据，为沪深300股指期货
# 将时间转换为标准格式时间
newdate  = pd.to_datetime(data['Time']) 
#newtime  = pd.to_datetime(data['time']) 
# 获取Time,LatestPrice,Volume指标
newdata = pd.concat([newdate,data[['Latestprice','Volume']]],axis = 1)
#转化为时间序列
newdata.index= newdata['Time']
del newdata['Time']
#选取最大合约日
day = judge_day_mounth(newdata)
#分割合约日天数
num = judge_day_number(day)
profit_total = 0
profit_if = 0
recall = {}
#按天提取
for i in range(len(num)):
    one_day = day[sum(num[:i]):sum(num[:i+1])]
    #选择回归开始时间后的数据
    one_day = choose_in_time( one_day )  
    day_num = len( one_day )
    date = str(one_day.index[0])[:10]
    print date
    one_day_time = Series(one_day.index,index=range(day_num))
    tempx=np.empty(day_num)
    tempx=range(day_num)
    tempy=np.array(one_day['Latestprice'])    
    #IF主力合约累计收益率
    profit_if += ( tempy[day_num - 1] * ( 1 - charge ) - tempy[0] * ( 1 + charge) )/ ( tempy[0] * ( 1 + charge) )
    singal = 0   #0是平仓 1是多仓 2是空仓
    correct = 0
    charge_times = 0
    pre_price = 0
    recall_temp = {} 
    recall_once = 0
    recall_pent = {}
    recall_index = 0
    analytime = find_time(one_day)
    for j in range(analytime,day_num):
        profit = 0
        x=tempx[:j]
        y=tempy[:j]
        #先随机产生一组多项式分布的参数
        Search_st = np.random.randn( m + 1 )
        plsq = leastsq(residuals, Search_st , args=(y, x))#第一个参数是需要拟合的差值函数，第二个是拟合初始值，第三个是传入函数的其他参数

        coe = plsq[0]
        diff1 = fake_func(diff_poly(coe),tempx[j])
        diff2 = fake_func(diff_poly(diff_poly(coe)),tempx[j])

        if diff1 * diff2 > 0  and j != day_num - 1:
            if singal == 0:
                pre_price = tempy[j]
                if diff1 > 0 :  
                    singal = 1
#                    print "开多" + "    " + "%.2f%%" %( profit_total * 100 )
                else:
                    singal = 2
#                    print "开空" + "    " + "%.2f%%" %( profit_total * 100 )
            elif singal !=0:
                recall_temp[j] = tempy[j]

        if diff1 * diff2 < 0 and singal != 0 and j != day_num - 1:
            charge_times += 1
            #计算最大回撤
            if recall_temp:
                recall_once = min ( recall_temp.values() )
                recall_pent[recall_index] = profitt (recall_once, pre_price)
            else:
                recall_pent[recall_index] = 0
            recall_temp = {}  
            recall_index += 1

            if singal == 1:    
                profit = profitt(tempy[j],pre_price)
            elif singal == 2:
                profit = profitt(pre_price,tempy[j])
            profit_total += profit
            if profit >= 0:
                correct += 1
            singal = 0
#            print "平仓" +  "    " + "%.2f%%" %( profit_total * 100 )

        elif j == day_num - 1 and singal != 0:
            charge_times += 1
            #计算最大回撤
            if recall_temp:
                recall_once = min ( recall_temp.values() )
                recall_pent[recall_index] = profitt (recall_once, pre_price)
            else:
                recall_pent[recall_index] = 0
            recall_temp = {}  
            recall_index += 1

            if singal == 1:    
                profit = profitt(tempy[j],pre_price)
            elif singal == 2:
                profit = profitt(pre_price,tempy[j])
            profit_total += profit
            if profit >= 0:
                correct += 1
            singal = 0
#            print "平仓" +  "    " + "%.2f%%" %( profit_total * 100 )

    recall_total = min (recall_pent.values())
    print "策略累计收益率：""%.2f%%" %( profit_total * 100 / len(num))
    print "IF主力合约累计收益率："+ "%.2f%%" %( profit_if * 100 ) 
    print "正确率："+ "%.2f%%" %( correct *100 / charge_times)
    print "最大回撤："+"%.2f%%" %( recall_total * 100 )
#    pl.plot(tempx, fake_func(plsq[0], tempx), label="%d"%(m)+" "'times fitted curve')
#    pl.plot(tempx,  tempy,  label='data points')
#    pl.legend()