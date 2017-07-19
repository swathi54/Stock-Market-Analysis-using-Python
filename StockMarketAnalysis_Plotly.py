#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 10 17:31:07 2017

@author: Swathi Annamalai
@Purpose: Stock Market Analysis using Plotly. 
@Data Used: Data used from Yahoo Finance using panda datareader
@Modules Used:  We will be using scikit-learn, csv, numpy and matplotlib 
                packages to implement and visualize SVM
"""

##### IMPORT LIBRARIES AND SETUP ENVIRONMENT ######
### 1. Exploring Stock Prices, Averages and Returns 
import pandas as pd
import numpy as np
import statsmodels

# For Visualization
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
#sns.set_style('whitegrid')

# PLOTLY imports
# plotly.plotly contains all the machinery to communicate with Plotly
import plotly 
import plotly.figure_factory as ff
import plotly.graph_objs as go

# plotly charts are described declaratively with objects in 
# plotly.graph_objs. Every aspect of a plotly chart (the colors, the grids, 
# the data, and so on) has a corresponding key-value attribute in these objects. 

# plotly.graph_objs contains all the helper classes to make/style plots
from plotly.graph_objs import *

# import cufflings to easily plot pandas data frames
import cufflinks as cf
cf.set_config_file(theme='white')

# for making some beautiful custom color scales
import colorlover as cl

# For Reading Stock Sata from YAHOO
from pandas_datareader.data import DataReader

# For Date TimeStamps
from datetime import datetime

# import sys 
import sys

# Filter out Warnings that can be ignored
import warnings
warnings.filterwarnings('ignore')

# for reproducibility purposes, here are the versions of modules used 
print("statsmodels: {}".format(statsmodels.__version__))
print("numpy: {}".format(np.__version__))
print("pandas: {}".format(pd.__version__))
print("matplotlib: {}".format(matplotlib.__version__))
print("seaborn: {}".format(sns.__version__))
print("plotly: {}".format(plotly.__version__))
print("python: {}".format(sys.version))

# Using pandas library, lets fetch and analyze data for these companies:
    # MSFT, Google, Amazon and Apple

# Set up End and Start times for retrieving Data
end = datetime.now()
# Let's go back to a year worth of data
start = datetime(end.year - 1,end.month,end.day)

# Grab stock data for Apple, Google, Microsoft and Amazon
AAPL = DataReader('AAPL', 'yahoo', start, end)
GOOG = DataReader('GOOG', 'yahoo', start, end)
AMZN = DataReader('AMZN', 'yahoo', start, end)
MSFT = DataReader('MSFT', 'yahoo', start, end)

#print(AAPL)
# change the Timestamp index in the four data frames to Date
tech_list = [AAPL, GOOG, AMZN, MSFT]

for stock in tech_list:   
    stock["Date"] = stock.index.date
for stock in tech_list:
    stock.set_index("Date", drop=True, inplace=True)

#plotly.offline.plot(ff.create_table(GOOG.describe().round(2), index = True))

# General Info on Google data 
print(GOOG.info())

### Change in Price of GOOGLE Stock over time
data = [go.Scatter(x=GOOG.index, y=GOOG.High)]
layout = go.Layout(title = 'GOOGLE Closing Price')

fig = go.Figure(data=data,layout=layout)
plotly.offline.plot(fig,filename='google-closing-price')


### To get better overview of price variations, we plot MOVING AVERAGES
# Moving Average is a constantly updated average price for a stock over a specified period
# Ex. 10-day MA presents its first data point as the avg prices from Day1-10
# Next data point is avg of prices from Day2-Day11 and so on

# What was the moving average of the 4stocks?
moving_avg_days = [10,20,50]
GOOG['10days MA'] = GOOG['Adj Close'].rolling(10).mean()
GOOG['20days MA'] = GOOG['Adj Close'].rolling(20).mean()
GOOG['50days MA'] = GOOG['Adj Close'].rolling(50).mean()

table = plotly.offline.plot(ff.create_table(GOOG.round(2).head(20), index = True, index_title = "Date"))
table['layout'].update(width = 950)
plotly.offline.plot(table,filename='moving-avg-google')

### 2. Analyzing the Great Recession in Dec 2007 and Google price change 
df = DataReader("goog", 'yahoo', datetime(2007, 10, 1), datetime(2010, 10, 1))

trace = go.Candlestick(x=df.index,
                       open=df.Open,
                       high=df.High,
                       low=df.Low,
                       close=df.Close)
data = [trace]
layout = {
    'title': 'Google Stock behavior during the 2007 Recession',
    'yaxis': {'title': 'GOOGLE Stock Price'},
    'shapes': [{
        'x0': '2007-12-01', 'x1': '2007-12-01',
        'y0': 0, 'y1': 1, 'xref': 'x', 'yref': 'paper',
        'line': {'color': 'rgb(30,30,30)', 'width': 1}
    }],
    'annotations': [{
        'x': '2007-12-01', 'y': 0.05, 'xref': 'x', 'yref': 'paper',
        'showarrow': False, 'xanchor': 'left',
        'text': 'Start of the Recession'
    }]
}
fig = dict(data=data, layout=layout)
#plotly.offline.plot(fig, filename='google-recession-candlestick')

# Grab all the closing prices for the tech stock list into one DataFrame
stocks = ['AAPL','GOOG','MSFT','AMZN']
closing_df = DataReader(stocks,'yahoo',start,end)['Adj Close']
closing_df_2 = DataReader(stocks,'yahoo',start,end)['Adj Close']

# change the timestamp to date
closing_df["Date"] = closing_df.index.date
closing_df.set_index("Date", drop=True, inplace=True)

# Let's compare the closing prices(Adj Close) of 4 tech stocks
fig1 = closing_df.iplot(asFigure = True, subplots = True, title='Compare Closing Prices')
plotly.offline.plot(fig1, filename = 'compare-closing-prices')

# Stacking the stocks on a single plot
#figstack = closing_df.iplot(fill=True, asFigure=True, title="Tech Giants Closing Price", filename = 'stacked closing prices')
closing_df_2["Date"] = closing_df_2.index.date
closing_df_2.set_index("Date", drop=True, inplace=True)

figstack = closing_df_2.iplot(fill=True, asFigure=True, title="Tech Giants Closing Price")

plotly.offline.plot(figstack, filename = 'stacked closing prices')

### CORRELATION ANALYSIS ### 
# Correlation is a statistical measure to analyze of how stocks move in 
# relation to one another. 
# Correlation is represented by correlation coefficient - PEARSON COEFFICIENT r
# ranging between -1 and +1
# When the prices of two stocks usually move in a similar direction, 
# the stocks are considered positively correlated. The amount of 
# correlation ranges from 0, which means no correlation, to 1, 
# which means perfect correlation. Perfect correlation means the 
# relationship that appears to exist between two stocks is positive 100% 
# of the time.

# Make a new tech returns DataFrame
tech_rets = closing_df.pct_change()

# Let's look at correlation between Google and itself
sns.jointplot('GOOG','GOOG', data = tech_rets, kind='scatter',
              color='purple', edgecolor="w", s = 40, alpha = 0.8,
              marginal_kws=dict(bins=20),
              space = 0.3, xlim = (-0.06, 0.06), ylim = (-0.06, 0.06))


# get the current figure
fig2 = plt.gcf()

# convert it to plotly figure
fig2 = plotly.tools.mpl_to_plotly(fig2)

# update figure layout
fig2['layout'].update(# control x and y axes of the marginal histograms
                     yaxis2 = dict(nticks = 4, showgrid = False),
                     xaxis2 = dict(ticks = "", showticklabels = False, 
                                   showgrid = True, showline = False),
                     # control x and y axes of the right marginal histogram
                     yaxis3 = dict(ticks = "", showticklabels = False),
                     xaxis3 = dict(nticks = 5, showgrid = False),
                     width = 850,
                     height = 450)

plotly.offline.plot(fig2, filename = 'tech returns')

## Comparing Google to itself shows a linear relationship 

## Correlate Google to Microsoft 
sns.jointplot('GOOG','MSFT', data = tech_rets, kind='scatter',
              color='blue', edgecolor="w", s = 50, space = 0.3,
              marginal_kws=dict(bins=20), xlim = (-0.06, 0.06))

# get the current matplotlib figure
fig3 = plt.gcf()

# convert matplotlib figure to a plotly one
plotly_fig = plotly.tools.mpl_to_plotly(fig3)

# change the marker line color and width
for trace in plotly_fig['data']:
    #trace['opacity'] = 0.7
    trace['marker']['line']['color'] = 'white'
    trace['marker']['line']['width'] = 0.65

# polish the layout by controlling the ticks of the marginal histograms
plotly_fig['layout'].update(# control x and y axes of the top marginal histogram
                            yaxis2 = dict(nticks = 4, showgrid = False),
                            xaxis2 = dict(ticks = "", showline = False,
                                          showticklabels = False, 
                                          showgrid = True),
                            # control x and y axes of the right marginal histogram
                            yaxis3 = dict(ticks = "", showticklabels = False),
                            xaxis3 = dict(nticks = 5, showgrid = False),
                            width = 850,
                            height = 450)


# Plotting the correlation
plotly.offline.plot(plotly_fig, filename = 'Correlation between Goog and MSFT')


## Lets repeat this correlation for all 4 tech stocks 
# What was the correlation between closing prices of the 4 tech stocks?
fig4 = ff.create_scatterplotmatrix(tech_rets, diag='histogram', size = 5,height=740, width=880)

for trace in fig4['data']:
    trace['opacity'] = 0.7
    trace['marker'] = dict(color = "seagreen", line = dict(color = 'white', 
                                                       width = 0.7))

plotly.offline.plot(fig4, filename = 'Correlation between 4 Tech Giants')

## A quick glance shows all four stocks are highly correlated with each 
# other. This which means you should not put all of them in one portfolio. 
# Rather, you should pick the least correlated ones and combine them with 
# stocks from other industries that have low correlation with the chosen 
# stocks. This is a wise path towards a more diverse portfolio, and
# reducing losses.


### Let's Diversify the portfolio ###





