import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def create_plot(plot: str, series: pd.Series, source='seaborn'):
    fig, ax = plt.subplots()
    if source == 'seaborn':
        plot_mapping =  {'distplot': 'sns.distplot(x=series, ax=ax)',
                        'boxplot': 'sns.boxplot(y=series, ax=ax)',
                        'violinplot': 'sns.violinplot(x=series, ax=ax)'
                        }
    else:
        pass

    exec(plot_mapping[plot])

    plt.show()