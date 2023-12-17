import pickle
from typing import List, Union

import pandas as pd

from sklearn.model_selection import cross_validate, GridSearchCV, train_test_split
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
import xgboost as xgb

from pragmatic_play.lib.sources_sinks import IO


class TitanicClassification:

    def __init__(self,
                 model: List[Union[RandomForestClassifier, AdaBoostClassifier, xgb.XGBClassifier]],
                 train_data: pd.DataFrame,
                 test_data: pd.DataFrame,
                 io_settings: IO,
                 ):

        self.io_settings = io_settings
        self.model = model
        self.train_data = train_data
        self.test_data = test_data
        self.x_train = None
        self.y_train = None
        self.x_val = None
        self.y_val = None
        self.gs_scoring_method = "f1"
        self.best_model_path = io_settings.model_sink

    def train_test_split(self):
        self.x_train, self.y_train, self.x_val, self.y_val = train_test_split(self.train_data.drop(['Survived'], axis=1), self.train_data.Survived, test_size=0.33, random_state=42)

        return self.x_train, self.y_train, self.x_val, self.y_val

    def grid_search_model(self, param_grid):
        # give train data, perform cross validation and return best parameters and model type
        gs = GridSearchCV(estimator=self.model, param_grid=param_grid, scoring='accuracy', cv=3, n_jobs=-1)
        gs.fit(self.x_train, self.y_train)

        return gs.best_score_, gs.best_params_

    def cross_validate_model(self):
        cv_results = cross_validate(self.model, self.train_data, self.test_data)

        return cv_results

    # def best_model_selections(self):
    #     cv_results
    #     pass

    def save_model(self):
        pickle.dump(self.best_model, open(self.best_model_path, 'wb'))

    def load_model(self, file_path):
        loaded_model = pickle.load(open(file_path, 'rb'))
