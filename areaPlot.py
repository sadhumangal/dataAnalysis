#coding:utf-8
import pandas as pd
from pandas import Series, DataFrame
from matplotlib import pyplot as plt
%matplotlib inline

plt.rcParams['font.sans-serif'] = ['SimHei']  #用来显示中文
plt.rcParams['axes.unicode_minus'] = False  #用来正常显示负号

def text_to_df2(path):
    import codecs
    from pandas import Series
    List = []
    Lindex = []
    Lvalues = []
    with codecs.open('values20170109.txt','r','gbk') as f:
        data = f.readlines()
    for line in data:
        if 'predict_value' in line:
            List.append(line)    

    for L in List:
        Lindex.append(L.split(': ')[0][:5])
        Lvalues.append((L.split('predict_value')[1].strip()).split(' ')[1])
    ser = Series(Lvalues,index=Lindex)
    return ser.map(lambda x:float(x))

def join_df2(path1,path2,save=False,dateNeed=None):
    data= pd.read_csv(path1)
    data.index = data.date
    data = data[['Open']]  
    
    ser = text_to_df2(path2)
    ser.index = ser.index.map(lambda x:x[:5])
    data.index = data.index.map(lambda x:x[:5])
    serDF = DataFrame(ser)
    df = serDF.join(data,how='right')
    
    plt.style.use('seaborn-darkgrid')
    fig, ax = plt.subplots(1,1,figsize=(10,4))
    if dateNeed:
        plt.title(u'Date:%s'%dateNeed)
    plt.fill_between(range(len(df)),df.ix[:,0],color='red',alpha=.5)
    plt.axhline(y=0,ls='--',lw=2,color='gray')
    plt.axhline(y=1.8,ls='--',lw=2,color='green')
    plt.axhline(y=1.4,ls='--',lw=1,color='green')
    plt.axhline(y=1.0,ls='--',lw=0.5,color='green')
    plt.axhline(y=-2,ls='--',lw=2,color='red')
    plt.axhline(y=-1.6,ls='--',lw=1,color='red')
    plt.axhline(y=-1.2,ls='--',lw=0.5,color='red')
    plt.text(10,1.8,u'short1',fontdict=dict(color='blue',size=12))
    #plt.text(10,1.6,u'理论建空仓分界线2',fontdict=dict(color='blue',size=10))
    plt.text(10,1.4,u'short2',fontdict=dict(color='blue',size=10))
    plt.text(10,1.0,u'short3',fontdict=dict(color='blue',size=10))
    plt.text(10,-2,u'long1',fontdict=dict(color='purple',size=12))
    #plt.text(10,-1.8,u'理论建多仓分界线2',fontdict=dict(color='purple',size=10))
    plt.text(10,-1.6,u'long2',fontdict=dict(color='purple',size=10))
    plt.text(10,-1.2,u'long3',fontdict=dict(color='purple',size=10))
    plt.ylabel(u'predict-value')
    plt.xlabel(u'Time')
    df.Open.plot(ax=ax.twinx())
    plt.ylabel(u'price');
    if save:
        plt.savefig('D:\work store private\pic_set\%s.png'%dateNeed,bbox_inches='tight')
