import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import pearsonr
import scipy

def get_key(my_dict, val):
    for key, value in my_dict.items():
        if val == value:
            return key
    return "key doesn't exist"

def create_plot(plot: str, series: pd.Series, source='seaborn'):
    fig, ax = plt.subplots()
    if source == 'seaborn':
        sns.set_theme(style='whitegrid')
        plot_mapping = {'displot': 'sns.histplot(x=series, ax=ax)',
                        'boxplot': 'sns.boxplot(y=series, ax=ax)',
                        'violinplot': 'sns.violinplot(x=series, ax=ax)',
                        'qqplot': "scipy.stats.probplot(series, dist='norm', plot=plt)"
                        }
    else:
        plot_mapping = None
        pass
    exec(plot_mapping[plot])
    plt.show()


def IQR_calculation(series: pd.Series, boundary_multiplier: float):
    iq_range = series.quantile(0.75) - series.quantile(0.25)
    lower_bound = series.quantile(0.25) - (iq_range * boundary_multiplier)
    upper_bound = series.quantile(0.75) + (iq_range * boundary_multiplier)
    outliers = series.loc[np.where((series > upper_bound)|(series<lower_bound))]
    print('Upper and Lower bounds for {} multiplier: {}'.format(boundary_multiplier, (lower_bound, upper_bound)))
    if len(outliers) == 0:
        print('No Outliers detected: No values outside the bounds')
    else:
        print('Printing Outliers: {} outlier points out of {} ({}% of the total) \n {}'
              .format(len(outliers), len(series), round(len(outliers)*100/len(series),2), outliers))


def violin_stripplot(data):
    sns.violinplot(y=data, showfliers=True)
    sns.stripplot(y=data, color='black')
    plt.show()


def box_stripplot(data):
    sns.boxplot(y=data, showfliers=True)
    sns.stripplot(y=data, color='black')
    plt.show()


def corrfunc(x, y, ax=None, **kws):
    """Plot the correlation coefficient in the top left hand corner of a plot."""
    r, _ = pearsonr(x, y)
    ax = ax or plt.gca()
    ax.annotate(f'ρ = {r:.2f}', xy=(.1, .9), xycoords=ax.transAxes)
