import streamlit as st
import pandas as pd
import io
from lazypredict.Supervised import LazyRegressor
from sklearn.ensemble import RandomForestRegressor
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.datasets import load_diabetes, load_boston
from sklearn.model_selection import train_test_split
import base64

st.write("""
# The Machine Learning Algorithm Comparison App
In this implementation, the **Lazypredict** library is used for building several machine learning models at once.
""")


# Sidebar - Collects user input features into dataframe
with st.sidebar.header('1. Upload your CSV data'):
    uploaded_file = st.sidebar.file_uploader("Upload your input CSV file", type=["csv"])
    
# Sidebar - Specify parameter settings
with st.sidebar.header('2. Set Parameters'):
    split_size = st.sidebar.slider('Data split ratio (% for Training Set)', 10, 90, 70)
    seed_number = st.sidebar.slider('Set the random seed number', 1, 100, 40)

# Displays the dataset
st.subheader('1. Dataset')


# Download CSV data
def filedownload(df, filename):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download={filename}>Download {filename} File</a>'
    return href

def imagedownload(plt, filename):
    s = io.BytesIO()
    plt.savefig(s, format='pdf', bbox_inches='tight')
    plt.close()
    b64 = base64.b64encode(s.getvalue()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:image/png;base64,{b64}" download={filename}>Download {filename} File</a>'
    return href


def build_model(df):

   
    X = df.iloc[:,:-1] #  all column except for the last column 
    Y = df.iloc[:,-1] #  last column 
    st.subheader('1. Dataset Description')
    st.markdown('**Dataset dimensions**')
    st.write('X')
    st.info(X.shape)
    st.write('Y')
    st.info(Y.shape)

    st.markdown('**Variable details**:')
    st.write('X variables')
    st.info(list(X.columns))
    st.write('Y variable')
    st.info(Y.name)

    # Building lazy model
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y,test_size = split_size,random_state = seed_number)
    reg = LazyRegressor(verbose=0,ignore_warnings=False, custom_metric=None)
    models_train,predictions_train = reg.fit(X_train, X_train, Y_train, Y_train)
    models_test,predictions_test = reg.fit(X_train, X_test, Y_train, Y_test)




    st.subheader('2. Table of Model Performance')
    st.write('Training set')
    st.write(predictions_train)
    st.markdown(filedownload(predictions_train,'training.csv'), unsafe_allow_html=True)

    st.write('Test set')
    st.write(predictions_test)
    st.markdown(filedownload(predictions_test,'test.csv'), unsafe_allow_html=True)


    st.subheader('3. Plot for Model Performance (Test set)')
    with st.markdown('**Calculation time**'):
        # portrait
        predictions_test["Time Taken"] = [0 if i < 0 else i for i in predictions_test["Time Taken"] ]
        plt.figure(figsize=(3, 9))
        sns.set_theme(style="whitegrid")
        ax3 = sns.barplot(y=predictions_test.index, x="Time Taken", data=predictions_test)
    st.markdown(imagedownload(plt,'plot-calculation-time-portrait.pdf'), unsafe_allow_html=True)
    
    # landscape
    plt.figure(figsize=(9, 3))
    sns.set_theme(style="whitegrid")
    ax3 = sns.barplot(x=predictions_test.index, y="Time Taken", data=predictions_test)
    plt.xticks(rotation=90)
    st.pyplot(plt)
    st.markdown(imagedownload(plt,'plot-calculation-time-landscape.pdf'), unsafe_allow_html=True)

    with st.markdown('**R-squared**'):
        # portrait
        predictions_test["R-Squared"] = [0 if i < 0 else i for i in predictions_test["R-Squared"] ]
        plt.figure(figsize=(3, 9))
        sns.set_theme(style="whitegrid")
        ax1 = sns.barplot(y=predictions_test.index, x="R-Squared", data=predictions_test)
        ax1.set(xlim=(0, 1))
    st.markdown(imagedownload(plt,'plot-r2-portrait.pdf'), unsafe_allow_html=True)
        # landscape
    plt.figure(figsize=(9, 3))
    sns.set_theme(style="whitegrid")
    ax1 = sns.barplot(x=predictions_test.index, y="R-Squared", data=predictions_test)
    ax1.set(ylim=(0, 1))
    plt.xticks(rotation=90)
    st.pyplot(plt)
    st.markdown(imagedownload(plt,'plot-r2-landscape.pdf'), unsafe_allow_html=True)


    with st.markdown('**RMSE (capped at 50)**'):
        # protrait view 
        predictions_test["RMSE"] = [50 if i > 50 else i for i in predictions_test["RMSE"] ]
        plt.figure(figsize=(3, 9))
        sns.set_theme(style="whitegrid")
        ax2 = sns.barplot(y=predictions_test.index, x="RMSE", data=predictions_test)
    st.markdown(imagedownload(plt,'plot-rmse-portrait.pdf'), unsafe_allow_html=True)
        # Landscape View
    plt.figure(figsize=(9, 3))
    sns.set_theme(style="whitegrid")
    ax2 = sns.barplot(x=predictions_test.index, y="RMSE", data=predictions_test)
    plt.xticks(rotation=90)
    st.pyplot(plt)
    st.markdown(imagedownload(plt,'plot-rmse-landscape.pdf'), unsafe_allow_html=True)

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.markdown('**Preview of dataset**')
    st.write(df)
    build_model(df)
else:
    st.info('Awaiting for CSV file to be uploaded.')
    if st.button('Use Example Dataset'):
        # Diabetes dataset
        
        #diabetes = load_diabetes()
        #X = pd.DataFrame(diabetes.data, columns=diabetes.feature_names)
        #Y = pd.Series(diabetes.target, name='response')
        #df = pd.concat( [X,Y], axis=1 )

        #st.markdown('The Diabetes dataset is used as the example.')
        #st.write(df.head(5))

        # Boston housing dataset
        boston = load_boston()
        
        X = pd.DataFrame(boston.data, columns=boston.feature_names) 
        Y = pd.Series(boston.target, name='response') 
        df = pd.concat( [X,Y], axis=1 )

        st.markdown('The Boston housing dataset is used as the example.')
        st.write(df.head(7))

        build_model(df)





# Inspired and taught by DataProfessor