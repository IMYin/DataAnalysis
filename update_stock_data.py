# -*- coding: utf-8 -*-
"""
Created on Mon Oct 10 21:47:39 2016

@author: Sunnyin
"""

#update data of the stocks

import tushare as ts
import datetime,os


path = 'E:\\big_data\\TheRoadOfPython2016\\anocondaLearningSpace\\data_case\\'
os.chdir(path)
#initial date
today = datetime.date.today()
ISOFORMAT = '%Y-%m-%d'
start = today.strftime(ISOFORMAT)

for root,dirs,files in os.walk(path):
    fileNames = files
    
for name in fileNames:
    ts.get_hist_data(name.split('.')[0],start=today).to_csv(name,mode='a+')
