from utils import *

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
        print(dataset.info())
        print(dataset.describe())
        print(dataset.head())

    def visualize_distribution(self, series: pd.Series, source = 'seaborn', list_of_plots: list = None):
        if list_of_plots is None:
            list_of_plots = ['distplot','boxplot', 'violinplot']

        for plot in list_of_plots:
            create_plot(plot, series, source = source)
            plt.show()











