# Importing All required libraries
import streamlit as st
import numpy as np
import pandas as pd
from sklearn import datasets
from sklearn.ensemble import RandomForestClassifier

# Providing header and text to the app
st.write('''
    # Simple Iris Flower Prediction App

    This app predicts the iris flower type

''')
# Header for input display
st.sidebar.header('User Input Parameters')


def user_input():
    sepal_length = st.sidebar.slider('sepal_length', 4.3, 7.9, 5.4)
    sepal_width = st.sidebar.slider('sepal_width', 2.0, 4.4, 3.4)
    petal_length = st.sidebar.slider('petal_length', 1.0, 6.9, 1.3)
    petal_width = st.sidebar.slider('petal_width', 0.1, 2.5, 0.2)

    data = {
        'sepal_length': sepal_length,
        'sepal_width': sepal_width,
        'petal_length': petal_length,
        'petal_width': petal_width,
    }


    features = pd.DataFrame(data,index=[0])

    return features

df = user_input()

st.subheader('User Input Parameters')
st.write(df)

iris = datasets.load_iris()
X = iris.data
y = iris.target

classifier = RandomForestClassifier()
classifier.fit(X,y)

prediction  = classifier.predict(df)
prediction_prob = classifier.predict_proba(df)  

# Shows all Available targets 
st.subheader('Class labels and their corresponding index numbers')
st.write(iris.target_names)

# Provides the prediction
st.subheader('Prediction')
st.write(iris.target_names[prediction])

#Probablity of being in one of the three classes
st.subheader('Prediction Probablity')
st.write(prediction_prob)





