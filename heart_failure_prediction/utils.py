import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import scipy

def create_plot(plot: str, series: pd.Series, source='seaborn'):
    fig, ax = plt.subplots()
    if source == 'seaborn':
        sns.set_theme(style='whitegrid')
        plot_mapping = {'distplot': 'sns.distplot(x=series, ax=ax)',
                        'boxplot': 'sns.boxplot(y=series, ax=ax)',
                        'violinplot': 'sns.violinplot(x=series, ax=ax)',
                        'qqplot': "scipy.stats.probplot(series, dist='norm', plot=plt)"
                        }
    else:
        plot_mapping = None
        pass

    exec(plot_mapping[plot])

    plt.show()
