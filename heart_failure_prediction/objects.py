from utils import *
import pandas as pd
import matplotlib.pyplot as plt
from typing import Union, List

class Importer:
    def __init__(self):
        self.__name = 'Importer'
        self._mapping_file = {'original_dataset': 'heart_failure_clinical_records_dataset.csv'}

    def import_dataset(self, dataset):
        path = './data/{}'.format(self._mapping_file[dataset])
        dataframe_to_return = pd.read_csv(path)
        return dataframe_to_return


class Explorer:
    def __init__(self):
        self.__name='Importer'

    def main_info(self, dataset):
        pd.set_option('display.max_columns', None)
        print('dataset.info()')
        print(dataset.info())
        print('____________________________________________________________')
        print('____________________________________________________________')
        print('dataset.describe()')
        print(dataset.describe())
        print('____________________________________________________________')
        print('____________________________________________________________')
        print('dataset.head()')
        print(dataset.head())
        print('____________________________________________________________')
        print('____________________________________________________________')
        print('dataset.dtypes')
        print(dataset.dtypes)
        print('____________________________________________________________')
        print('____________________________________________________________')
        pd.reset_option('display')

    def visualize_distribution(self, series: pd.Series, source='seaborn', list_of_plots: List = None):
        if list_of_plots is None:
            list_of_plots = ['distplot', 'boxplot', 'violinplot', 'qqplot']

        for plot in list_of_plots:
            create_plot(plot, series, source=source)
            plt.show()

    def quantify_missing(self, dataset):
        print('Number of Missing Values per variable')
        print(dataset.isnull().sum())
        print('______________________________________________________')
        print('Percentage of Missing Values per variable')
        print(data.isnull().mean())

    def visualize_outliers(self, data: Union[pd.Series, pd.DataFrame], list_of_columns: List = None, boundary_multiplier: float = 1.5, plot_selection: str = 'violin'):
        if list_of_columns is None:
            plot_mapping = {'violin': 'violin_stripplot(data)',
                            'box': 'box_stripplot(data)'
                            }
            IQR_calculation(data, boundary_multiplier=boundary_multiplier)
            exec(plot_mapping[plot_selection])
        else:
            for column in list_of_columns:
                print('COLUMN: {}'.format(column))
                IQR_calculation(data[column], boundary_multiplier=boundary_multiplier)
                print('____________________________________________________________')
                print('____________________________________________________________')
                print('____________________________________________________________')

    def visualize_variable_relationship(self, data: pd.DataFrame , columns: List = None, mode: str = 'all_predictors'):
        """
        We need to visualize relationships:
        a. Between two predictors
        b. Between more than two predictors
        c. Between as many predictors as we want and the target variable, depending on the type of the predictor (categorical or continuous)
        :param mode: Defines the mode of the desired visualization
        :param data: DataFrame to perform the visualization on
        :param columns: Desired selected columns to use
        """
        if columns is None:
            pass
        else:
            data = data.loc[:, columns]


        if mode=="all_predictors":
            corr=data.corr()
            ax1 = sns.heatmap(
                corr,
                vmin=-1, vmax=1, center=0,
                cmap=sns.diverging_palette(20, 220, n=200),
                square=True
            )
            ax2 = sns.pairplot(data, corner = True).map_lower(corrfunc)
            plt.show()