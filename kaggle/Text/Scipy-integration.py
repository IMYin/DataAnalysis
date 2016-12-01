#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on  11/29/16 9:58 PM

@author: IMYin

@File: Scipy-integration.py
"""

import numpy as np
from scipy.integrate import quad, trapz

# Setting up fake data
x = np.sort(np.random.randn(150) * 4 + 4).clip(0, 5)
func = lambda x: np.sin(x) * np.cos(x ** 2) + 1
y = func(x)

# Integrating function with upper and lower
# limits of 0 and 5, respectively
fsolution = quad(func, 0, 5)

dsolution = trapz(y, x=x)

print('dsolution = ' + str(dsolution))
