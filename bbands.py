# -*- coding: utf-8 -*-
"""
Created on Thu Sep 29 14:25:18 2016

@author: Sunnyin
"""

#import numpy as np
import talib as tl
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import os

os.chdir("E:\\PythonWorkSpace\\data\\data\\data")
r = mlab.csv2rec("601088.csv")
r.sort()
close = r.close[-100:]
upperband, middleband, lowerband = tl.BBANDS(close, timeperiod=5, nbdevup=2, nbdevdn=2, matype=0)
t = range(len(close))

plt.grid()
plt.plot(t,upperband,lw=2.0)
plt.plot(t,lowerband,lw=2.0)
plt.plot(t,middleband,lw=1.5)
plt.plot(t,close,lw=1.0)
plt.show()
