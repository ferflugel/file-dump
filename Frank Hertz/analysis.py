import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy.signal import find_peaks
import statsmodels.api as sm

# Reads data from file, Plotting the data and minima
for file in ['data2/data_2.txt', 'data2/data_4.txt',
             'data2/data_6.txt', 'data2/data_8.txt']:
    data = pd.read_csv(file, sep='\t')
    sns.lineplot(x=data['CH1 (V)  '], y=100 * data['CH2 (V)'])
    peaks, _ = find_peaks((-1) * data['CH2 (V)'].to_numpy(), distance=75)
    plt.plot(data['CH1 (V)  '][peaks], 100 * data['CH2 (V)'][peaks], "x")

# Showing the plot
sns.despine()
plt.show()

# Taking the average after using interpolation to reformat the arrays
x_data, y_data = [], []
x_range = np.linspace(0, 30, 100)
for file in ['data2/data_2.txt', 'data2/data_4.txt',
             'data2/data_6.txt', 'data2/data_8.txt']:
    data = pd.read_csv(file, sep='\t')
    x_data.append(x_range)
    y_data.append(np.interp(x_range, data['CH1 (V)  '], data['CH2 (V)']))

average = np.mean(y_data, axis=0)
maxima = np.amax(y_data, axis=0)
minima = np.amin(y_data, axis=0)
errors = np.std(y_data, axis=0)

# Plotting
sns.lineplot(x=x_range, y=average, ls='--', color='k', lw=1, label='Mean')
plt.fill_between(x_range, maxima, minima, alpha=0.3, color='blue', edgecolor=None)
peaks, _ = find_peaks((-1) * average, distance=10)
plt.hlines(0.060, x_range[peaks][3], x_range[peaks][4], color='k', lw=1)
plt.vlines(x_range[peaks][3], 0.060, 0.063, color='k', lw=1)
plt.vlines(x_range[peaks][4], 0.060, 0.063, color='k', lw=1)
plt.text(19.7, 0.063, '5.2 V')

# Showing the plot
sns.despine()
plt.legend(loc=4, frameon=False)
plt.xlabel('Accelerating voltage (V)')
plt.ylabel('Electrometer voltage (V)')
plt.title('Accelerating vs Electrometer Voltage')
plt.savefig('plots/line_plot_max_min', dpi=250)
plt.show()

# Line of best fit
variables = pd.DataFrame({'count': [1, 2, 3, 4, 5], 'const': [1, 1, 1, 1, 1]})
model = sm.OLS(pd.Series(x_range[peaks][1:]), variables[['count', 'const']]).fit()
print('\n\n', model.summary())
a, b = 5.2727, 2.3636
sns.lineplot(x=[0.5, 5.5], y=a*np.array([0.5, 5.5])+b, color='k', lw=1, alpha=1)

# Scatter plot of the peaks
sns.scatterplot(x=[1, 2, 3, 4, 5], y=x_range[peaks][1:], color=(1, 0.4118, 0.3804), alpha=1)

# Showing the plot
plt.xlim(0, 6)
plt.ylim(0, 33)
plt.xlabel('Valley number (count)')
plt.ylabel('Accelerating voltage (V)')
sns.despine()
plt.savefig('plots/scatter_plot_extrema', dpi=250)
plt.show()

