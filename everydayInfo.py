# -*- coding: utf-8 -*-
"""
Created on Sat Oct 08 21:52:46 2016

@author: Sunnyin
"""

#import tushare as ts
import numpy as np
import talib as ta
import matplotlib.mlab as mlab
import os,datetime,operator




def get_case_data(sorted_data):
    close = sorted_data.close
    high = sorted_data.high
    low = sorted_data.low
    ma5 = sorted_data.ma5
    ma10 = sorted_data.ma10
    ma20 = sorted_data.ma20
    return (close,high,low,ma5,ma10,ma20)
#通过MACD指标来判别购买与否，分别为DIFF,DEA,DIFF-DEA
def get_macd(sorted_data):
    close,high,low,ma5,ma10,ma20 = get_case_data(sorted_data)
    macd, macdsignal, macdhist = ta.MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)
    SignalMA5 = ta.MA(macdsignal, timeperiod=5, matype=0)
    SignalMA10 = ta.MA(macdsignal, timeperiod=10, matype=0)
    SignalMA20 = ta.MA(macdsignal, timeperiod=20, matype=0)
    #2个数组 1.DIFF、DEA均为正，DIFF向上突破DEA，买入信号。 2.DIFF、DEA均为负，DIFF向下跌破DEA，卖出信号。
    operator = 0
    if macd[-1] > 0:
        if macdsignal[-1] > 0:
            if macd[-1] > macdsignal[-1] and macd[-2] <= macdsignal[-2]:
                operator += 10  #买入
                
    else:
        if macdsignal[-1] < 0:
            if macd[-1] <= macdsignal[-2]:
                operator -= 10
        
    #DEA线与k线发生背离，行情反转信号
    if ma5[-1] >= ma10[-1] and ma10[-1] >= ma20[-1]:  #k线上升
        if SignalMA5[-1] <= SignalMA10[-1] and SignalMA10[-1] <= SignalMA20[-1]:  #DEA下降
            operator -= 1
    if ma5[-1] <= ma10[-1] and ma10[-1] <= ma20[-1]:  #k线下降
        if SignalMA5[-1] >= SignalMA10[-1] and SignalMA10[-1] >= SignalMA20[-1]:  #DEA上升
            operator += 1
            
    #分析MACD柱状图，由负变正，则买入信号
    if macdhist[-1] > 0:
        for i in range(1,7):
            if macdhist[-2] <= 0:
                operator += 5
                break
    if macdhist[-1] < 0:
        for i in range(1,7):
            if macdhist[-2] >= 0:
                operator -= 5
                break
    return (operator)
    
#通过KDJ指标来判别购买与否
def get_kdj(sorted_data):
    close,high,low,ma5,ma10,ma20 = get_case_data(sorted_data)
    slowk, slowd = ta.STOCH(high,low,close, fastk_period=9, slowk_period=3, slowk_matype=0, slowd_period=3, slowd_matype=0)
    slowkMA5 = ta.MA(slowk, timeperiod=5, matype=0)
    slowkMA10 = ta.MA(slowk, timeperiod=10, matype=0)
    slowkMA20 = ta.MA(slowk, timeperiod=20, matype=0)
    slowdMA5 = ta.MA(slowd, timeperiod=5, matype=0)
    slowdMA10 = ta.MA(slowd, timeperiod=10, matype=0)
    slowdMA20 = ta.MA(slowd, timeperiod=20, matype=0)
    operator = 0
    
    #1.K线是快速确认线——数值在90以上为超买，数值在10以下为超卖；D大于80时，行情呈现超买现象。D小于20时，行情呈现超卖现象。
    if slowk[-1] >= 90:
        operator += 3
    elif slowk[-1] <= 10:
        operator -= 3
    
    if slowd[-1] >=80:
        operator += 3
    elif slowd[-1] <= 20:
        operator -= 3

     #2.上涨趋势中，K值大于D值，K线向上突破D线时，为买进信号
    if slowk[-1] > slowd[-1] and slowk[-2] <= slowd[-2]:
        operator += 10
    elif slowk[-1] < slowd[-1] and slowk[-2] >= slowd[-2]:
        operator -= 10
        
     #3.当随机指标与股价出现背离时，一般为转势的信号。
    if ma5[-1] >= ma10[-1] and ma10[-1] >= ma20[-1]:  #k线上升
        if (slowkMA5[-1] <= slowkMA10[-1] and slowkMA10[-1] <= slowkMA20[-1]) or (slowdMA5[-1] <= slowdMA10[-1] and slowdMA10[-1] <= slowdMA20[-1]):
            operator -= 1
    elif ma5[-1] <= ma10[-1] and ma10[-1] <= ma20[-1]:  #k线下降
        if (slowkMA5[-1] >= slowkMA10[-1] and slowkMA10[-1] >= slowkMA20[-1]) or (slowdMA5[-1] >= slowdMA10[-1] and slowdMA10[-1] >= slowdMA20[-1]):
            operator += 1
    return operator

path = 'E:\\big_data\\TheRoadOfPython2016\\anocondaLearningSpace\\data_base'
os.chdir(path)
for root,dirs,files in os.walk(path):
    fileNames = files

#100 stocks were randomly selected.
fileNum = np.random.random_integers(2897,size = 100)
useFiles = []
for i in fileNum:
    useFiles.append(fileNames[i])

for fname in useFiles:
    r = mlab.csv2rec(fname)
    if len(r) > 60:
        macd_score = get_macd(r)
        kdj_score = get_kdj(r)
        sotck_name = fname.split('.')
        print("the stock "+ sotck_name + " macd score is :" + str(macd_score))
        print("the stock "+ sotck_name + " kdj score is :" + str(kdj_score))
    else:
        continue

#stockFname = []
#for stock in stocksList:
#    data = ts.get_hist_data(stock[1]).sort_index()
#    stockFname.append(stock[0]+end+'.csv')
#    
#    macd_score = get_macd(data)
#    kdj_score = get_kdj(data)
#    print("the stock "+ stock[0] + " macd score is :" + str(macd_score))
#    print("the stock "+ stock[0] + " kdj score is :" + str(kdj_score))

#    upperband, middleband, lowerband = ta.BBANDS(close, timeperiod=5, nbdevup=2, nbdevdn=2, matype=0)
#    t = range(len(close))


