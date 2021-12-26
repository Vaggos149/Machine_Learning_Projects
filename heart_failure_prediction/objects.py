import utilities
import pandas as pd
import matplotlib.pyplot as plt
from typing import Union, List, Dict
import seaborn as sns
from settings import *


class Importer:
    def __init__(self):
        self.__name = 'Importer'
        self._mapping_dataset_name = {'original_dataset': 'heart_failure_clinical_records_dataset.csv'}
        self.data_file_path = main_project_path + './data'

    def import_dataset(self, dataset_name):
        path = self.data_file_path + '/{}'.format(self._mapping_dataset_name[dataset_name])
        imported_dataset = pd.read_csv(path)
        return imported_dataset


class Explorer:
    def __init__(self):
        self.__name = 'Explorer'
        self.list_of_plots_distribution_visualization = ['displot', 'boxplot', 'violinplot', 'qqplot']
        self.outlier_visualization_plot_mapping = {'violin': 'utilities.violin_stripplot(colname=column, data=data)',
                                                   'box': 'utilities.box_stripplot(colname=column, data=data)'
                                                   }
        self.outlier_boundary_multiplier = 1.5

    @staticmethod
    def main_info(dataset):
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

    def visualize_variable_distribution(self,
                               series: pd.Series,
                               list_of_plots: List = None):
        plt.close('all')  # closing all existing plots to avoid figure overriding

        if list_of_plots is None:
            list_of_plots = self.list_of_plots_distribution_visualization

        for plot in list_of_plots:
            utilities.create_plot(plot, series)
            plt.show()

    @staticmethod
    def quantify_missing(dataset):
        print('Number of Missing Values per variable')
        print(dataset.isnull().sum())
        print('______________________________________________________')
        print('Percentage of Missing Values per variable')
        print(dataset.isnull().mean())

    def visualize_outliers(self,
                           data: Union[pd.Series, pd.DataFrame],
                           list_of_columns: List = None,
                           boundary_multiplier: float = None,
                           plot_selection: str = None):
        plt.close('all')  # closing all existing plots to avoid figure overriding

        if boundary_multiplier is None:
            boundary_multiplier = self.outlier_boundary_multiplier

        if list_of_columns is None:  # if no list_of_columns is provided by the user, the code runs for the whole dataset
            list_of_columns = list(data.columns)

        if plot_selection is None:
            print('No Plot Selection for outlier visualization was selected...Skipping plotting')

        for column in list_of_columns:
            print('COLUMN: {}'.format(column))
            try:
                utilities.iqr_calculation(data[column], boundary_multiplier=boundary_multiplier)
            except TypeError:
                print(f'Column {column} is of a DataType which is inappropriate for IQR calculation..Skipping calculation for this column')
                pass
            if plot_selection is None:
                pass
            else:
                try:
                    fig = plt.figure()
                    fig.add_subplot()
                    exec(self.outlier_visualization_plot_mapping[plot_selection])
                    plt.show()
                except TypeError:
                    print(f'Column {column} cannot reproduce the plot of your choice...'
                          f'Please, make sure you select appropriate selections of columns-plots')
            print('____________________________________________________________')
            print('____________________________________________________________')
            print('____________________________________________________________')

    @staticmethod
    def visualize_variable_relationship(data: pd.DataFrame,
                                        mode: str = None,
                                        selected_variables_and_types_dict: Dict = None,
                                        hue=None):
        """
        We need to visualize relationships:
        a. Between two predictors
        b. Between more than two predictors
        c. Between as many predictors as we want and the target variable, depending on the type of the predictor (categorical or continuous)
        :param selected_variables_and_types_dict: Includes a Dictionary of selected_variables : {varName: type_of_var},
                where type_of_var is either "continuous" or "categorical"
        :param mode: Defines the mode of the desired visualization. Available modes are [multiple_variables,pair_of_variables]
        :param data: DataFrame to perform the visualization
        :param hue: Optional parameter  'hue' for seaborn functionality
        """
        plt.close('all')  # closing all existing plots to avoid figure overriding
        if mode is None:
            print("Mode is not selected. Printing for default plot mode: 'multiple_variables'")
            mode = 'multiple_variables'

        if mode is "multiple_variables":
            if selected_variables_and_types_dict is None:
                print('Columns parameter not provided: Visualizing for all variables in the dataset')
                print('______________________________________________________________________________')
                pass
            else:
                data = data.loc[:, selected_variables_and_types_dict.keys()]
            corr = data.corr()
            ax1 = sns.heatmap(
                corr,
                vmin=-1, vmax=1, center=0,
                cmap=sns.diverging_palette(20, 220, n=200),
                square=True
            )
            ax2 = sns.pairplot(data, corner=True).map_lower(utilities.corrfunc)

        elif mode == "pair_of_variables":
            if len(selected_variables_and_types_dict) != 2:
                raise Exception('selected_variables length does not match mode \'pair_of_variables\'. '
                                'This mode requires the user to/'
                                'provide a pair of variables - columns of the input dataframe as a list: e.g. [var1,var2]')

            if all(variable_type == 'continuous' for variable_type in selected_variables_and_types_dict.values()):
                ax1 = sns.scatterplot(data=data,
                                      x=list(selected_variables_and_types_dict.keys())[0],
                                      y=list(selected_variables_and_types_dict.keys())[1],
                                      hue=hue)
                plt.show()

            elif all(variable_type == 'categorical' for variable_type in selected_variables_and_types_dict.values()):
                ax1 = sns.countplot(x=list(selected_variables_and_types_dict.keys())[0],
                                    hue=list(selected_variables_and_types_dict.keys())[1],
                                    data=data)

                ax2 = (pd.crosstab(data[list(selected_variables_and_types_dict.keys())[0]],
                                   data[list(selected_variables_and_types_dict.keys())[1]],
                                   normalize='index'
                                   ).plot.bar(stacked=True, rot=0)
                       ).legend(loc=2)
                plt.show()

            else:
                continuous_variable = utilities.get_key(selected_variables_and_types_dict, 'continuous')
                categorical_variable = utilities.get_key(selected_variables_and_types_dict, 'categorical')
                ax1 = sns.catplot(x=categorical_variable, y=continuous_variable, hue=hue,
                                  kind='box', dodge=False, data=data)
                ax2 = sns.catplot(x=categorical_variable, y=continuous_variable, hue=hue,
                                  kind='violin', dodge=False, data=data)
                ax3 = sns.catplot(x=categorical_variable, y=continuous_variable, hue=hue,
                                  kind='swarm', dodge=False, data=data)

                plt.show()
