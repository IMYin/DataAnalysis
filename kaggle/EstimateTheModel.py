#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on  11/15/16 10:48 PM

@author: IMYin

@File: EstimateTheModel.py
"""

import pandas as pd
import numpy as np

from sklearn.ensemble import RandomForestClassifier,RandomForestRegressor
from sklearn.grid_search import GridSearchCV
from sklearn.cross_validation import  train_test_split
from sklearn.metrics import classification_report
from sklearn.pipeline import Pipeline
import sklearn.preprocessing as preprocessing

import os,datetime


def set_missing_ages(df):
    age_df = df[['Age', 'Fare', 'Parch', 'SibSp', 'Pclass']]
    known_age = age_df[age_df.Age.notnull()].as_matrix()
    unknown_age = age_df[age_df.Age.isnull()].as_matrix()

    y = known_age[:, 0]
    X = known_age[:, 1:]

    # fit by RamdomForestRegressor
    rfr = RandomForestRegressor(random_state=0, n_estimators=2000, n_jobs=-1)
    rfr.fit(X, y)

    # predict the unknown age
    predictedAges = rfr.predict(unknown_age[:, 1:])
    # backfill the value of unknown age
    df.loc[(df.Age.isnull()), 'Age'] = predictedAges

    return df, rfr



os.chdir("/home/sunnyin/kaggle/data/Titanic")

#read the data

data_train = pd.read_csv('train.csv')
data_train,rfr = set_missing_ages(data_train)
dummies_Embarked = pd.get_dummies(data_train['Embarked'],prefix='Embarked')
dummies_Sex = pd.get_dummies(data_train['Sex'],prefix='Sex')
dummies_Pclass = pd.get_dummies(data_train['Pclass'],prefix='Pclass')

df = pd.concat([data_train,dummies_Embarked,dummies_Pclass,dummies_Sex],axis=1)
df.drop(['Pclass','Name','Cabin','Sex','Ticket','Embarked'],axis=1,inplace=True)

scaler = preprocessing.StandardScaler()
age_scale_param = scaler.fit(df['Age'].reshape(-1,1))
df['Age_scaled'] = scaler.fit_transform(df['Age'].reshape(-1,1),age_scale_param)

fare_scale_param = scaler.fit(df['Fare'].reshape(-1,1))
df['Fare_scaled'] = scaler.fit_transform(df['Fare'].reshape(-1,1),fare_scale_param)

train_df = df.filter(regex='Survived|Age_.*|SibSp|Parch|Fare_.*|Embarked_.*|Sex_.*|Pclass_.*')
train_np = train_df.as_matrix()

y = train_np[:,0]
X = train_np[:,1:]

# split the data
X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2)
pipeline = Pipeline([('clf',RandomForestClassifier())])

parameters = {
    'clf__n_estimators': (200,150 , 130, 100),
    'clf__max_depth': (130, 150, 180),
    'clf__min_samples_split': (1, 2, 3),
    'clf__min_samples_leaf': (1, 2, 3),
    'clf__criterion'  :  ('gini','entropy')
}
grid_search = GridSearchCV(pipeline, parameters, n_jobs=-1, verbose=1, scoring='f1')
grid_search.fit(X_train, y_train)
print('best score: %0.3f' % grid_search.best_score_)
print('Best parameters set:')
best_parameters = grid_search.best_estimator_.get_params()
for param_name in sorted(parameters.keys()):
    print "\t%s: %r" % (param_name, best_parameters[param_name])

predictions = grid_search.predict(X_test)
print(classification_report(y_test, predictions))
