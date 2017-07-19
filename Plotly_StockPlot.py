###!/usr/bin/env python3
### -*- coding: utf-8 -*-
##"""
##Created on Tue May  9 15:43:42 2017
##
##@author: SwatzMac
##"""
#
##### Plotly to show Apple stock price changes over period of time
import plotly.plotly 
import plotly.graph_objs as go

from datetime import datetime
import pandas_datareader.data as web

df = web.DataReader("aapl", 'yahoo',
                    datetime(2015, 1, 1),
                    datetime(2016, 7, 1))

data = [go.Scatter(x=df.index, y=df.High)]

plotly.offline.plot(data)


#### Apple stock behavior from recession and till 2009
import plotly.plotly as py
import plotly.graph_objs as go

from datetime import datetime
import pandas_datareader.data as web

df = web.DataReader("aapl", 'yahoo', datetime(2007, 10, 1), datetime(2009, 4, 1))

trace = go.Candlestick(x=df.index,
                       open=df.Open,
                       high=df.High,
                       low=df.Low,
                       close=df.Close)
data = [trace]
layout = {
    'title': 'The Great Recession',
    'yaxis': {'title': 'AAPL Stock'},
    'shapes': [{
        'x0': '2007-12-01', 'x1': '2007-12-01',
        'y0': 0, 'y1': 1, 'xref': 'x', 'yref': 'paper',
        'line': {'color': 'rgb(30,30,30)', 'width': 1}
    }],
    'annotations': [{
        'x': '2007-12-01', 'y': 0.05, 'xref': 'x', 'yref': 'paper',
        'showarrow': False, 'xanchor': 'left',
        'text': 'Official start of the recession'
    }]
}
fig = dict(data=data, layout=layout)
plotly.offline.plot(fig, filename='aapl-recession-candlestick')

#### Time Series with Rangeslider showing Apple High and Low
import plotly.plotly as py
import plotly.graph_objs as go

import pandas as pd

df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv")

trace_high = go.Scatter(
    x=df.Date,
    y=df['AAPL.High'],
    name = "AAPL High",
    line = dict(color = '#17BECF'),
    opacity = 0.8)

trace_low = go.Scatter(
    x=df.Date,
    y=df['AAPL.Low'],
    name = "AAPL Low",
    line = dict(color = '#7F7F7F'),
    opacity = 0.8)

data = [trace_high,trace_low]

layout = dict(
    title='Time Series with Rangeslider',
    xaxis=dict(
        rangeselector=dict(
            buttons=list([
                dict(count=1,
                     label='1m',
                     step='month',
                     stepmode='backward'),
                dict(count=6,
                     label='6m',
                     step='month',
                     stepmode='backward'),
                dict(step='all')
            ])
        ),
        rangeslider=dict(),
        type='date'
    )
)

fig = dict(data=data, layout=layout)
plotly.offline.plot(fig, filename = "Time Series with Rangeslider")


### Candlestick Animation 
from numpy import nan
import numpy as np

import matplotlib.pyplot as plt
from matplotlib.finance import candlestick_ohlc
from matplotlib.animation import FuncAnimation

fig = plt.figure()
ax = fig.add_subplot(111)

def test(dummy):
    opn =  104.04852126730329
    close = np.random.uniform(90, 110)
    high = max(opn, close)*np.random.uniform(1, 1.05)
    low = min(opn, close)*np.random.uniform(0.95, 1)
    DOCHLV = np.array([[1, 100, 99, 101, 98, 0.0], [2, nan, nan, nan, nan, 0.0], [3, nan, nan, nan, nan, 0.0], [4, 104, 98, 105, 95, 0.0], [5, nan, nan, nan, nan, 0.0], [6, nan, nan, nan, nan, 0.0], [7, 100, 99.99976844819628, 100.91110690369828, 97.82248296015564, 1152.3258524820196], [8, 99.99976844819628, 100.51985544064271, 100.51985544064271, 96.65206230438159, 1578.5836411214814], [9, 100.51985544064271, 104.04852126730329, 104.54571702827914, 99.49632496479201, 1477.5651279091041], [10, opn, close, high, low, 372.6679262982206]])
    candlestick_ohlc(ax, DOCHLV, width=0.8, colorup='g', colordown='r', alpha=1.0)
    ax.set_xlim(0, len(DOCHLV)+1)
anim = FuncAnimation(fig, test, interval=25)
plt.show()




