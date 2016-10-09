# -*- coding: utf-8 -*-
"""
Created on Sat Oct 08 22:59:02 2016

@author: Sunnyin
"""

#get all of stocks data

import tushare as ts
import os

os.chdir('E:\\big_data\\TheRoadOfPython2016\\anocondaLearningSpace\\stocksData')
allData = ts.get_today_all()
code = allData.code.values
for stock in code:
    ts.get_hist_data(stock).to_csv(stock +'.csv')