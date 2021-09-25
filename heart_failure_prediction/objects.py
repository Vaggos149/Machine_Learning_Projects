import utils
import pandas as pd
import matplotlib.pyplot as plt
from typing import Union, List, Dict
import seaborn as sns

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
        self.__name='Explorer'

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
            list_of_plots = ['displot', 'boxplot', 'violinplot', 'qqplot']

        for plot in list_of_plots:
            utils.create_plot(plot, series, source=source)
            plt.show()

    def quantify_missing(self, dataset):
        print('Number of Missing Values per variable')
        print(dataset.isnull().sum())
        print('______________________________________________________')
        print('Percentage of Missing Values per variable')
        print(dataset.isnull().mean())

    def visualize_outliers(self, data: Union[pd.Series, pd.DataFrame], list_of_columns: List = None, boundary_multiplier: float = 1.5, plot_selection: str = 'violin'):
        if list_of_columns is None:
            plot_mapping = {'violin': 'violin_stripplot(data)',
                            'box': 'box_stripplot(data)'
                            }
            utils.IQR_calculation(data, boundary_multiplier=boundary_multiplier)
            exec(plot_mapping[plot_selection])
        else:
            for column in list_of_columns:
                print('COLUMN: {}'.format(column))
                utils.IQR_calculation(data[column], boundary_multiplier=boundary_multiplier)
                print('____________________________________________________________')
                print('____________________________________________________________')
                print('____________________________________________________________')

    def visualize_variable_relationship(self, data: pd.DataFrame, columns: List = None,
                                        mode: str = None, selected_variables: Dict = None,
                                        hue=None):
        """
        We need to visualize relationships:
        a. Between two predictors
        b. Between more than two predictors
        c. Between as many predictors as we want and the target variable, depending on the type of the predictor (categorical or continuous)
        :param mode: Defines the mode of the desired visualization. Available modes are [None,pair_of_predictors,target_predictors]
        :param data: DataFrame to perform the visualization on
        :param columns: Desired selected columns to use as keys, type 'continuous' or 'categorical' as values
        :param size: Optional parameter 'size' for seaborn functionality
        :param hue: Optional parameter  'hue' for seaborn functionality
        """

        if mode is None:
            if columns is None:
                print('Columns parameter not provided: Visualizing for all variables in the dataset')
                print('______________________________________________________________________________')
                pass
            else:
                data = data.loc[:, columns]
            corr=data.corr()
            ax1 = sns.heatmap(
                corr,
                vmin=-1, vmax=1, center=0,
                cmap=sns.diverging_palette(20, 220, n=200),
                square=True
            )
            ax2 = sns.pairplot(data, corner=True).map_lower(utils.corrfunc)
            plt.show()

        elif mode == "pair_of_predictors":
            if len(selected_variables)!=2:
                raise Exception('selected_variables length does not match mode \'pair_of_variables\'. '
                                'This mode requires the user to/'
                                'provide a pair of variables - columns of the input dataframe as a list: e.g. [var1,var2]')

            if all(variable_type == 'continuous' for variable_type in selected_variables.values()):
                ax1 = sns.scatterplot(data=data, x=list(selected_variables.keys())[0], y=list(selected_variables.keys())[1],
                                      hue=hue)
                plt.show()
            elif all(variable_type == 'categorical' for variable_type in selected_variables.values()):

                ax1 = sns.catplot(x=list(selected_variables.keys())[0], y=list(selected_variables.keys())[1],
                                  hue=hue, kind='bar', data=data)
                ax2 = sns.catplot(x=list(selected_variables.keys())[0], hue=list(selected_variables.keys())[1],
                                  kind='count', data=data)
                ax3 = sns.catplot(x=list(selected_variables.keys())[0], y=list(selected_variables.keys())[1],
                                  hue=hue,  kind='point', data=data)
                plt.show()
            else:
                continuous_variable = utils.get_key(selected_variables, 'continuous')
                categorical_variable = utils.get_key(selected_variables, 'categorical')
                ax1 = sns.catplot(x=categorical_variable, y=continuous_variable, hue=hue,
                                  kind='box', dodge=False, data=data)
                ax2 = sns.catplot(x=categorical_variable, y=continuous_variable, hue=hue,
                                  kind='violin', dodge=False, data=data)
                ax3 = sns.catplot(x=categorical_variable, y=continuous_variable, hue=hue,
                                  kind='swarm', dodge=False, data=data)
                plt.show()