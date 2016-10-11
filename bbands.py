# -*- coding: utf-8 -*-
"""
Created on Thu Sep 29 14:25:18 2016

@author: Sunnyin
"""

#import numpy as np
import talib as tl
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import numpy as np
import matplotlib.ticker as ticker
import os

os.chdir("E:\\PythonWorkSpace\\data\\data\\data")
r = mlab.csv2rec("603369.csv")
r.sort()
r = r[-40:]
close = r.close
upperband, middleband, lowerband = tl.BBANDS(close, timeperiod=5, nbdevup=2, nbdevdn=2, matype=0)
t = range(len(close))
macd, macdsignal, macdhist = tl.MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)
#fig,ax = plt.subplots()
#ax.plot(r.date,r.close,'o-')
#fig.autofmt_xdate()
N = len(r)
ind = np.arange(N)  # the evenly spaced plot indices
#plt.grid()
#plt.plot(t,upperband,lw=2.0)
#plt.plot(t,lowerband,lw=2.0)
#plt.plot(t,middleband,lw=1.5)
#plt.plot(t,close,lw=1.0)
#plt.show()

def format_date(x, pos=None):
    thisind = np.clip(int(x + 0.5), 0, N - 1)
    return r.date[thisind].strftime('%Y-%m-%d')

fig, ax = plt.subplots()
ax.grid(True)
ax.plot(ind, close, '.-',)
ax.plot(ind,lowerband,'.--')
ax.plot(ind,upperband,'.--')
ax.plot(ind,middleband,'^-')
ax.xaxis.set_major_formatter(ticker.FuncFormatter(format_date))
fig.autofmt_xdate()

plt.show()
