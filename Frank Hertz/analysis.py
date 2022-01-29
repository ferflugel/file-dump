import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy.signal import find_peaks

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

sns.lineplot(x=x_range, y=average, ls='--', color='k', lw=1, label='Mean')
plt.fill_between(x_range, maxima, minima, alpha=0.3, color='blue', edgecolor=None)

# Showing the plot
sns.despine()
plt.legend(loc=4, frameon=False)
plt.savefig('plots/line_plot_max_min', dpi=250)
plt.show()