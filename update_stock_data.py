# -*- coding: utf-8 -*-
"""
Created on Mon Oct 10 21:47:39 2016

@author: Sunnyin
"""

#update data of the stocks

import tushare as ts
import datetime,os


path = 'E:\\big_data\\TheRoadOfPython2016\\anocondaLearningSpace\\data_base\\'
os.chdir(path)
#initial date
today = datetime.date.today()
ISOFORMAT = '%Y-%m-%d'
start = today.strftime(ISOFORMAT)

for root,dirs,files in os.walk(path):
    fileNames = files

number = 0
for name in fileNames:
    stock_data = ts.get_hist_data(name.split('.')[0],start=start)
    if len(stock_data)> 0:
        stock_data.to_csv(name,mode='a+',header=False)
        number += 1
    else:
        print("This stock"+name.split('.')[0]+" is no trade today.")
print(str(number)+" stocks data update completed.")