##Required Libraries
import streamlit as st 
import numpy as np # linear algebra #rgb values for images exist in a np array
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import os
import matplotlib.pyplot as plt
from matplotlib.image import imread
import holidays

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
st.set_option('deprecation.showPyplotGlobalUse', False)
st.pyplot(plt.show())

st.write('''
Assuming you have read in the dataset and created a DataFrame called dataset. 
Assuming you have read in the dataset and created a DataFrame called dataset
- We first shouldd efine the holidays for your country and then create a new column in the dataset to indicate whether the date is a holiday or not
- Also we should create a subset of the dataset that only includes data from holidays
- and finally # Group the data by date and calculate the mean occupancy for each holiday.
''')
st.info("The following is a plot of the occupancy for each holiday using a bar chart ")
# Assuming you have read in the dataset and created a DataFrame called dataset
dataset['datetime'] = pd.to_datetime(dataset['datetime'], format='%Y-%m-%d_%H.%M')



# Assuming you have read in the dataset and created a DataFrame called dataset
# Define the holidays for your country
us_holidays = holidays.US()
# Create a new column in the dataset to indicate whether the date is a holiday or not
dataset['holiday'] = dataset['datetime'].apply(lambda x: x in us_holidays)
# Create a subset of the dataset that only includes data from holidays
holiday_dataset = dataset[dataset['holiday']]
# Group the data by date and calculate the mean occupancy for each holiday
holiday_occupancy = holiday_dataset.groupby('datetime')['occupancy'].mean()
# Plot the occupancy for each holiday using a bar chart
plt.bar(holiday_occupancy.index, holiday_occupancy)
plt.title('Average Occupancy during Holidays')
plt.xlabel('Holiday Date')
plt.ylabel('Average Occupancy')
plt.xticks(rotation=45)
st.pyplot(plt.show())


st.info("The following is the  mean occupancy for holidays and non-holidays using a bar chart")
mean_holiday_occupancy = dataset[dataset['holiday'] == True]['occupancy'].mean()
mean_non_holiday_occupancy = dataset[dataset['holiday'] == False]['occupancy'].mean()
# Plot the data
fig, ax = plt.subplots()
ax.bar(['Holiday', 'Non-Holiday'], [mean_holiday_occupancy, mean_non_holiday_occupancy])
ax.set_ylabel('Mean Occupancy')
ax.set_title('Mean Occupancy for Holidays and Non-Holidays')
st.pyplot(plt.show())

st.write('''
Here we are converting the datatime column into the datatime data type column and also we are grouping 
-the data by the day of the week and calculating the mean occupency
''')
st.info("The following is the mean occupency by the day of week by using the bar chart")
dataset['datetime'] = pd.to_datetime(dataset['datetime'])


mean_occupancy_by_day = dataset.groupby(dataset['datetime'].dt.day_name())['occupancy'].mean()

# Plot the data
fig, ax = plt.subplots()
mean_occupancy_by_day.plot(kind='bar', ax=ax)
ax.set_xlabel('Day of Week')
ax.set_ylabel('Mean Occupancy')
ax.set_title('Mean Occupancy by Day of Week')
st.pyplot(plt.show())

st.write('''
Here in this we are grouping the data by day and count the number of entries for each day and 
-finding the day with the highest number of entries form the dataset
''')
st.info("The following is the presenting the busiest day of the month from the data set by using the line chart")
entries_by_day = dataset.groupby('day')['camera'].count()

# Create a line chart to visualize the results
plt.plot(entries_by_day.index, entries_by_day.values)

# Set the chart title and axis labels
plt.title('Number of Entries by Day')
plt.xlabel('Day')
plt.ylabel('Number of Entries')
st.pyplot(plt.show())

st.write('''
Here we are grouping the data by date and time and compute the total occupancy for each group
-for finding the date and time with the highest total occupency form the dataset
''')
st.info("The following we are predicting the busiest date and time from the dataset")
occupancy_by_date_time = dataset.groupby(['day', 'month', 'year', 'hour'])['occupancy'].sum()
busiest_date_time = occupancy_by_date_time.idxmax()
st.write("The busiest day and time is: {}-{}-{} {}:00".format(busiest_date_time[0], busiest_date_time[1], busiest_date_time[2], busiest_date_time[3]))

st.write('''
Here we are convering the datatime column to  a pandas datetime format and also Grouping  the 
-data by week and count the number of records in each group for predecting the occupency for each week
''')
st.info("The following we are predicting occupency for each and every week from the whole dataset")
dataset['datetime'] = pd.to_datetime(dataset['datetime'], format='%Y-%m-%d_%H.%M')
# Convert the 'datetime' column to a pandas datetime format
dataset['datetime'] = pd.to_datetime(dataset['datetime'])

# Group the data by week and count the number of records in each group
parked_by_week = dataset.groupby(pd.Grouper(key='datetime', freq='W'))['occupancy'].count()

# Print the results
st.write(parked_by_week)























