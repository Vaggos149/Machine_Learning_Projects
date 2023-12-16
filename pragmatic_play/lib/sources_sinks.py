import pickle
import pandas as pd

project_name = "pragmatic_play"
user = "john_rocker"


class IO:
    """
    Defines the main object for reading / writing functionality
    """

    def __init__(self, mode):
        self.mode = mode
        self.main_sink = "D:/Machine_Learning_Projects/pragmatic_play/data_storage"

    @staticmethod
    def read_dataframe_from_csv(csv_path_to_read: str,
                                ):
        df = pd.read_csv(csv_path_to_read)

        return df

    def write_dataframe_to_csv(self,
                               dataset: pd.DataFrame,
                               dataset_name: str = None):

        dataset.to_csv(self.main_sink + f'/{dataset_name}.csv')

    def save_model(self,
                   model,
                   model_name: str):

        pickle.dump(model, open(self.main_sink + f'/{model_name}', 'wb'))


