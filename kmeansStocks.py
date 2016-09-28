
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 28 09:36:29 2016

@author: Sunnyin
"""

import numpy as np
import pandas as pd
from scipy.cluster.vq import kmeans,vq
import os,copy

os.chdir('E:\\PythonWorkSpace\\data\\data\\data')
path = 'E:\\PythonWorkSpace\\data\\data\\data'

for root,dirs,files in os.walk(path):
    fileNames = files
    
fileNum = np.random.random_integers(2890,size = 100)
useFiles = []
for i in fileNum:
    useFiles.append(fileNames[i])
    
stocks = []
change = []
useFileTrue = copy.deepcopy(useFiles)
stocksName = {}
for index in range(len(useFiles)):
    info = pd.read_csv(useFiles[index])
    if len(info) > 101:
        stocks.append(info.close.values[:100])
    else:
        useFileTrue.pop(index)

print("Now,we will analysis "+ str(len(stocks))+ " stocks data...")
for _ in range(len(stocks)):
    change.append(np.sign(np.diff(stocks[_])))
    
data = np.vstack(change)
centroids,_= kmeans(data,5)
result,_ = vq(data,centroids)

for num in range(len(result)):
    stocksName[useFileTrue[num]] = result[num]
print(stocksName)
