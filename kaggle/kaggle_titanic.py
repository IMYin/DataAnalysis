# -*- coding: utf-8 -*-
"""
Created on Thu Nov 10 15:52:01 2016

@author: IMYin
"""

import os, datetime

import numpy as np
import pandas as pd
import sklearn.preprocessing as preprocessing
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier


# processing the bad value
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


# processing the column : Cabin
def set_Cabin_type(df):
    df.loc[(df.Cabin.isnull()), 'Cabin'] = 'Yes'
    df.loc[(df.Cabin.notnull()), 'Cabin'] = 'No'

    return df


t0 = datetime.datetime.now()
os.chdir('/home/sunnyin/kaggle/data/Titanic')
data_train = pd.read_csv('train.csv')
data_train, rfr = set_missing_ages(data_train)
data_train = set_Cabin_type(data_train)

dummies_Cabin = pd.get_dummies(data_train['Cabin'], prefix='Cabin')
dummies_Embarked = pd.get_dummies(data_train['Embarked'], prefix='Embarked')
dummies_Sex = pd.get_dummies(data_train['Sex'], prefix='Sex')
dummies_Pclass = pd.get_dummies(data_train['Pclass'], prefix='Pclass')

# merging data
df = pd.concat([data_train, dummies_Cabin, dummies_Embarked, dummies_Pclass, dummies_Sex], axis=1)
df.drop(['Pclass', 'Name', 'Cabin', 'Sex', 'Ticket', 'Embarked'], axis=1, inplace=True)

scaler = preprocessing.StandardScaler()
age_scale_param = scaler.fit(df['Age'].reshape(-1, 1))
df['Age_scaled'] = scaler.fit_transform(df['Age'].reshape(-1, 1), age_scale_param)

fare_scale_param = scaler.fit(df['Fare'].reshape(-1, 1))
df['Fare_scaled'] = scaler.fit_transform(df['Fare'].reshape(-1, 1), fare_scale_param)

train_df = df.filter(regex='Survived|Age_.*|SibSp|Parch|Cabin_.*|Fare_.*|Embarked_.*|Sex_.*|Pclass_.*')
train_np = train_df.as_matrix()

y = train_np[:, 0]
X = train_np[:, 1:]
rfc = RandomForestClassifier(n_estimators=130, n_jobs=-1, criterion='entropy', max_depth=18, min_samples_leaf=1,
                             min_samples_split=3)
rfc.fit(X, y)
# clf = LogisticRegression()
# clf.fit(X,y)
# ------------------------------------------------

data_test = pd.read_csv('test.csv')
data_test.loc[(data_test.Fare.isnull()), 'Fare'] = 0
tmp_df = data_test[['Age', 'Fare', 'Parch', 'SibSp', 'Pclass']]
null_age = tmp_df[data_test.Age.isnull()].as_matrix()
X = null_age[:, 1:]
predictedAges = rfr.predict(X)
data_test.loc[(data_test.Age.isnull()), 'Age'] = predictedAges

data_test = set_Cabin_type(data_test)

dummies_Cabin = pd.get_dummies(data_test['Cabin'], prefix='Cabin')
dummies_Embarked = pd.get_dummies(data_test['Embarked'], prefix='Embarked')
dummies_Sex = pd.get_dummies(data_test['Sex'], prefix='Sex')
dummies_Pclass = pd.get_dummies(data_test['Pclass'], prefix='Pclass')

# merging data
df_test = pd.concat([data_test, dummies_Cabin, dummies_Embarked, dummies_Pclass, dummies_Sex], axis=1)
df_test.drop(['Pclass', 'Name', 'Cabin', 'Sex', 'Ticket', 'Embarked'], axis=1, inplace=True)

df_test['Age_scaled'] = scaler.fit_transform(df_test['Age'].reshape(-1, 1), age_scale_param)
df_test['Fare_scaled'] = scaler.fit_transform(df_test['Fare'].reshape(-1, 1), fare_scale_param)

test = df_test.filter(regex='Age_.*|SibSp|Parch|Cabin_.*|Fare_.*|Embarked_.*|Sex_.*|Pclass_.*')

# predict the result
predictions = rfc.predict(test)
# predictions = clf.predict(test)

result = pd.DataFrame({'PassengerId': data_test['PassengerId'], 'Survived': predictions.astype(np.int32)})
result.to_csv('/home/sunnyin/kaggle/results/rfc_grid_search.csv', index=False)

t1 = datetime.datetime.now()
times = (t1 - t0).total_seconds()

print("dt:{} sec".format(times))
