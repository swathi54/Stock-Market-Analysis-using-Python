from scipy.interpolate import interp1d
from urllib.request import urlopen
 
import matplotlib.pyplot as plt
import numpy as np
 
url = 'http://real-chart.finance.yahoo.com/table.csv?s=GOOG&amp;amp;amp;amp;d=9&amp;amp;amp;amp;e=17&amp;amp;amp;amp;f=2015&amp;amp;amp;amp;g=d&amp;amp;amp;amp;a=3&amp;amp;amp;amp;b=12&amp;amp;amp;amp;c=1996&amp;amp;amp;amp;ignore=.csv'
google_csv = urlopen(url)
data_google = np.genfromtxt(google_csv, delimiter=',', dtype=None)
 
# Checking out the file header.
print(data_google[0:4, :])

adj_close = np.array(data_google[1:, 6:].flatten(), dtype=float)
plt.figure()
plt.plot(adj_close, 'r')
plt.xlabel('Days')
plt.ylabel('Adjusted Close Price')
plt.show()

# Using the vector size to create the X axis.
end = np.shape(adj_close)[0]
adj_x = np.linspace(0, end, end, endpoint=True)
 
# Interpolating points in the entire function.
interp_linear = interp1d(adj_x, adj_close, kind='linear')
interp_adjclose = interp_linear(adj_x)
 
# Plotting the interpolation.
plt.figure()
plt.plot(adj_x, adj_close, 'ro', adj_x, interp_adjclose, 'k--')
plt.xlabel('Days')
plt.ylabel('Adjusted Close Price')
plt.show()

# Let's try in a smaller interval.
# We'll get the first ten days.
adj_piece = adj_close[:10]
 
# Let's create an X axis from 0 to 10, with 50 points:
axis_x = np.linspace(0, 10)
 
# We'll use interp_linear with axis_x values.
interp_piece_lin = interp_linear(axis_x)
# Plotting the interpolation.
plt.figure()
plt.plot(axis_x, interp_piece_lin, 'k+', adj_piece, 'ro')
plt.xlabel('Days')
plt.ylabel('Adjusted Close Price - Linear interpolation')
plt.show()
 
# Trying now the cubic interpolation (kind='cubic').
interp_cubic = interp1d(adj_x, adj_close, kind='cubic')
interp_piece_cub = interp_cubic(axis_x)
# Plotting the interpolation.
plt.figure()
plt.plot(axis_x, interp_piece_cub, 'k+', adj_piece, 'ro')
plt.xlabel('Days')
plt.ylabel('Adjusted Close Price - Cubic interpolation')
plt.show()
