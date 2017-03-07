#!/usr/bin/python3
# coding: utf-8


"""Examples of DNN regressor for Housing dataset"""

from __future__  import  absolute_import 
from __future__ import  division
from __future__ import print_function

from sklearn import cross_validation
from sklearn import metrics
from sklearn import preprocessing
import tensorflow as tf
import numpy as np



# load dataset
boston = tf.contrib.learn.datasets.load_dataset('boston')
x, y = boston.data, boston.target
# print(np.shape(x),np.shape(y))

# Split dataset into train/test
x_train, x_test, y_train, y_test = cross_validation.train_test_split(x, y, test_size=0.2, random_state=42)

# scale data(training set) to 0 mean and unit standard deviation
scaler = preprocessing.StandardScaler()
x_train = scaler.fit_transform(x_train)

# build 2 layers fully connected DNN with 10, 10 units respectively
feature_columns = tf.contrib.learn.infer_real_valued_columns_from_input(x_train)


# tf.contrib.learn.Estimator()


regressor = tf.contrib.learn.DNNRegressor(feature_columns=feature_columns, hidden_units=[10,10])

print(x_train)
print(feature_columns)

# fit
regressor.fit(x_train, y_train, steps=5000, batch_size=1)

x_transformed = scaler.transform(x_test)

y_predicted = list(regressor.predict(x_transformed, as_iterable=True))
score = metrics.mean_squared_error(y_predicted, y_test)

print('MSE: {0:f}'.format(score))

