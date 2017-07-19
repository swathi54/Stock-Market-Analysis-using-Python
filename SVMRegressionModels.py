#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 14 13:13:07 2017
@author: Swathi Annamalai
@Purpose: Stock Market Price Prediction using SVM. We are using a few different
          files here - google.csv, google2.csv
@Files Used: google.csv - Data from 1st Feb2017 - 26thFeb; predict for 28th Feb
             google2.csv - Data from 1st May2017 - 15thMay; predict for 16th May
@Modules Used:  We will be using scikit-learn, csv, numpy and matplotlib 
                packages to implement and visualize SVM  

"""
# Importing all modules needed
import csv #to read csv file
import numpy as np #used for array processing and conversion
from sklearn.svm import SVR #

# for visualization
import matplotlib.pyplot as plt

#codecs provides classes that manage the data encoding and decoding
#all text data needs to be decoded from its byte representation as 
#it is read, and encoded from the internal values to a specific 
#representation as it is written.
import codecs 

# Arrays for storing date and price from both csv files
dates = []
prices = []

dates2 = []
prices2 = []

# Function to read data from google.csv
def get_data(filename):
	with codecs.open(filename, 'r',encoding='utf-8') as csvfile:
		csvFileReader = csv.reader(csvfile)
		next(csvFileReader)	# skipping column names
		for row in csvFileReader:
			dates.append(int(row[0].split('-')[0]))
			prices.append(float(row[1]))
	return

# Function takes in 3 arguemnts. It predicts Googles stock price based on 
# given dates and prices from file
# Dates - int type, Price - opening price of stock for day and x = date for 
# which we want to predict the price (29/ 16) 
def predict_price(dates, prices, x):
	dates = np.reshape(dates,(len(dates), 1)) # converting to matrix of n X 1
    
# SVM - Plots data in n-dimensional space (n = features); value(feature) = value of coordinate
#Classification performed by finding right hyper plane to define 2classes
#Best hyperplane identified when best separation is achieved. It ignores 
#outliers and finds hyperplane with highest margin.

#Kernel = these are functions that convert non-separable problem to separable problem
        
    #defining the support vector regression models
    #Linear model 
	svr_lin = SVR(kernel= 'linear', C= 1e2)
    #RBF and Poly are useful for non-linear hyperplane
	svr_poly = SVR(kernel= 'poly', C= 1e2, degree= 2)
	svr_rbf = SVR(kernel= 'rbf', C= 1e2, gamma= 0.1) 
    
    #fitting the data points in the models
	svr_rbf.fit(dates, prices) 
	svr_lin.fit(dates, prices)
	svr_poly.fit(dates, prices)
    
    #plotting the initial datapoints 
	plt.scatter(dates, prices, color= 'black', label= 'Data') 
    #plotting the line made by the RBF kernel
	plt.plot(dates, svr_rbf.predict(dates), color= 'red', label= 'RBF model') 
    #plotting the line made by linear kernel
	plt.plot(dates,svr_lin.predict(dates), color= 'blue', label= 'Linear model') 
    #plotting the line made by polynomial kernel
	plt.plot(dates,svr_poly.predict(dates), color= 'green', label= 'Polynomial model') 
	plt.xlabel('Date')
	plt.ylabel('Stock Price')
	plt.title('Support Vector Regression Models on Google Stock Price')
	plt.legend()
	plt.show()
	return svr_rbf.predict(x)[0], svr_lin.predict(x)[0], svr_poly.predict(x)[0]

# Function to read data from google2.csv
get_data('/Users/SwatzMac/Desktop/google.csv') # calling get_data method by passing the csv file to it
print ("Dates- ", dates)
print ("Prices- ", prices)
# Predicting Price of Google for 28th Feb 2017
print("RBF, Linear and Polynomial: ",predict_price(dates, prices, 28))
#(814.35241956144057, 837.33999999997991, 848.26657832874275)
print("Actual Price of Google on 02/28/2017: 823.21")
# Actual Price Closed: 823.21

def get_data2(filename):
	with codecs.open(filename, 'r',encoding='utf-8') as csvfile:
		csvFileReader = csv.reader(csvfile)
		next(csvFileReader)	# skipping column names
		for row in csvFileReader:
			dates2.append(int(row[0].split('-')[0]))
			prices2.append(float(row[1]))
	return
get_data2('/Users/SwatzMac/Desktop/google2.csv')
print ("Dates- ", dates2)
print ("Prices- ", prices2)
# Predicting Price of Google for 16th May 2017
print("RBF, Linear and Polynomial: ",predict_price(dates2, prices2, 16))
#(930.41606173545415, 939.03888888889173, 939.00399999928754)
print("Actual Price of Google on 05/16/2017: 943.00")
# Actual Price Closed: 943.00

