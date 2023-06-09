##Required Libraries
import streamlit as st 
import numpy as np # linear algebra #rgb values for images exist in a np array
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import os
import matplotlib.pyplot as plt
from matplotlib.image import imread
import holidays
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix, roc_curve, precision_recall_curve, mean_squared_error, mean_absolute_error
from sklearn.tree import DecisionTreeClassifier
#from sklearn.metrics import plot_confusion_matrix
from sklearn.metrics import precision_score, recall_score














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

st.write('Here we are plotting the above data for every week occupency by line chart')
st.info("The following we are plotting the line chart for occupency for every week")
# Plot the results
parked_by_week.plot(kind='line', title='Number of Vehicles Parked per Week')
plt.xlabel('Week')
plt.ylabel('Number of Vehicles')
st.pyplot(plt.show())

##Algorithams for accuracy
st.subheader("👨🏾‍💻 Step V: Algorithams")

st.write('''
This type of mapping is useful for converting categorical data into a numerical form
-that can be more easily analyzed or used as input to machine learning algorithms
''')
st.info("Here converting categorical into numerical form for performing upcoming operations {'S': 0, 'C': 1, 'R': 2, 'O': 3}")
weather_mapping = {'S': 0, 'C': 1, 'R': 2, 'O': 3}
dataset['weather'] = dataset['weather'].map(weather_mapping)

st.write('''
Here we are Splitting the dataset into training and testing sets, and defining the features and 
-target variable creating the feature matrix and target array for the training set 
-Creating the feature matrix and target array for the testing set Training a linear regression model
-Making predictions on the testing set and evaluate the performance of the model
''')

st.info("Here we are finding the Mean Squared Error and Mean Absolute Error")
train_data, test_data = train_test_split(dataset, test_size=0.2, random_state=42)

# Define the features and target variable
features = ['day', 'hour', 'minute', 'month', 'weather','year']
target = 'occupancy'

# Create the feature matrix and target array for the training set
X_train = train_data[features]
y_train = train_data[target]

# Create the feature matrix and target array for the testing set
X_test = test_data[features]
y_test = test_data[target]

# Train a linear regression model
model = LinearRegression()
model.fit(X_train, y_train)

# Make predictions on the testing set
y_pred = model.predict(X_test)

# Evaluate the performance of the model
mse = mean_squared_error(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)

st.write('Mean Squared Error:', mse)
st.write('Mean Absolute Error:', mae)

st.write('''
-Here we are performing the Decision Tree classifieer for finding the accuracy by 
-Assuming you have split your data into training and testing sets and created X_train, y_train, X_test, y_test variables
''')

st.info("The following is the accuracy for finding the occupency using the DecisionTreeClassifier")
dt = DecisionTreeClassifier(random_state=42)
dt.fit(X_train, y_train)
y_pred = dt.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
st.write("Accuracy:", accuracy)

st.write('''
Here we are performing the RandomForest classifieer for finding the accuracy by 
-Assuming you have split your data into training and testing sets and created X_train, y_train, X_test, y_test variables
 ''')

st.info("The following is the accuracy for finding the occupency using the RandomForestClassifier")
rf = RandomForestClassifier(random_state=42)
rf.fit(X_train, y_train)
y_pred = rf.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
st.write("Accuracy:", accuracy)

st.write('''
-Here we are performing the LogisticRegression for finding the accuracy by 
-Assuming you have split your data into training and testing sets and created X_train, y_train, X_test, y_test variables
''')
st.info("The following is the accuracy for finding the occupency using the LogisticRegression")
# Assuming you have split your data into training and testing sets and created X_train, y_train, X_test, y_test variables
lr = LogisticRegression(random_state=42)  # Instantiate the logistic regression model
lr.fit(X_train, y_train)  # Fit the model on the training data
y_pred = lr.predict(X_test)  # Predict the labels for the test data
accuracy = accuracy_score(y_test, y_pred)  # Compute the accuracy score

st.write("Accuracy:", accuracy)

st.write('''
Here we are performing the GaussianNB for finding the accuracy by Assuming you have split your
-data into training and testing sets and created X_train, y_train, X_test, y_test variables
 ''')

st.info("The following is the accuracy for finding the occupency using the GaussianNB")
nb = GaussianNB()
nb.fit(X_train, y_train)

y_pred = nb.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
st.write("Accuracy:", accuracy)

st.write('''
Here we are performing the KNeighborsClassifier for finding the accuracy by Assuming you have split your
-data into training and testing sets and created X_train, y_train, X_test, y_test variables
 ''')

st.info("The following is the accuracy for finding the occupency using the KNeighborsClassifier")

knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(X_train, y_train)

y_pred = knn.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
st.write("Accuracy:", accuracy)

st.write('''
Here we are assuming that having a list of algorithm names and their corresponding accuracy scores
-Create a bar chart using the algorithm names as x-axis labels and accuracy scores as y-axis values
-Setting chart title and labels for the x- and y-axes and we are displaying the bar chart
''')
st.info("Here we are drawing the bar chart for the accuracy of the above all algorithams")
algos = ['Logistic Regression', 'Decision Tree', 'Random Forest', 'Gaussian Naive Bayes', 'K-Nearest Neighbors']
accuracy_scores = [0.66, 0.88, 0.88, 0.66, 0.87]
plt.bar(algos, accuracy_scores)
plt.title('Accuracy Scores for Different Algorithms')
plt.xlabel('Algorithm')
plt.ylabel('Accuracy')

# Display the bar chart
st.pyplot(plt.show())

##Using confusion_matrix, roc_curve, precision_recall_curve, mean_squared_error, mean_absolute_error
st.subheader("👨🏾‍💻 Step VI: PERFORMING CONFUSION MATRIX FOR DIFFERENT ALGORITHAMS")

st.write('''
Here we are performing the confusion mayrix.roc_curve,precision_recall_curve,mean_squared_error, mean_absolute_error
-by  assuming y_true and y_pred are your ground truth and predicted labels, respectively
-for a binary classification problem confusion matrix, ROC curve,Precision-Recall curve,assuming
-y_true and y_pred are your ground truth and predicted values, respectively for a regression problem
- mean squared error and mean absolute error
''')
st.info("Here we are predicting and plotting the confusion matrix,roc curve,precision recall curve,Mean Squared Error Mean Absolute Error")
 
y_true = np.array(y_test)  # Convert to numpy array
y_pred = np.array(y_pred)  # Convert to numpy array

cm = confusion_matrix(y_true, y_pred)
print("Confusion Matrix:\n", cm)
# ROC curve
fpr, tpr, thresholds = roc_curve(y_true, y_pred)
plt.plot(fpr, tpr)
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC Curve")
st.pyplot(plt.show())

# Precision-Recall curve
precision, recall, thresholds = precision_recall_curve(y_true, y_pred)
plt.plot(recall, precision)
plt.xlabel("Recall")
plt.ylabel("Precision")
plt.title("Precision-Recall Curve")
st.pyplot(plt.show())

# assuming y_true and y_pred are your ground truth and predicted values, respectively
# for a regression problem
# mean squared error
mse = mean_squared_error(y_true, y_pred)
st.write("Mean Squared Error:", mse)

# mean absolute error
mae = mean_absolute_error(y_true, y_pred)
st.write("Mean Absolute Error:", mae)


st.write('''
Here we are Assuming you have trained and evaluated a decision tree model and obtained the predicted 
-labels and true labels for Instantiate the decision tree classifier , by Fitting the model on the training data
-by Predicting the labels for the test data and computing the confusion matrix
''')
st.info("The following we are predicting and plottong a confusion matrix for predicted label and true label for the decision tree model algoritham")

clf = DecisionTreeClassifier()  # Instantiate the decision tree classifier
clf.fit(X_train, y_train)  # Fit the model on the training data
y_pred = clf.predict(X_test)  # Predict the labels for the test data
cm = confusion_matrix(y_test, y_pred)  # Compute the confusion matrix

st.write("Confusion Matrix:")
st.write(cm)

#from sklearn.metrics import plot_confusion_matrix

#plot_confusion_matrix(clf, X_test, y_test)  # Plot the confusion matrix
#plt.show()  # Show the plot


st.write('Here we are computing the precision and recall by importing some libraries called precision_score, recall_score')
st.info("The following we predicted the precision and recall for our dataset")

# Compute precision and recall
precision = precision_score(y_true, y_pred)
recall = recall_score(y_true, y_pred)

# Print the precision and recall
st.write("Precision: {:.3f}".format(precision))
st.write("Recall: {:.3f}".format(recall))

st.write('''
Here we are fitting the clf object on the training data and  Assuming that the trained and evaluated
-a classifier and obtained the predicted probabilities and true labels for Obtaining the predicted 
-probabilities of the positive class and computing the precision-recall curve and thresholds
''')
st.info("The following we are computing the precision-recall curve and precision-recall curve with varying thresholds by obtaining the predicted probabilities and true labels")

       

from sklearn.metrics import precision_recall_curve
import matplotlib.pyplot as plt

# Fit the clf object on the training data
clf.fit(X_train, y_train)

# Assuming you have trained and evaluated a classifier and obtained the predicted probabilities and true labels
y_scores = clf.predict_proba(X_test)[:, 1]  # Obtain the predicted probabilities of the positive class
precision, recall, thresholds = precision_recall_curve(y_test, y_scores)  # Compute the precision-recall curve and thresholds

# Plot the precision-recall curve
plt.plot(recall, precision)
plt.xlabel('Recall')
plt.ylabel('Precision')
plt.title('Precision-Recall Curve')
st.pyplot(plt.show())

# Plot the precision-recall curve with varying thresholds
plt.plot(thresholds, precision[:-1], label='Precision')
plt.plot(thresholds, recall[:-1], label='Recall')
plt.xlabel('Threshold')
plt.title('Precision-Recall Curve with Varying Thresholds')
st.pyplot(plt.show())
st.pyplot(plt.show())









