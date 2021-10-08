# -*- coding: utf-8 -*-
"""Diabetes Detection

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1REXOfPSgpzSV18H_Prr3JTUMODEby7mn
"""

import numpy as np
import pandas as pd
import pickle

df = pd.read_csv('diabetes.csv')

df.head()

df = df.rename(columns={'DiabetesPedigreeFunction' : 'DPF'})

df

df_copy = df.copy(deep=True)

df_copy['Glucose'] = df_copy['Glucose'].replace(0,np.NaN)
df_copy['BloodPressure'] = df_copy['BloodPressure'].replace(0,np.NaN)
df_copy['SkinThickness'] = df_copy['SkinThickness'].replace(0,np.NaN)
df_copy['Insulin'] = df_copy['Insulin'].replace(0,np.NaN)
df_copy['BMI'] = df_copy['BMI'].replace(0,np.NaN)

df_copy.head()

df_copy.isnull().sum()

df_copy['Glucose'].fillna(df_copy['Glucose'].mean(),inplace=True)
df_copy['BloodPressure'].fillna(df_copy['BloodPressure'].mean(),inplace=True)
df_copy['SkinThickness'].fillna(df_copy['SkinThickness'].mean(),inplace=True)
df_copy['Insulin'].fillna(df_copy['Insulin'].median(),inplace=True)
df_copy['BMI'].fillna(df_copy['BMI'].median(),inplace=True)

df_copy.isnull().sum()

from sklearn.model_selection import train_test_split

X = df_copy.drop(columns='Outcome')
y = df_copy['Outcome']

X.head()

X_train,X_test,y_train,y_test = train_test_split(X,y,test_size = 0.20,random_state = 42)

from sklearn.ensemble import RandomForestClassifier

clf = RandomForestClassifier()

clf.fit(X_train,y_train)

pred = clf.predict(X_test)

from sklearn.metrics import accuracy_score,confusion_matrix

accuracy_score(y_test,pred)

confusion_matrix(y_test,pred)

filename = 'finalized_model.pkl'
pickle.dump(clf, open(filename, 'wb'))

