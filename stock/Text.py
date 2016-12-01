#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on  11/29/16 10:34 PM

@author: IMYin

@File: Text.py
"""
import pandas as pd
import matplotlib.pyplot as plt

import os

os.chdir('/home/sunnyin/myProject/data/stock')
data = pd.read_csv('300175.csv')
data.sort(['date'],inplace=True)


print(data.head())

