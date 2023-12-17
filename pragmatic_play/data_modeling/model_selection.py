import pickle

import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier

from pragmatic_play.lib.sources_sinks import IO
from pragmatic_play.lib.modeling import TitanicClassification

# settings
mode = "testing"

# data processed reading

io = IO(mode=mode)

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

                    adaboost: {"n_estimators": [10, 20, 30, 50], "learning_rate": [0.1, 0.2, 0.3, 0.4, 0.5, 1.0]},

                    kneighbors: {"n_neighbors": list(np.arange(2, 10))}

                    }


for model_object, param_grid in grid_dictionary.items():
    obj_classification = TitanicClassification(model=model_object, train_data=train_data, test_data=test_data, io_settings=io_settings)
    x_train, y_train, x_val, y_val = obj_classification.train_test_split()

    best_score, best_params = obj_classification.grid_search_model(param_grid=param_grid)
    print(f'Classification {model_object}, "best_score": {best_score}, "best_params" : {best_params}')


best_params = {'criterion': 'gini', 'min_samples_leaf': 1, 'min_samples_split': 4, 'n_estimators': 50}
best_model = RandomForestClassifier(max_features='auto', oob_score=True, random_state=42, n_jobs=-1,
                                    criterion='gini',min_samples_leaf= 1, min_samples_split= 4, n_estimators= 50)

best_model_path = io_settings.model_sink
best_model.fit(train_data.drop(['Survived'], axis=1), train_data.Survived)
with open(best_model_path, 'wb') as f:
    pickle.dump(object, f)
