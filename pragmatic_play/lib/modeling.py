from typing import List, Union

import pandas as pd

from sklearn.model_selection import cross_validate, GridSearchCV
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
import xgboost as xgb

from pragmatic_play.lib.sources_sinks import IO


class TitanicClassificationEvaluation:

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
        self.gs_scoring_method = "f1"

    def grid_search_model(self, param_grid):
        # give train data, perform cross validation and return best parameters and model type
        gs = GridSearchCV(estimator=self.model, param_grid=param_grid, scoring=self.gs_scoring_method, cv=3, n_jobs=-1)
        gs.fit(self.train_data.drop(['Survived'], axis=1), self.train_data.Survived)

        return gs.best_score_, gs.best_params_

    def cross_validate_model(self):
        cv_results = cross_validate(self.model, self.train_data.drop(['Survived'], axis=1), self.train_data.Survived)

        return cv_results

