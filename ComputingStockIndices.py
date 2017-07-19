import pandas as pd
import pandas_datareader as web   # Package and modules for importing data; this code may change depending on pandas version
import datetime
import numpy as np
import math
from stockstats import StockDataFrame as sdf
import matplotlib.pyplot as plt 

 
# Enter the start date to be used
date_start = input('Enter a start date in YYYY-MM-DD format:')
year, month, day = map(int, date_start.split('-'))
start = datetime.date(year, month, day)

#Enter the end date to be used
date_end = input('Enter a date in YYYY-MM-DD format:')
year, month, day = map(int, date_end.split('-'))
end = datetime.date(year, month, day)

 
# First argument is the series we want, second is the source ("yahoo" for Yahoo! Finance), third is the start date, fourth is the end date

enty=input("which stock to analyze:")
ent_stock = web.DataReader(enty, "google", start, end)


#delta variance definition

def delta_variance(stock, my_list):
    variance = 0
    average = np.round(stock.rolling(window = my_list, center = False).mean(), 2)
    for i in range(my_list):
        variance += (average - stock[i]) ** 2
    return variance / my_list

#delta_StandardDev

def delta_StandardDev(stock, my_list):
    Value1 = delta_variance(stock, my_list)
    dstd = ( Value1 ) ** 0.5
    return dstd

#delta_BollingerBands

def delta_BollingerBands(stock, my_list, NumDevs):
    average=np.round(stock.rolling(window = my_list, center = False).mean(), 2)
    dbtbands = average + NumDevs * delta_StandardDev(stock, my_list)
    return dbtbands

#delta_PctBollinger

def delta_PctBollinger(stock, my_list, NumDevs):
    value1 = delta_BollingerBands(stock, my_list,+NumDevs)
    value2 = delta_BollingerBands(stock, my_list,-NumDevs)
    value3 = (stock - value2) / (value1 - value2)
    return value3

#%b_close

def percentbclose(stock, my_list, NumDevs):
    value1=100 * delta_PctBollinger(stock, my_list, NumDevs)
    return value1

#Bollinger bands

def bollingerbands(stock,my_list,Numdevs):
    value1 = np.round(stock["Close"].rolling(window = 20, center = False).mean(), 2) + stock["Close"].rolling(window = 20, center = False).std() * Numdevs
    return value1

def indicator_list(stock):
    stock["bclose"]=percentbclose(stock["Close"], 20, 3)
    stock["20d"] = np.round(stock["Close"].rolling(window = 20, center = False).mean(), 2)
    stock["50d"] = np.round(stock["Close"].rolling(window = 50, center = False).mean(), 2)
    stock["200d"] = np.round(stock["Close"].rolling(window = 200, center = False).mean(), 2)
    stock["upper_band"]=bollingerbands(stock,20,2)
    stock["lower_band"]=bollingerbands(stock,20,-2)
    stock_df=sdf.retype(stock)
    stock["rsi"]=stock_df['rsi_9']   
    del stock["close_-1_s"]
    del stock["close_-1_d"]
    del stock["rs_9"]
    del stock["rsi_9"]
    stock["brsi"]=percentbclose(stock["rsi"][1:], 20, 3)
    
    
indicator_list(ent_stock)

def plotting_indicators(stock):
    #This line is necessary for the plot to appear in a Jupyter notebook
    %matplotlib inline   
    #Control the default size of figures in this Jupyter notebook
    %pylab inline               
    pylab.rcParams['figure.figsize'] = (15, 9)   # Change the size of plots
    fig=figure(figsize=(12,12), dpi=120)
    fig.set_size_inches(14, 15)
    subplot(3,1,1) 
    stock["close"].plot(grid = True, label='Close') # Plot the closing price of aapl
    stock["upper_band"].plot(grid = True, label='Upper Band')
    stock["lower_band"].plot(grid = True, label='Lower Band')
    title('Plot of closing price, %bclose and %brsi for stock ' + enty)
    legend(loc = 'upper right' , shadow=True)
    ylabel('Price'); grid(True)
    subplot(3,1,2)
    stock["bclose"].plot(grid = True, label='%bclose') # Plot the bclose price of aapl
    legend(loc = 'upper right', shadow=True)
    ylabel('%bclose'); grid(True)
    subplot(3,1,3)
    stock["brsi"].plot(grid = True, label='%brsi') # Plot the brsi price of aapl
    legend(loc = 'upper right', shadow=True)
    ylabel('%brsi'); grid(True)
    
    
plotting_indicators(ent_stock)
