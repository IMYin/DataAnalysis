# -*- coding: utf-8 -*-
"""
Created on Mon Oct 10 21:47:39 2016

@author: Sunnyin
"""

#update data of the stocks

import tushare as ts
import datetime


data_dir = 'E:\\big_data\\TheRoadOfPython2016\\anocondaLearningSpace\\data_case\\'
stock_basics = ts.get_stock_basics()

today = datetime.date.today()
ISOFORMAT = '%Y-%m-%d'
start = today.strftime(ISOFORMAT)

for code in stock_basics.index:
    ts.get_hist_data(code,start=today).to_csv(code +'.csv',mode='a+')