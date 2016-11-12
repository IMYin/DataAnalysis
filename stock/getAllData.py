# -*- coding: utf-8 -*-
"""
Created on Sat Oct 08 22:59:02 2016

@author: Sunnyin
"""

#get all of stocks data

import tushare as ts
import os

path = '/home/sunnyin/myProject/data/stock'
os.chdir(path)
x = 0
stock_basics = ts.get_stock_basics()
for code in stock_basics.index:
    try:
        ts.get_hist_data(code,retry_count=10).to_csv(code +'.csv')
        print("got the " + str(x) + " data...")
        x += 1
    except Exception as e:
        print(e.message)
print(str(x) + ' stocks completed..')
    
