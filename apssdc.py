# -*- coding: utf-8 -*-
"""Apssdc

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1lkeu53RcSXyQ4RNdAv0jgyohNrF_Ez66
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import pickle as pickle
import os

"""LODING DATASET"""

import pandas as pd
data = pd.read_excel("/content/employee_burnout_analysis-AI.xlsx")

"""DATA OVERVIEW"""

data.head()

data.tail(3)

data.describe()

data.columns.tolist()

data.nunique()

data.info()

data.isnull().sum()

data.isnull().sum().values.sum()

"""Exploratory Data Analysis

"""

data.corr(numeric_only=True)['Burn Rate'][:-1]

sns.pairplot(data)
plt.show()

"""Drop off all observations with NAN values of our dataframe

"""

data = data.dropna()

data.shape

data.dtypes

"""The employees ID doesn't provide any useful information and, therefore, they must be dropped"""

data = data.drop('Employee ID', axis = 1)

"""Checking the correlation of Data of Joining with Target variable"""

print(f"Min date {data['Date of Joining'].min()}")
print(f"Max date {data['Date of Joining'].max()}")
data_month = data.copy()

data_month["Date of Joining"] = data_month['Date of Joining'].astype("datetime64[ns]")# Specify time unit as nanoseconds
data_month["Date of Joining"].groupby(data_month['Date of Joining'].dt.month).count().plot(kind="bar", xlabel= 'Month', ylabel='Hired employees')

"""The date og joining is uniform distributed with values between 2008-01-01 and 2008-12-31. So in order to create a new feature which represents the labour seniority, we could create a variable with de days worked"""

data_2008 = pd.to_datetime(["2008-01-01"]*len(data))
#Specify time unit as nanoseconds when converting to datatime64
data["Days"] = data['Date of Joining'].astype("datetime64[ns]").sub(data_2008).dt.days
data.Days

#select only numeric columns before calculatingcorrelation
numeric_data = data.select_dtypes(include=['number'])
correlation = numeric_data.corr()['Burn Rate']
print(correlation)

data.corr(numeric_only=True)['Burn Rate'][:]

data = data.drop(['Date of Joining', 'Days'], axis =1)

data.head()

"""Now analysing the categorical variables"""

cat_columns = data.select_dtypes(object).columns
fig, ax = plt.subplots(nrows=1, ncols=len(cat_columns), sharey=True, figsize=(10, 5))
for i, c in enumerate(cat_columns):
  sns.countplot(x=c, data=data, ax=ax[i])
plt.show()

"""One-Hot Encoding for categorical features"""

# Check if the columns exist before applying get_dummies
if all(col in data.columns for col in ['Company Type', 'WFH Setup Available', 'Gender']):
    data = pd.get_dummies(data, columns=['Company Type', 'WFH Setup Available', 'Gender'], drop_first=True)
    data.head()
    encoded_columns = data.columns
else:
    print("Error: One or more of the specified columns are not present in the DataFrame.")
    print(data.columns)

"""Preprocessing"""

y = data['Burn Rate']
x = data.drop('Burn Rate', axis=1)

X_train, X_test, y_train, y_test = train_test_split(x, y, train_size=0.5, shuffle=True, random_state=1)
scaler = StandardScaler()
scaler.fit(X_train)
X_train = pd.DataFrame(scaler.transform(X_train), index=X_train.index, columns=X_train.columns)
X_test = pd.DataFrame(scaler.transform(X_train), index=X_train.index, columns=X_train.columns)

import os
import pickle
scaler_filename = '../models/scaler.pkl'
os.makedirs(os.path.dirname(scaler_filename), exist_ok=True)
with open(scaler_filename, 'wb') as scaler_file:
    pickle.dump(scaler, scaler_file)

X_train

y_train

path = '../data/processed/'
os.makedirs(path, exist_ok=True)
X_train.to_csv(path + 'X_train_processed.csv', index=False)
y_train.to_csv(path + 'y_train_processed.csv', index=False)

"""Model Building

Linear Regression
"""

linear_regression_model = LinearRegression()
linear_regression_model.fit(X_train, y_train)

print("Linear Regression Model Performance Metrics:\n")
y_pred = linear_regression_model.predict(X_test)

mse = mean_squared_error(y_test, y_pred)
print("Mean Squared Error:", mse)

rmse = mean_squared_error(y_test, y_pred, squared=False)
print("Root Mean Squared Error:", rmse)

mae = mean_absolute_error(y_test, y_pred)
print("Mean Absolute Error:", mae)

r2 = r2_score(y_test, y_pred)
print("R-squared Score:", r2)

# Check the shape of X_test and y_test
print("Shape of X_test:", X_test.shape)
print("Shape of y_test:", y_test.shape)

# If the shapes don't match, revisit your data splitting process.
# Ensure that X_test and y_test are derived from the same original dataset
# and were split using consistent indices.