# -*- coding: utf-8 -*-
"""
Created on Sat Oct 08 22:59:02 2016

@author: Sunnyin
"""

#get all of stocks data

import tushare as ts
import os

os.chdir('E:\\big_data\\TheRoadOfPython2016\\anocondaLearningSpace\\data_base')
x = 1
stock_basics = ts.get_stock_basics()
for code in stock_basics.index[2953:]:
    print("the code is : " + str(code))
    ts.get_hist_data(code,retry_count=10).to_csv(code +'.csv')
    print("got the " + str(x) + " data...")
    x += 1
    
    