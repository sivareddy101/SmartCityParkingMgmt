##Required Libraries
import streamlit as st 
import numpy as np # linear algebra #rgb values for images exist in a np array
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import os
import matplotlib.pyplot as plt
from matplotlib.image import imread


## ignore warnings 
import warnings
warnings.filterwarnings("ignore")


## ======================================== Reusable Function Space ===========================
st.title("👋 Welcome to Smart Parking Manamgement App v1.0")
#Starting from the top
st.markdown("# Dedicated for Smart City Management Framework™")
st.markdown("Project realized by: Naga Srinivas Reddy & Naga Siva Reddy & Shravan Yadav")

  
  
original_title = '<p style="color:Orange; font-size: 30px;"> Let get started...</p>'
st.markdown(original_title, unsafe_allow_html=True)

## ======================================== Streamlit App Space ===============================

## Showcasing raw data 
st.subheader("📊 Step I: Raw Data")
# Create a text element and let the reader know the data is loading.
data_load_state = st.text('Loading data...')
# Load 10,000 rows of data into the dataframe.
dataset = pd.read_excel('./dataset/parking.xlsx')
# Notify the reader that the data was successfully loaded.
data_load_state.text('Loading data...done!')
st.write(dataset.head(10))
    
## Showcasing stats 
st.subheader("📈 Step II: Data Stats")
st.write(dataset.describe())

## Cleaning data 
st.subheader("🧼 Step III: Cleaning the dataset")
st.info("At this step, we are about to clean the dataset...")
st.warning("Here are some facts about the dataset:")
st.info('Number of rows')
st.success(dataset.shape[0])
st.info('Number of columns')
st.success(dataset.shape[1])
# Find the missing values in the dataset
missing_values = dataset.isna().sum()
st.warning("Here are the missing values:", icon="⚠️")
st.error(missing_values)
columns_list = dataset.columns
# Drop the "occupant_changed" column from the dataset
dataset = dataset.drop(columns=['occupant_changed'])

## Visualizing data 
st.subheader("📉 Step IV: EDA Process- Visualizing the dataset")

# Group the data by weather condition and compute the average occupancy for each group
occupancy_by_weather = dataset.groupby('weather')['occupancy'].mean()

# Create a bar chart to visualize the results
plt.bar(occupancy_by_weather.index, occupancy_by_weather.values)
# Set the chart title and axis labels
plt.title('Average Vehicle Occupancy by Weather Condition')
plt.xlabel('Weather Condition')
plt.ylabel('Average Occupancy')
# Display the chart
st.write("Group the data by weather condition and compute the average occupancy for each group")
st.pyplot(plt.show())

