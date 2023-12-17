import tensorflow as tf
import keras
import numpy as np
from keras.layers import Dense
from keras.models import Sequential
from sklearn.model_selection import cross_validate, cross_val_score, GridSearchCV, train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier

from pragmatic_play.lib.sources_sinks import IO
from pragmatic_play.lib.modeling import TitanicClassification

# settings
mode = "testing"

# data processed reading

io = IO(mode=mode)

# model_engine = TitanicClassification()

# input dataframes
train_path_to_read = io.main_sink + '/train_data_processed.csv'
test_path_to_read = io.main_sink + '/test_data_processed.csv'

train_data = io.read_dataframe_from_csv(csv_path_to_read=train_path_to_read)
test_data = io.read_dataframe_from_csv(csv_path_to_read=test_path_to_read)

y_train_data = train_data.Survived
x_train_data = train_data.drop(['Survived'], axis=1)
io_settings = IO(mode="test")
# Classification

# random forest classifier
random_forest = RandomForestClassifier()
adaboost = AdaBoostClassifier()
kneighbors = KNeighborsClassifier()

grid_dictionary = {random_forest: {"criterion": ["gini", "entropy"], "min_samples_leaf": [1, 5, 10], "min_samples_split": [2, 4, 10, 12, 16],
                                  "n_estimators": [50, 100, 400, 700, 1000]
                                  },

                    #adaboost: {},

                    kneighbors: {"n_neighbors": list(np.arange(2, 10))}

                    }

for model_object, param_grid in grid_dictionary.items():
    obj_classification = TitanicClassification(model=model_object, train_data=train_data, test_data=test_data, io_settings=io_settings)
    x_train, y_train, x_val, y_val = obj_classification.train_test_split()

    best_score, best_params = obj_classification.grid_search_model(param_grid=param_grid)
    print(f'Classification {model_object}, "best_score": {best_score}, "best_params" : {best_params}')
