%%writefile test.py

# Core Pkgs
import streamlit as st
import os
from PIL import Image 
import warnings
warnings.filterwarnings("ignore")

#Visualization
import matplotlib.pyplot as plt 
import matplotlib
matplotlib.use("Agg")
import seaborn as sns

#from dataset_milestone1 import datasets: Add all the different diseases 
import pandas as pd
# Load the CSV file into a pandas dataframe
print(os.listdir("./"))
smartparking =pd.read_excel('./dataset/parking.xlsx')


## ======================================== Reusable Function Space ===========================
def welcome():
    hello = st.title("👋 Welcome to Smart Parking Manamgement App v1.0")
    #Starting from the top
    st.markdown("# Dedicated for Smart City Management Framework™")
    st.markdown("Project realized by: Naga Srinivas Reddy & Naga Siva Reddy & Shravan Yadav")
    original_title = '<p style="color:Orange; font-size: 30px;">/p>'
    st.markdown(original_title, unsafe_allow_html=True)
    return hello

def load_dataset(nrow):
    data = pd.read_excel('./dataset/parking.xlsx')
    return data.head(nrow)

def cleaningdata(df):
    
    return 200
    
## ======================================== Streamlit App Space ===============================

def app():
    ## Showing greeting
    welcome()
    
    ## Showcasing raw data 
    st.subheader("📊 Step I: Raw Data")
    # Create a text element and let the reader know the data is loading.
    data_load_state = st.text('Loading data...')
    # Load 10,000 rows of data into the dataframe.
    data = load_dataset(10)
    # Notify the reader that the data was successfully loaded.
    data_load_state.text('Loading data...done!')
    st.write(data)
    
    ## Showcasing raw data 
    st.subheader("📈 Step II: EDA Process & Visualization")
    
    return 200


## ======================================== Launching the app: =================================
if __name__ == "__main___":
    app()
