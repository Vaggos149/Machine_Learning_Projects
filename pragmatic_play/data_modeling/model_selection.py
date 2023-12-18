import pickle
import warnings

import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier

from pragmatic_play.lib.sources_sinks import IO
from pragmatic_play.lib.modeling import TitanicClassificationEvaluation

# warnings
# temporarily ingores warnings
warnings.filterwarnings("ignore")
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

# set output paths
best_model_path = io.best_model_path

# Classification
# random forest classifier
random_forest = RandomForestClassifier()
adaboost = AdaBoostClassifier()
kneighbors = KNeighborsClassifier()

grid_dictionary = {"random_forest": {"classifier": RandomForestClassifier(),

                                     "params": {"criterion": ["gini", "entropy"], "min_samples_leaf": [1, 5, 10], "min_samples_split": [2, 4, 10, 12, 16],
                                                "n_estimators": [50, 100, 400, 700, 1000]}
                                     },
                   "adaboost": {"classifier": AdaBoostClassifier(),

                                "params": {"n_estimators": [10, 20, 30, 50], "learning_rate": [0.1, 0.2, 0.3, 0.4, 0.5, 1.0]}
                                },

                   "kneighbors": {"classifier": KNeighborsClassifier(),

                                  "params": {"n_neighbors": list(np.arange(2, 10))}
                                  }
                   }

for model_object in grid_dictionary.keys():
    obj_classification = TitanicClassificationEvaluation(model=grid_dictionary[model_object]["classifier"], train_data=train_data, test_data=test_data, io_settings=io_settings)

    best_score, best_params = obj_classification.grid_search_model(param_grid=grid_dictionary[model_object]["params"])
    cv_results = obj_classification.cross_validate_model()
    print(f'Classification {model_object}, f"best_score of {obj_classification.gs_scoring_method}": {best_score}, "best_params" : {best_params}')
    print('Cross Validation mean f1: {}'.format(np.mean(cv_results['test_score'])))
    # cross validation

# choice of best parameters --> RandomForestClassifier with {'criterion': 'gini', 'min_samples_leaf': 1, 'min_samples_split': 2, 'n_estimators': 1000}
best_params = {'criterion': 'gini', 'min_samples_leaf': 1, 'min_samples_split': 2, 'n_estimators': 1000}
best_model = RandomForestClassifier(max_features='auto', oob_score=True, random_state=42, n_jobs=-1,
                                    criterion='gini', min_samples_leaf=1, min_samples_split=2, n_estimators=1000)

best_model.fit(train_data.drop(['Survived'], axis=1), train_data.Survived)

with open(best_model_path, 'wb') as f:
    pickle.dump(best_model, f)

print("Ending model selection process")

